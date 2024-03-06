#!/usr/bin/env python3

#TODO figure out if the find by ID is good enough
from __future__ import annotations
from collections import deque
from dataclasses import dataclass, asdict
from enum import Enum
import json
from typing import Any, Callable, Optional, Sequence, TypeAlias

import numpy as np
import numpy.typing as npt


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


@dataclass
class FeatureAttributes():
    featureData: str = "featureData"
    mateType: str = "mateType"
    matedEntities: str = "matedEntities"
    matedOccurrence: str = "matedOccurrence"
    matedCS: str = "matedCS"
    xAxis: str = "xAxis"
    yAxis: str = "yAxis"
    zAxis: str = "zAxis"
    origin: str = "origin"


@dataclass
class PartAttributes():
    partId: str = "partId"
    bodyType: str = "bodyType"


@dataclass
class OccurrenceAttributes():
    path: str = "path"
    transform: str = "transform"
    hidden: str = "hidden"


@dataclass
class APIAttributes():
    features: str = "features"
    instances: str = "instances"
    occurrences: str = "occurrences"
    rootAssembly: str = "rootAssembly"
    subassemblies: str = "subAssemblies"


def get_part_tform_mate(joint_info: dict) -> npt.ArrayLike:
    mated_cs = joint_info[FeatureAttributes.matedCS]
    part_tform_mate = np.eye(4)
    part_tform_mate[:3, 0] = np.array(mated_cs[FeatureAttributes.xAxis])
    part_tform_mate[:3, 1] = np.array(mated_cs[FeatureAttributes.yAxis])
    part_tform_mate[:3, 2] = np.array(mated_cs[FeatureAttributes.zAxis])
    part_tform_mate[:3, 3] = mated_cs[FeatureAttributes.origin]
    return part_tform_mate


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
        self.element_dict = element_dict
        self.node_id = node_id
        self.name = name
        self.children = []
        self.depth = depth
        self.path = path
        self.hidden = False
        self.joint_info = None
        self.world_tform_element = np.eye(4)

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
        print(f"{self.pose}")
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
        joint_map: dict,
        ) -> None:
        self._add_occurrence_info(occurrence_map)
        self._add_joint_info(joint_map)
    
    def _add_occurrence_info(self, occurrence_map: dict) -> None:
        """

        Args:
            occurrence_map: mapping of path (joined into a single string) to the occurrence
        """
        if self.path == "":
            return
        if self.path not in occurrence_map:
            raise ValueError(f"Instance {self.path} not in occurrences!")
        occurrence = occurrence_map[self.path]
        self.world_tform_element = np.array(occurrence[OccurrenceAttributes.transform]).reshape(4, 4)
        self.hidden = bool(occurrence[OccurrenceAttributes.hidden])

    def _add_joint_info(self, joint_map: dict) -> None:
        """Get the mates associated with the node from the dictionary and store them here.
        
        Args:
            joint_map: a mapping of occurrence ids and their feature information
        """
        if self.node_id is not None and self.node_id in joint_map:
            self.joint_info = joint_map[self.node_id]
        

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


def _build_features_map(features: list) -> dict:
    """Constructs a map of occurrence ids and mate data.

    Mapping occurrence ids to the feature data of the mate. This is because mates occur between instances of objects,
    not elements.

    Args:
        features: the features information returned in the OnShape API Call

    Returns:
        A mapping of occurrence ids to mates
    """
    features_map = {}
    for feature in features:
        feature_data = feature[FeatureAttributes.featureData]
        for entity in feature_data[FeatureAttributes.matedEntities]:
            # If it's inside the map, append it. Otherwise, store it as a list of features associated with the ID
            # TODO @bhung: Check if matedOccurence ever actually has more than one number
            for occurrence in entity[FeatureAttributes.matedOccurrence]:
                if occurrence in features_map:
                    features_map[occurrence].append(feature_data)
                else:
                    features_map[occurrence] = [feature_data]
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
    print(json_assembly_data)
    root_subassemblies = _build_subassemblies_map(json_assembly_data[APIAttributes.subassemblies])
    root_mates = _build_features_map(root_dict[APIAttributes.features])
    root_occurrences = _build_occurrences_map(root_dict[APIAttributes.occurrences])
    print(root_occurrences)
    root_node = OnshapeTreeNode(element_dict=root_dict)
    root_node.name = "root"
    # print(root_node)
    build_tree_helper(root_node, root_subassemblies, root_mates, root_occurrences)
    return root_node


# document_subassemblies should exist somewhere it can be accessed
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
    current_path = ""
    path_end = 0
    # print(root.element_dict)
    while len(stack) > 0:
        next_node = stack.pop()
        next_element = next_node.element_dict
        # From the document holding the information about mates, add it in
        next_node._add_joint_info(document_mates)
        next_node._add_occurrence_info(document_occurrences)
        
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
            child_node._add_joint_info(document_mates)
            child_node._add_occurrence_info(document_occurrences)

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
    with open("../test/data/no_mates.txt", "r") as fi:
        json_data = json.load(fi)
    test = build_tree(json_data)
    test.print_names()
    test.print_children()
    test.print_joint_info()
    test.print_transforms()


if __name__ == "__main__":
    main()