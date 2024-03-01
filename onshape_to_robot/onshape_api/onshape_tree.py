#!/usr/bin/env python3

#TODO figure out if the find by ID is good enough
from __future__ import annotations
import json

from collections import deque
from dataclasses import dataclass, asdict
from enum import Enum
from typing import Any, Callable, Optional, Sequence, TypeAlias

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
class FeatureAttributes(CommonAttributes):
    featureData: str = "featureData"
    mateType: str = "mateType"
    matedEntities: str = "matedEntities"
    matedOccurrence: str = "matedOccurrence"


@dataclass
class PartAttributes(CommonAttributes):
    partId: str = "partId"
    bodyType: str = "bodyType"


@dataclass
class APIElements():
    instances: str = "instances"
    subassemblies: str = "subAssemblies"
    features: str = "features"


class OnshapeTreeNode():
    def __init__(
        self,
        element_dict: Optional[dict] = None,
        node_id: Optional[str] = None,
        name: Optional[str] = None,
        depth: int = 0
        ):
        self.element_dict = element_dict
        self.node_id = node_id
        self.name = name
        self.children = []
        self.depth = depth
        self.joint_info = None

    def __repr__(self):
        return f"{self.name}: {self.node_id} (depth {self.depth})"

    def add_child(self, node: OnshapeTreeNode) -> None:
        self.children.append(node)

    def print_children(self):
        print(f"{self}", end=": ")
        print(f"{self.children}")
        for child in self.children:
            child.print_children()

    def print_element_ids(self):
        print(f"{self}", end=": ")
        print(f"{self.element_dict[CommonAttributes.elementId]}")
        for child in self.children:
            child.print_element_ids()

    def print_joint_info(self):
        print(f"{self}", end=": ")
        print(f"{self.joint_info}")
        for child in self.children:
            child.print_joint_info()

    def print_names(self):
        print(f"{self}")
        for child in self.children:
            child.print_names()
    
    def _add_joint_info(self, joint_map: dict) -> None:
        """Get the mates associated with the node from the dictionary and store them here."""
        if self.node_id is not None and self.node_id in joint_map:
            self.joint_info = joint_map[self.node_id]
            print(self.joint_info)


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
    """Constructs a map of occurence ids and mate data"""
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


def _add_joint_info(node: OnshapeTreeNode, mates: dict) -> None:
    # Checks if they have an existing mate
    if not parent.node_id in mates and not child.node_id in mates:
        return
        

def build_tree(json_assembly_data: dict) -> OnshapeTreeNode:
    """Given a JSON Onshape API call for the elements in an assembly, return a tree representing the entire assembly"""
    root_dict = json_assembly_data["rootAssembly"]
    # TODO see if this is necessary later
    del root_dict["occurrences"]
    root_dict[CommonAttributes.name] = "root"
    root_subassemblies = _build_subassemblies_map(json_assembly_data[APIElements.subassemblies])
    root_mates = _build_features_map(root_dict[APIElements.features])
    root_node = OnshapeTreeNode(root_dict)
    root_node.name = "root"
    build_tree_helper(root_node, root_subassemblies, root_mates)
    return root_node


# document_subassemblies should exist somewhere it can be accessed
def build_tree_helper(root: OnshapeTreeNode, document_subassemblies: dict, document_mates: dict) -> None:
    stack = deque()
    stack.append(root)
    depth = 0
    node = root
    while len(stack) > 0:
        next_node = stack.pop()
        next_element = next_node.element_dict
        # From the document holding the information about mates, add it in
        next_node._add_joint_info(document_mates)
        
        # Iterate through the elements in the API instances 
        for instance in next_element[APIElements.instances]:
            # Create a child node
            child_node = OnshapeTreeNode(instance, node_id=instance[CommonAttributes.idNum], name=instance[CommonAttributes.name], depth=next_node.depth+1)
            child_node._add_joint_info(document_mates)

            # Base case: we hit a part. Add the child to the node and skip adding it to the queue
            if instance[CommonAttributes.elementType] == ElementAttributes.part:
                next_node.add_child(child_node)
                continue

            # Recursive case: we hit a subassembly. Add it to the top of the stack with its subassembly data
            child_id = instance[CommonAttributes.elementId]
            child_node.element_dict = document_subassemblies[child_id]
            stack.append(child_node)
            next_node.add_child(child_node)


def main():
    with open("../test/data/multi_features_sub_assembly.txt", "r") as fi:
        json_data = json.load(fi)
    test = build_tree(json_data)
    test.print_names()
    test.print_children()
    test.print_joint_info()


if __name__ == "__main__":
    main()