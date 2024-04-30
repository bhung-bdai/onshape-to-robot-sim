#!/usr/bin/env python3

from __future__ import annotations
from typing import Any, Callable, Optional, Sequence

from collections import deque
from dataclasses import dataclass, asdict
from enum import Enum
import json
import pdb
import os

import numpy as np
import numpy.typing as npt

from onshape_to_sim.onshape_api.client import Client
from onshape_to_sim.onshape_api.utils import (
    API,
    APIAttributes,
    CommonAttributes,
    ElementAttributes,
    FeatureAttributes,
    MassAttributes,
    OccurrenceAttributes,
    PartAttributes,
    check_and_append_extension,
    get_relevant_metadata,
    join_api_url,
)
from onshape_to_sim.utils import (
    express_mass_properties_in_world_frame
)

# TODO: figure out if this is going to be here later
onshape_client = Client(creds="test_config.json", logging=False)
# TODO: load these from a config

part_relevant_metadata = set(("Rigid Body",))
assembly_relevant_metadata = set(("Rigid Body",))

def get_element_tform_mate(mated_cs: dict) -> npt.ArrayLike:
    element_tform_mate = np.eye(4)
    element_tform_mate[:3, 0] = np.array(mated_cs[FeatureAttributes.xAxis])
    element_tform_mate[:3, 1] = np.array(mated_cs[FeatureAttributes.yAxis])
    element_tform_mate[:3, 2] = np.array(mated_cs[FeatureAttributes.zAxis])
    element_tform_mate[:3, 3] = mated_cs[FeatureAttributes.origin]
    return np.round(element_tform_mate, decimals=10)


class OnshapeTreeNode():
    """A tree representing assemblies, subassemblies, and parts of an Onshape API request.

    The root of the tree is the root of the assembly. Children of each node are either subassemblies or parts.
    Leaves are guaranteed to be parts, while branches are guaranteed to be assemblies. The information each mate/joints
    if stored in every single instance which is inside that mate. The root has
    """
    def __init__(
        self,
        name: str,
        depth: int = 0,
        element_dict: Optional[dict] = None,
        node_id: Optional[str] = None,
        occurrence_id: str = "",
        parent_node: Optional[OnshapeTreeNode] = None,
        is_rigid_body: bool = False,
        ):
        self.element_dict: Optional[dict] = element_dict
        self.node_id: Optional[str] = node_id
        self.name: str = name
        # Assumes the last two parts are the <instance_number> value_number
        self.mesh_name: str = "".join((self.name.split(" ")[:-2])).lower()
        self.simplified_name: str = self._simplified_name()
        self.parent_node: Optional[Self] = parent_node
        self.is_rigid_body: bool = is_rigid_body
        self.children: list = []
        self.depth: int = depth
        self.occurrence_id: str = occurrence_id
        self.hidden: bool = False
        # self.joint_child_info: list = []
        self.world_tform_element: npt.ArrayLike = np.eye(4)
        self.element_tform_mate: Optional[npt.ArrayLike] = None
        self.com_wrt_world = np.zeros((3,))
        self.inertia_wrt_world = np.zeros((3, 3))
        self.mass = 0.0
        self.has_mass = False
        self.volume = 0.0
        self.links = [] # For root only
        self.rigid_bodies = [] # For root only
        self.occurrence_id_to_node = {} # For root only
        self.internal_naming = {} # For root only
        self.joint_parents = {} # For root only TODO rename this

    def _simplified_name(self):
        simple_name = ""
        for char in self.name:
            if char == "<" or char == ">":
                continue
            elif char == " ":
                simple_name += "_"
            else:
                simple_name += char.lower()
        return simple_name

    def __repr__(self):
        return f"{self.name} ({self.simplified_name}, mesh_name: {self.mesh_name}): {self.occurrence_id} (depth {self.depth})"

    def get_joint_parents(self):
        return self.joint_parents

    def get_rigid_bodies(self):
        return self.rigid_bodies

    def get_occurrence_id_to_node(self):
        return self.occurrence_id_to_node

    def add_child(self, child_node: OnshapeTreeNode) -> None:
        """Append a new node to this node's list of children.""" 
        self.children.append(child_node)

    def print_children(self):
        """Print nodes followed by a list of their children"""
        print(f"{self}", end=": ")
        print(f"{self.children}")
        for child in self.children:
            child.print_children()

    def print_element_ids(self):
        """Print nodes followed by their element ids"""
        print(f"{self}", end=": ")
        print(f"{self.element_dict[CommonAttributes.elementId]}")
        for child in self.children:
            child.print_element_ids()

    def print_transforms(self):
        """Print nodes and their transforms"""
        print(f"{self}", end=": ")
        print(f"{self.world_tform_element}")
        for child in self.children:
            child.print_transforms()

    def print_names(self):
        """Print nodes"""
        print(f"{self}")
        for child in self.children:
            child.print_names()

    def print_mass_properties(self):
        """Print mass properties"""
        print(f"{self}", end=": ")
        print(f"Mass: {self.mass}. Has mass: {self.has_mass}. COM: {self.com_wrt_world}")
        for child in self.children:
            child.print_mass_properties()

    def search_by_occurrence_id(self, occurrence_id: str) -> Optional[OnshapeTreeNode]:
        if self.occurrence_id == occurrence_id:
            return self
        for child in self.children:
            child.search_by_occurrence_id(occurrence_id)

    def _initialize_node(
        self,
        occurrence_map: dict,
        joint_map: dict,
        joint_parents: dict,
        ) -> None:
        self._add_occurrence_info(occurrence_map)
        self._add_joint_info(joint_map, joint_parents)
    
    def _add_occurrence_info(self, occurrence_map: dict,) -> None:
        """Adds the information about the occurrence with the path and transform into the element.

        Args:
            occurrence_map: mapping of path (joined into a single string) to the occurrence
        """
        if self.occurrence_id == "":
            return
        if self.occurrence_id not in occurrence_map:
            raise ValueError(f"Instance {self.occurrence_id} not in occurrences!")
        occurrence = occurrence_map[self.occurrence_id]
        self.world_tform_element = np.array(occurrence[CommonAttributes.transform]).reshape(4, 4)
        # self.world_tform_element = self.parent_node.world_tform_element @ self.world_tform_element
        self.hidden = bool(occurrence[OccurrenceAttributes.hidden])

    def _add_joint_info(self, joint_map: dict, joint_parents: dict) -> None:
        """Get the mates associated with the node from the dictionary and store them here.

        Currently I think only parts can be done this way, so we only store joint information on a per-part basis.
        
        Args:
            joint_map: a mapping of occurrence ids and their feature information
        """
        # TODO: explain all this nonsense
        if self.occurrence_id is None or self.occurrence_id not in joint_map:
            return
        for joint in joint_map[self.occurrence_id]:
            # breakpoint()
            # Thanks again to Onshape for being incompatible with this implementation
            # Basically you need to go up to the nearest rigid body because mate connectors can only occur on faces of 
            # parts. So if the parent assembly is the link, then we need to find it to define the joint instead
            link_name = self.closest_rigid_body_link()

            if link_name not in joint_parents:
                joint_parents[link_name] = [joint]
            else:
                joint_parents[link_name].append(joint)

    def closest_rigid_body_link(self) -> str:
        # Thanks again to Onshape for being incompatible with this implementation
        # Basically you need to go up to the nearest rigid body because mate connectors can only occur on faces of 
        # parts. So if the parent assembly is the link, then we need to find it to define the joint instead
        link_name = self.simplified_name
        parent = self.parent_node
        while not self.is_rigid_body and parent is not None:
            if parent.is_rigid_body:
                link_name = parent.simplified_name
                break
            parent = parent.parent_node
        return link_name

    def _add_mass_properties(self, mass_properties_map: dict) -> None:
        """Adds information about the mass, com, and inertia into the element.

        These values are all expressed in the element's own frame. They need to be mapped into the world frame using the
        transforms provided with the occurrence.

        Args:
            mass_properties_map: mapping of instance id to mass properties
        """
        mass_properties = mass_properties_map[self.node_id]
        self.volume = mass_properties[MassAttributes.volume]
        self.has_mass = mass_properties[MassAttributes.hasMass]
        self.mass, self.com_wrt_world, self.inertia_wrt_world = express_mass_properties_in_world_frame(
            world_tform_element = self.world_tform_element,
            mass = mass_properties[MassAttributes.mass],
            com_in_element_frame = mass_properties[MassAttributes.centroid],
            inertia_in_element_frame = mass_properties[MassAttributes.inertia]
        )
        

# TODO: combine subassemblies into a single mass property thing

def _build_subassemblies_map(subassemblies: list) -> dict:
    """Constructs a map of subassembly element id to subassembly information.
    
    We choose to map by elementId because duplicated assemblies are just references to the same subassembly with an 
    updated instance id.

    Args:
        subassemblies: the subassemblies information returned in the OnShape API call

    Returns:
        A mapping of elementId to subassembly information
    """
    subassemblies_map = {}
    for subassembly in subassemblies:
        subassembly_element_id = subassembly[CommonAttributes.elementId]
        subassemblies_map[subassembly_element_id] = subassembly
    return subassemblies_map


def _extract_mass_properties(response: dict) -> dict:
    """Extracts mass properties from an Onshape API call.
    
    Args:
        response: the parsed JSON response from the API call

    Returns:
        A mapping of the mass properties to their relevant data
    """
    mass_properties = {}
    mass_properties[MassAttributes.mass] = response[MassAttributes.mass][0]
    mass_properties[MassAttributes.hasMass] = response[MassAttributes.hasMass]
    mass_properties[MassAttributes.volume] = response[MassAttributes.volume][0]
    mass_properties[MassAttributes.centroid] = np.array(response[MassAttributes.centroid][:3])
    mass_properties[MassAttributes.inertia] = np.array(response[MassAttributes.inertia][:9]).reshape(3, 3)
    return mass_properties


def _add_instances_mass_properties(onshape_client: Client, instances: list, mass_properties_map: dict) -> None:
    """Updates a map from instance ids to mass properties in-place.
    
    Args:
        instances: the instances we want to add query mass properties for
        mass_properties_map: map of instance id to mass properties that we want to update
    """ 
    for instance in instances:
        instance_id = instance[CommonAttributes.idNum]
        if instance_id in mass_properties_map:
            continue
        did = instance[CommonAttributes.documentId]
        eid = instance[CommonAttributes.elementId]
        if CommonAttributes.version in instance:
            wvm = API.version
            wvmid = instance[CommonAttributes.version]
        else:
            wvm = API.microversion
            wvmid = instance[CommonAttributes.documentMicroversion]
        if PartAttributes.partId in instance:
            part_id = instance[PartAttributes.partId]
            response = onshape_client.part_mass_properties(did=did, wvmid=wvmid, eid=eid, partid=part_id, wvm=wvm)
            masses = [response[MassAttributes.bodies][part_id] for part_id in response[MassAttributes.bodies]]
        else:
            # Is an assembly
            response = onshape_client.assembly_mass_properties(did=did, wvmid=wvmid, eid=eid, wvm=wvm)
            masses = [response]
        for mass in masses:
            mass_properties = _extract_mass_properties(mass)
            mass_properties_map[instance_id] = mass_properties


def _build_mass_properties_map(onshape_client: Client, instances: list, subassemblies: list) -> dict:
    """Given a list of instances, return a map from their occurence ids to mass properties in each instance and subassembly.
    
    We need to map this separately because each will require an API call to either the assembly mass properties or the 
    part mass properties. The part mass properties will need a partID. I wish we could just aggregate a list of all
    the mass properties but it's not possible under the current configuration, as PartStudio ignores assemblies. 
    
    Args:
        instances: the instances of assemblies and parts inside the document.
        subassemblies: the subassemblies inside the document

    Returns:
        A map of occurrence IDs to their mass properties
    """
    mass_properties_map = {}
    _add_instances_mass_properties(onshape_client, instances, mass_properties_map)
    for subassembly in subassemblies:
        # Add all of the instances from the subassemblies into the mass properties map
        _add_instances_mass_properties(onshape_client, subassembly[APIAttributes.instances], mass_properties_map)
    return mass_properties_map

def _build_features_map(features: list, subassemblies: list) -> dict:
    """Constructs a map of path and mate data.

    Mapping path to the feature data of the mate. This is because mates occur between instances of objects, but they 
    aren't separated by the instance ids. Instead they're uniquely determined by the path. Wish they would just assign 
    ids but I think it's a clever way to leverage references? 

    Args:
        features: the features information returned in the OnShape API Call

    Returns:
        A mapping of occurrence ids to mates
    """
    features_map = {}
    # TODO @bhung add subassemblies
    # for subassembly in json_assembly_data[APIAttributes.subassemblies]:
    #     occurrence_path = 
    #     assembly_features += subassembly[APIAttributes.features]
    for feature in features:
        mated_entities = feature[FeatureAttributes.featureData][FeatureAttributes.matedEntities]
        mate_type = feature[FeatureAttributes.featureData][FeatureAttributes.mateType]
        mate_name = feature[FeatureAttributes.featureData][CommonAttributes.name]
        # TODO @bhung figure out if the assumption that the parent is the final entity is true
        # Loop through the n - 1 children and added them
        entity_one_path = "".join(mated_entities[0][FeatureAttributes.matedOccurrence])
        entity_two_path = "".join(mated_entities[1][FeatureAttributes.matedOccurrence])
        if entity_one_path == "":
            parent_entity = mated_entities[0]
            parent_path = entity_one_path
            child_path = mated_entities[1]
        else:
            parent_entity = mated_entities[1]
            parent_path = entity_two_path
            child_path = mated_entities[0]
        parent_info = {
            FeatureAttributes.children: [],
            FeatureAttributes.is_parent: True,
            FeatureAttributes.mateType: mate_type,
            CommonAttributes.name: mate_name, 
        }
        # Based on docs, onshape forces mates to have 2 things
        # Initialize the child information
        parent_info[FeatureAttributes.children]= child_path
        # Extract the transform from the parent
        parent_info[CommonAttributes.transform] = get_element_tform_mate(parent_entity[FeatureAttributes.matedCS])

        # TODO: Check if we still need this eventually
        # child_info = {
        #     FeatureAttributes.parent: parent_path,
        #     FeatureAttributes.is_parent: False,
        #     FeatureAttributes.mateType: mate_type,
        #     CommonAttributes.name: mate_name,
        # }
        # child_path = "".join(child_entity[FeatureAttributes.matedOccurrence])
        # child_info[CommonAttributes.transform] = get_element_tform_mate(child_entity[FeatureAttributes.matedCS])
        # if child_path in features_map:
        #     features_map[child_path].append(child_info)
        # else:
        #     features_map[child_path] = [child_info]

        # Check and add the information into the feature map
        if parent_path in features_map:
            features_map[parent_path].append(parent_info)
        else:
            features_map[parent_path] = [parent_info]
    return features_map


def _add_instances_metadata(onshape_client: Client, instances: list, metadata_map: dict) -> dict:
    for instance in instances:
        instance_id = instance[CommonAttributes.idNum]
        if instance_id in metadata_map:
            continue
        did = instance[CommonAttributes.documentId]
        eid = instance[CommonAttributes.elementId]
        # Check if we want to use the version of the microversion
        if CommonAttributes.version in instance:
            wvm = API.version
            wvmid = instance[CommonAttributes.version]
        else:
            wvm = API.microversion # TODO: Check if document microversions are a consistent thing across all subassemblies
            wvmid = instance[CommonAttributes.documentMicroversion]
        # Check if it's a part or assembly
        if PartAttributes.partId in instance:
            part_id = instance[PartAttributes.partId]
            response = onshape_client.part_metadata(did=did, wvmid=wvmid, eid=eid, partid=part_id, wvm=wvm)
            metadata_value_map = get_relevant_metadata(response, part_relevant_metadata)
        else:
            # Is an assembly
            response = onshape_client.element_metadata(did=did, wvmid=wvmid, eid=eid, wvm=wvm)
            metadata_value_map = get_relevant_metadata(response, assembly_relevant_metadata)
        metadata_map[instance_id] = metadata_value_map
        

def _build_metadata_map(onshape_client: Client, instances: list, subassemblies: list) -> dict:
    """Given a list of instances, return a map of their occurence ids to metadata for each instance and subassembly.
    
    We need to map this separately because each will require an API call to each of the assembly or 
    part metadata. The part mass properties will need a partID. I wish we could just aggregate a list of all
    the metadata properties but they need to be accessed assembly-wise individually. 

    Note: we use instances as the key instead of occurrence id, because each instance shares the same metadata values.
    If you copy multiple parts/assemblies, they ALL SHARE THE SAME METADATA.
    
    Args:
        instances: the instances of assemblies and parts inside the document.
        subassemblies: the subassemblies inside the document

    Returns:
        A map of occurrence IDs to their mass properties
    """
    metadata_map = {}
    _add_instances_metadata(onshape_client, instances, metadata_map)
    for subassembly in subassemblies:
        # Add all of the instances from the subassemblies into the mass properties map
        _add_instances_metadata(onshape_client, subassembly[APIAttributes.instances], metadata_map)
    return metadata_map


def _build_occurrences_map(occurrences: list) -> dict:
    """Constructs a map of their paths (concatenated) and the occurrence.

    This is necessary to get the relative locations of all the items in the SDF.
    Since occurrences can have the same ID if they're part of the same subassembly, we instead need
    to look at their paths in order to find out where everything should be. For instance, if I copy
    assembly A, then parts b, c in A will have the same ID twice. The path will show up differently
    in the occurrence and needs to be appropriately followed to figure out which is which. 

    Because lists aren't hashable, I have chosen to instead just use the joined list as the key for the poses.
    
    Returns:
        A map from the concatenated strings in the path to occurrence data
    """
    occurrences_map = {}
    for occurrence in occurrences:
        occurrence_key = "".join(occurrence[OccurrenceAttributes.path])
        occurrences_map[occurrence_key] = occurrence
    return occurrences_map
        

def build_tree(json_assembly_data: dict, robot_name: str) -> OnshapeTreeNode:
    """Given a JSON Onshape API call for the elements in an assembly, return a tree representing the entire assembly.
    
    Args:
        json_assembly_data: the json returned by a call to the Onshape API

    Returns:
        The root of the Onshape tree
    """
    root_dict = json_assembly_data[APIAttributes.rootAssembly]
    # TODO see if this is necessary later
    root_dict[CommonAttributes.name] = CommonAttributes.root
    root_subassemblies = _build_subassemblies_map(json_assembly_data[APIAttributes.subassemblies])
    assembly_features = root_dict[APIAttributes.features]
    # Add in the ability to recurse into the subassembly later for other joints
    # for subassembly in json_assembly_data[APIAttributes.subassemblies]:
    #     occurrence_path = 
    #     assembly_features += subassembly[APIAttributes.features]
    root_mates = _build_features_map(assembly_features, json_assembly_data[APIAttributes.subassemblies])
    root_occurrences = _build_occurrences_map(root_dict[APIAttributes.occurrences])
    root_instances = root_dict[APIAttributes.instances]
    root_metadata = _build_metadata_map(
        onshape_client,
        root_instances,
        json_assembly_data[APIAttributes.subassemblies]
        )
    root_mass_properties = _build_mass_properties_map(
        onshape_client,
        root_instances,
        json_assembly_data[APIAttributes.subassemblies]
        )
    root_node = OnshapeTreeNode(name=robot_name, element_dict=root_dict)
    # breakpoint()
    build_tree_helper(
        root_node,
        root_subassemblies,
        root_mates,
        root_occurrences,
        root_mass_properties,
        root_metadata,
        )
    return root_node


def build_tree_helper(
    root: OnshapeTreeNode,
    document_subassemblies: dict,
    document_mates: dict,
    document_occurrences: dict,
    document_mass_properties: dict,
    document_metadata: dict,
    ) -> None:
    """Helper function which, given the root node and API document information, fills out the tree with nodes.

    Args:
        root: the root node of the Onshape tree
        document_subassemblies: a mapping of element ids to subassemblies
        document_mates: a mapping of occurence ids to mates
        document_occurrences: a mapping of path (joined into a single string) to the occurrence information
    """ 
    stack = deque()
    stack.append(root)
    depth = 0
    is_root_node = True
    while len(stack) > 0:
        next_node = stack.pop()
        next_element = next_node.element_dict
        # From the document holding the information about mates, add it in
        next_node._initialize_node(document_occurrences, document_mates, root.joint_parents)
        if is_root_node:
            is_root_node = False
        else:
            next_node._add_mass_properties(document_mass_properties)
        # Iterate through the elements in the API instances 
        for instance in next_element[APIAttributes.instances]:
            # Create a child node
            occurrence_id = instance[CommonAttributes.idNum]
            instance_name = instance[CommonAttributes.name]
            # print(occurrence_id)
            # Check if we've seen this element name. If so, assign a unique name and add it
            if instance_name not in root.internal_naming:
                root.internal_naming[instance_name] = 0
            else:
                root.internal_naming[instance_name] += 1

            # Check if it's a rigid body
            is_rigid = False
            if occurrence_id in document_metadata:
                # TODO: replace the hard coding later
                metadata = document_metadata[occurrence_id]
                try:
                    is_rigid = metadata["Rigid Body"]
                except KeyError:
                    # Rigid Body isn't a property, so we skip it 
                    is_rigid = False

            child_node = OnshapeTreeNode(
                depth=next_node.depth+1,
                element_dict=instance,
                node_id=occurrence_id,
                name=f"{instance_name} {root.internal_naming[instance_name]}",
                occurrence_id=f"{next_node.occurrence_id}{occurrence_id}",
                parent_node=next_node,
                is_rigid_body=is_rigid
                )
            root.occurrence_id_to_node[child_node.occurrence_id] = child_node
            # Add information about the occurrences and mates
            child_node._initialize_node(document_occurrences, document_mates, root.joint_parents)
            # Recalculate the COM and inertia wrt world frame, given by occurrence transform
            child_node._add_mass_properties(document_mass_properties)

            # Check if the object is a rigid body or not
            if is_rigid:
                root.rigid_bodies.append(child_node)

            # TODO: see if we can set the base case to a rigid body. Need to find the nearest rigid body
            # Base case: we hit a part. Add the child to the node and skip adding it to the queue
            if instance[CommonAttributes.elementType] == ElementAttributes.part:
                next_node.add_child(child_node)
                continue

            # Recursive case: we hit a subassembly. Add it to the top of the stack with its subassembly data
            child_id = instance[CommonAttributes.elementId]
            child_node.element_dict = document_subassemblies[child_id]
            stack.append(child_node)
            next_node.add_child(child_node)


def download_all_rigid_bodies_meshes(
    rigid_bodies: Sequence[dict],
    data_directory: str = "",
    file_type: str = API.stl
    ) -> list:
    """Downloads the STL associated with each part inside the document.
    
    Returns:
        A list containing the names of each rigid body we want to render in the viusalizer
    """
    if data_directory != "" and not os.path.isdir(data_directory):
        os.mkdir(data_directory)
    rigid_bodies_seen = set()
    mesh_names = []
    for rigid_body in rigid_bodies:
        rigid_body_data = rigid_body.element_dict
        if CommonAttributes.version in rigid_body_data:
            wvm = API.version
            wvmid = rigid_body_data[CommonAttributes.version]
        elif CommonAttributes.documentMicroversion in rigid_body_data:
            wvm = API.microversion
            wvmid = rigid_body_data[CommonAttributes.documentMicroversion]
        else:
            wvm = API.workspace
            wvmid = rigid_body_data[CommonAttributes.workspace]
        did = rigid_body_data[CommonAttributes.documentId]
        eid = rigid_body_data[CommonAttributes.elementId]
        mesh_filename = check_and_append_extension(
            "".join((rigid_body.name.split(" "))[:-2]).lower(),
            file_type
        )
        mesh_path = os.path.join(data_directory, mesh_filename)
        # Check if it's a part or if it's a assembly
        if PartAttributes.partId in rigid_body_data:
            rigid_body_id = rigid_body_data[PartAttributes.partId]
            rigid_body_hash = join_api_url(did, eid, rigid_body_id)
            if rigid_body_hash in rigid_bodies_seen:
                continue
            rigid_bodies_seen.add(rigid_body_hash)
            rigid_body_mesh = onshape_client.part_stl_pipeline(
                did=did, wvm=wvm, wvmid=wvmid, eid=eid, part_id=rigid_body_id, filename=mesh_path,
            )
        else:
            rigid_body_hash = join_api_url(did, eid)
            if rigid_body_hash in rigid_bodies_seen:
                continue
            rigid_bodies_seen.add(rigid_body_hash)
            rigid_body_mesh = onshape_client.assembly_stl_pipeline(
                did=did,
                wvm=wvm,
                wvmid=wvmid,
                eid=eid,
                meshname=mesh_filename,
                filename=mesh_path,
            )
        mesh_names.append(mesh_filename)
    return mesh_names


def create_onshape_tree(
    did: str,
    wvmid: str,
    eid: str,
    wvm: str,
    robot_name: Optional[str] = None
    ) -> OnshapeTreeNode:
    if robot_name is None:
        robot_name = onshape_client.get_document(did=did)[CommonAttributes.name]
    json_data = onshape_client.assembly_definition(
        did=did,
        wvmid=wvmid,
        eid=eid,
        wvm=wvm,
        )
    return build_tree(json_data, robot_name=robot_name)


def main():
    # TODO: add this credentials things (client = Client(creds=""))
    # did = "6041e7103bb40af449a81618"
    # wvmid = "7e51d7b6b381bd79481e2033"
    # eid = "aad7f639435879b7135dce0f"
    # wvm = "v"
    # did = "9e58c2c2298902a0b2526461"
    # wvmid = "10c0fc2dbd8f4f1d0e448548"
    # eid = "5048884906d62c21e634d119"
    # d2b65b007cccdccd672c9efe/v/d5207597cf0d4de2d51a2350/e/d64d0511810bd7d9d742d1bb
    did = "d2b65b007cccdccd672c9efe"
    wvmid = "13393916865ef21e14c7564a"
    eid = "d64d0511810bd7d9d742d1bb"
    # did = "6041e7103bb40af449a81618"
    # wvmid = "f6f89c195eec60b2e5c8a73e"
    # eid = "aad7f639435879b7135dce0f"
    wvm = "v"
    test = create_onshape_tree(did=did, wvm=wvm, wvmid=wvmid, eid=eid)
    test.print_transforms()
    test.print_children()
    print(test.joint_parents)
    test.print_mass_properties()


if __name__ == "__main__":
    main()