#!/usr/bin/env python3

from __future__ import annotations
from collections import deque
from dataclasses import dataclass, asdict
from enum import Enum
import json
from typing import Any, Callable, Optional, Sequence, TypeAlias

import numpy as np
import numpy.typing as npt

from onshape_to_sim.utils import (
    express_mass_properties_in_world_frame
)


@dataclass
class ElementAttributes:
    part: str = "Part"
    assembly: str = "Assembly"


@dataclass
class CommonAttributes:
    name: str = "name"
    suppressed: str = "suppressed"
    idNum: str = "id"
    isStandardContent: str = "isStandardContent"
    fullConfiguration: str = "fullConfiguration"
    documentVersion: str = "documentVersion"
    configuration: str = "configuration"
    documentId: str = "documentId"
    elementId: str = "elementId"
    elementType: str = "type"
    documentMicroversion: str = "documentMicroversion"
    transform: str = "transform"


@dataclass
class FeatureAttributes():
    children: str = "children"
    is_parent: str = "is_parent"
    featureData: str = "featureData"
    mateType: str = "mateType"
    matedEntities: str = "matedEntities"
    matedOccurrence: str = "matedOccurrence"
    matedCS: str = "matedCS"
    origin: str = "origin"
    parent: str = "parent"
    xAxis: str = "xAxis"
    yAxis: str = "yAxis"
    zAxis: str = "zAxis"


@dataclass
class PartAttributes():
    partId: str = "partId"
    bodyType: str = "bodyType"


@dataclass
class OccurrenceAttributes():
    path: str = "path"
    hidden: str = "hidden"


@dataclass
class MassAttributes():
    centroid: str = "centroid"
    hasMass: str = "hasMass"
    inertia: str = "inertia"
    mass: str = "mass"
    volume: str = "volume"

@dataclass
class APIAttributes():
    features: str = "features"
    instances: str = "instances"
    occurrences: str = "occurrences"
    rootAssembly: str = "rootAssembly"
    subassemblies: str = "subAssemblies"


def get_element_tform_mate(mated_cs: dict) -> npt.ArrayLike:
    element_tform_mate = np.eye(4)
    element_tform_mate[:3, 0] = np.array(mated_cs[FeatureAttributes.xAxis])
    element_tform_mate[:3, 1] = np.array(mated_cs[FeatureAttributes.yAxis])
    element_tform_mate[:3, 2] = np.array(mated_cs[FeatureAttributes.zAxis])
    element_tform_mate[:3, 3] = mated_cs[FeatureAttributes.origin]
    return element_tform_mate


class OnshapeTreeNode():
    """A tree representing assemblies, subassemblies, and parts of an Onshape API request.

    The root of the tree is the root of the assembly. Children of each node are either subassemblies or parts.
    Leaves are guaranteed to be parts, while branches are guaranteed to be assemblies. The information each mate/joints
    if stored in every single instance which is inside that mate.
    """
    def __init__(
        self,
        depth: int = 0,
        element_dict: Optional[dict] = None,
        node_id: Optional[str] = None,
        name: Optional[str] = None,
        path: str = "",
        ):
        self.element_dict: Optional[dict] = element_dict
        self.node_id: Optional[str] = node_id
        self.name: Optional[str] = name
        self.children: list = []
        self.depth: int = depth
        self.path: str = path
        self.hidden: bool = False
        self.joint_info: Optional[dict] = None
        self.world_tform_element: npt.ArrayLike = np.eye(4)
        self.element_tform_mate: Optional[npt.ArrayLike] = None
        self.com_wrt_world = np.zeros((3,))
        self.inertia_wrt_world = np.zeros((3, 3))
        self.mass = 0.0
        self.has_mass = False
        self.volume = 0.0

    def __repr__(self):
        return f"{self.name}: {self.node_id} (depth {self.depth})"

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

    def print_joint_info(self):
        """Print nodes followed by their joint information"""
        print(f"{self}", end=": ")
        print(f"{self.joint_info}")
        for child in self.children:
            child.print_joint_info()

    def print_names(self):
        """Print nodes"""
        print(f"{self}")
        for child in self.children:
            child.print_names()

    def _initialize_node(
        self,
        occurrence_map: dict,
        joint_map: dict
        ) -> None:
        self._add_occurrence_info(occurrence_map)
        self._add_joint_info(joint_map)
    
    def _add_occurrence_info(self, occurrence_map: dict,) -> None:
        """Adds the information about the occurrence with the path and transform into the element.

        Args:
            occurrence_map: mapping of path (joined into a single string) to the occurrence
        """
        if self.path == "":
            return
        if self.path not in occurrence_map:
            raise ValueError(f"Instance {self.path} not in occurrences!")
        occurrence = occurrence_map[self.path]
        self.world_tform_element = np.array(occurrence[CommonAttributes.transform]).reshape(4, 4)
        self.hidden = bool(occurrence[OccurrenceAttributes.hidden])

    def _add_joint_info(self, joint_map: dict) -> None:
        """Get the mates associated with the node from the dictionary and store them here.

        Currently I think only parts can be done this way, so we only store joint information on a per-part basis.
        
        Args:
            joint_map: a mapping of occurrence ids and their feature information
        """
        if self.node_id is not None and self.node_id in joint_map:
            self.joint_info = joint_map[self.node_id]
            # self.element_tform_mate = get_element_tform_mate(self.joint_info)

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
            world_tform_element=self.world_tform_element,
            mass=mass_properties[MassAttributes.mass],
            com_in_element_frame=mass_properties[MassAttributes.centroid],
            inertia_in_element_frame=mass_properties[MassAttributes.inertia]
        )
        

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


def _add_instance_mass_properties(instances: list, mass_properties_map: dict) -> None:
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
        wmv = "m" # TODO: Check if document microversions are a consistent thing across all subassemblies
        wmvid = instance[CommonAttributes.documentMicroversion]
        part_id = None
        if PartAttributes.partId in instance:
            part_id = instance[PartAttributes.partId]
        # TODO: implement this function to grab mass properties and checks if it's a part or an assembly
        response = onshape_client.mass_properties(did=did, eid=eid, wmv=wmv, wmvid=wmvid, part_id=part_id)
        # Extract the relevant mass properies and put them into a dictionary for easy lookup later
        mass_properties = _extract_mass_properties(response)
        mass_properties_map[instance_id] = mass_properties


def _build_mass_properties_map(instances: list, subassemblies: list) -> dict:
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
    _add_instance_mass_properties(instances, mass_properties_map)
    for subassembly in subassemblies:
        # Add all of the instances from the subassemblies into the mass properties map
        _add_instance_mass_properties(subassemblies[APIAttributes.instances])
    return mass_properties_map


def _build_features_map(features: list) -> dict:
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
    for feature in features:
        mated_entities = feature[FeatureAttributes.featureData][FeatureAttributes.matedEntities]
        mate_type = feature[FeatureAttributes.featureData][FeatureAttributes.mateType]
        # TODO @bhung figure out if the assumption that the parent is the final entity is true
        # Loop through the n - 1 children and added them
        parent_entity = mated_entities[-1]
        parent_path = "".join(parent_entity[FeatureAttributes.matedOccurrence])
        parent_info = {
            FeatureAttributes.children: [],
            FeatureAttributes.is_parent: True,
            FeatureAttributes.mateType: mate_type
        }
        for i in range(len(mated_entities) - 1):
            # Initialize the child information
            child_info = {
                FeatureAttributes.parent: parent_path,
                FeatureAttributes.is_parent: False,
                FeatureAttributes.mateType: mate_type
            }
            entity = mated_entities[i]
            child_path = "".join(entity[FeatureAttributes.matedOccurrence])
            child_info[CommonAttributes.transform] = get_element_tform_mate(entity[FeatureAttributes.matedCS])
            # Check and add the information into the feature map
            if child_path in features_map:
                features_map[child_path].append(child_info)
            else:
                features_map[child_path] = [child_info]
            # Add the child to the list of information kept by the parent
            parent_info[FeatureAttributes.children].append(child_path)
        # Extract the transform from the parent
        parent_info[CommonAttributes.transform] = get_element_tform_mate(parent_entity[FeatureAttributes.matedCS])
        if parent_path in features_map:
            features_map[parent_path].append(parent_info)
        else:
            features_map[parent_path] = [parent_info]
    return features_map


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
        

def build_tree(json_assembly_data: dict) -> OnshapeTreeNode:
    """Given a JSON Onshape API call for the elements in an assembly, return a tree representing the entire assembly.
    
    Args:
        json_assembly_data: the json returned by a call to the Onshape API

    Returns:
        The root of the Onshape tree
    """
    root_dict = json_assembly_data[APIAttributes.rootAssembly]
    # TODO see if this is necessary later
    root_dict[CommonAttributes.name] = "root"
    root_subassemblies = _build_subassemblies_map(json_assembly_data[APIAttributes.subassemblies])
    root_mates = _build_features_map(root_dict[APIAttributes.features])
    root_occurrences = _build_occurrences_map(root_dict[APIAttributes.occurrences])
    root_node = OnshapeTreeNode(element_dict=root_dict)
    root_node.name = "root"
    build_tree_helper(root_node, root_subassemblies, root_mates, root_occurrences)
    return root_node


def build_tree_helper(
    root: OnshapeTreeNode,
    document_subassemblies: dict,
    document_mates: dict,
    document_occurrences: dict
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
    node = root
    while len(stack) > 0:
        next_node = stack.pop()
        next_element = next_node.element_dict
        # From the document holding the information about mates, add it in
        next_node._initialize_node(document_occurrences, document_mates)
        # next_node._add_mass_properties(document_mass_properties)
        # Iterate through the elements in the API instances 
        for instance in next_element[APIAttributes.instances]:
            # Create a child node
            occurrence_id = instance[CommonAttributes.idNum]
            child_node = OnshapeTreeNode(
                depth=next_node.depth+1,
                element_dict=instance,
                node_id=occurrence_id,
                name=instance[CommonAttributes.name],
                path=next_node.path+occurrence_id
                )
            child_node._initialize_node(document_occurrences, document_mates)

            # Base case: we hit a part. Add the child to the node and skip adding it to the queue
            if instance[CommonAttributes.elementType] == ElementAttributes.part:
                next_node.add_child(child_node)
                print(f"Part: {child_node.path}")
                continue

            # Recursive case: we hit a subassembly. Add it to the top of the stack with its subassembly data
            child_id = instance[CommonAttributes.elementId]
            child_node.element_dict = document_subassemblies[child_id]
            stack.append(child_node)
            print(f"Assem: {child_node.path}")
            next_node.add_child(child_node)


def main():
    with open("../test/data/multi_features_sub_assembly.txt", "r") as fi:
        json_data = json.load(fi)
    test = build_tree(json_data)
    test.print_names()
    test.print_children()
    test.print_joint_info()
    test.print_transforms()


if __name__ == "__main__":
    main()