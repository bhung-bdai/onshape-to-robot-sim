#!/usr/bin/env python3
from __future__ import annotations
import json

from collections import deque
from dataclasses import dataclass, asdict
from enum import Enum
from typing import Any, Optional, Sequence, TypeAlias

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
class PartAttributes(CommonAttributes):
    partId: str = "partId"
    bodyType: str = "bodyType"


@dataclass
class AssemblyAttributes(CommonAttributes):
    name: str = "name"
    suppressed: str = "suppressed"
    idNum: str = "id"


@dataclass
class APIElements():
    instances: str = "instances"
    subAssemblies: str = "subAssemblies"


class OnshapeTreeNode():
    def __init__(self, element_dict: Optional[dict] = None, depth: int = 0):
        self.element_dict = element_dict
        self.children = []
        self.depth = depth

    def add_child(self, node: OnshapeTreeNode) -> None:
        self.children.append(node)

    def print_element_ids(self):
        print(self.element_dict[CommonAttributes.elementId])
        for child in self.children:
            child.print_element_ids()

    def print_names(self):
        print(f"{self.name}, depth: {self.depth}")
        for child in self.children:
            child.print_names()

    @property
    def name(self):
        return self.element_dict[CommonAttributes.name]


# Should we sort this by elementId?
def find_element_in_subassemblies(element_id: str, document_subassemblies: list) -> Optional[dict]:
    for element in document_subassemblies:
        if element[CommonAttributes.elementId] == element_id:
            return element
    return None


def build_tree(root_dict: list, root_subassemblies: list = []) -> OnshapeTreeNode:
    root_node = OnshapeTreeNode(root_dict)
    build_tree_helper(root_node, root_dict, root_subassemblies)
    return root_node


# document_subassemblies should exist somewhere it can be accessed
def build_tree_helper(node: OnshapeTreeNode, element_dict: dict, document_subassemblies: list) -> None:
    stack = deque()
    stack.append(element_dict)
    depth = 0
    while len(stack) > 0:
        next_element = stack.pop()
        depth += 1
        for instance in next_element[APIElements.instances]:
            # Create a child node
            child_node = OnshapeTreeNode(instance, depth)

            # Base case: we hit a part
            if instance[CommonAttributes.elementType] == ElementAttributes.part:
                node.add_child(child_node)
                continue
            depth += 1
            # Recursive case: we hit a subassembly
            # TODO I dont think this is right
            child_id = instance[CommonAttributes.elementId]
            child_element = find_element_in_subassemblies(child_id, document_subassemblies)
            stack.append(child_element)
            node.add_child(child_node)
        depth -= 1



json_string = """{
  "rootAssembly": {
    "occurrences": [
      {
        "hidden": false,
        "fixed": false,
        "transform": [
          1,
          0,
          0,
          0.107,
          0,
          1,
          0,
          0,
          0,
          0,
          1,
          -3.469446951953614e-18,
          0,
          0,
          0,
          1
        ],
        "path": [
          "MmRHXBai4kux8tPcZ"
        ]
      },
      {
        "hidden": false,
        "fixed": false,
        "transform": [
          1,
          0,
          0,
          0.08927692583203317,
          0,
          1,
          0,
          0.0741149203106761,
          0,
          0,
          1,
          0.06335652424022555,
          0,
          0,
          0,
          1
        ],
        "path": [
          "MrWVPT9IK41t//ORF",
          "MjXp5OEcWIwYLGGrG"
        ]
      },
      {
        "hidden": false,
        "fixed": true,
        "transform": [
          1,
          0,
          0,
          0,
          0,
          1,
          0,
          0,
          0,
          0,
          1,
          0,
          0,
          0,
          0,
          1
        ],
        "path": [
          "ME0OGHafV27m4erd3"
        ]
      },
      {
        "hidden": false,
        "fixed": false,
        "transform": [
          1,
          0,
          0,
          0.004736018538475037,
          0,
          1,
          0,
          0.03841717142611742,
          0,
          0,
          1,
          0.09923682259395718,
          0,
          0,
          0,
          1
        ],
        "path": [
          "MrWVPT9IK41t//ORF",
          "MmXPaG80Mq0OnEMRb"
        ]
      },
      {
        "hidden": false,
        "fixed": false,
        "transform": [
          1,
          0,
          0,
          0,
          0,
          1,
          0,
          0,
          0,
          0,
          1,
          0,
          0,
          0,
          0,
          1
        ],
        "path": [
          "MfnXxatwJGOcsLj0q"
        ]
      },
      {
        "hidden": false,
        "fixed": false,
        "transform": [
          1,
          0,
          0,
          0.025381017476320267,
          0,
          1,
          0,
          0.06465646903961897,
          0,
          0,
          1,
          0.07801759289577603,
          0,
          0,
          0,
          1
        ],
        "path": [
          "MrWVPT9IK41t//ORF"
        ]
      }
    ],
    "instances": [
      {
        "name": "Body <1>",
        "suppressed": false,
        "id": "ME0OGHafV27m4erd3",
        "type": "Part",
        "isStandardContent": false,
        "partId": "JHD",
        "fullConfiguration": "default",
        "configuration": "default",
        "documentMicroversion": "4a07df152aba423b55fded1f",
        "documentId": "6041e7103bb40af449a81618",
        "elementId": "7a12328807be40cb1472cc52"
      },
      {
        "name": "Wheel <1>",
        "suppressed": false,
        "id": "MfnXxatwJGOcsLj0q",
        "type": "Part",
        "isStandardContent": false,
        "partId": "JYD",
        "fullConfiguration": "default",
        "configuration": "default",
        "documentMicroversion": "4a07df152aba423b55fded1f",
        "documentId": "6041e7103bb40af449a81618",
        "elementId": "7a12328807be40cb1472cc52"
      },
      {
        "name": "Wheel <2>",
        "suppressed": false,
        "id": "MmRHXBai4kux8tPcZ",
        "type": "Part",
        "isStandardContent": false,
        "partId": "JYD",
        "fullConfiguration": "default",
        "configuration": "default",
        "documentMicroversion": "4a07df152aba423b55fded1f",
        "documentId": "6041e7103bb40af449a81618",
        "elementId": "7a12328807be40cb1472cc52"
      },
      {
        "name": "Assembly 1 <1>",
        "suppressed": false,
        "id": "MrWVPT9IK41t//ORF",
        "type": "Assembly",
        "fullConfiguration": "default",
        "configuration": "default",
        "documentMicroversion": "4a07df152aba423b55fded1f",
        "documentId": "6041e7103bb40af449a81618",
        "elementId": "e252e049abc5c4abd6bfe390"
      }
    ],
    "patterns": [],
    "fullConfiguration": "default",
    "configuration": "default",
    "documentMicroversion": "4a07df152aba423b55fded1f",
    "documentId": "6041e7103bb40af449a81618",
    "elementId": "aad7f639435879b7135dce0f"
  },
  "subAssemblies": [
    {
      "instances": [
        {
          "name": "Wheel <3>",
          "suppressed": false,
          "id": "MmXPaG80Mq0OnEMRb",
          "type": "Part",
          "isStandardContent": false,
          "partId": "JYD",
          "fullConfiguration": "default",
          "configuration": "default",
          "documentMicroversion": "4a07df152aba423b55fded1f",
          "documentId": "6041e7103bb40af449a81618",
          "elementId": "7a12328807be40cb1472cc52"
        },
        {
          "name": "Wheel <4>",
          "suppressed": false,
          "id": "MjXp5OEcWIwYLGGrG",
          "type": "Part",
          "isStandardContent": false,
          "partId": "JYD",
          "fullConfiguration": "default",
          "configuration": "default",
          "documentMicroversion": "4a07df152aba423b55fded1f",
          "documentId": "6041e7103bb40af449a81618",
          "elementId": "7a12328807be40cb1472cc52"
        }
      ],
      "patterns": [],
      "fullConfiguration": "default",
      "configuration": "default",
      "documentMicroversion": "4a07df152aba423b55fded1f",
      "documentId": "6041e7103bb40af449a81618",
      "elementId": "e252e049abc5c4abd6bfe390"
    }
  ],
  "parts": [
    {
      "isStandardContent": false,
      "partId": "JYD",
      "bodyType": "solid",
      "fullConfiguration": "default",
      "configuration": "default",
      "documentMicroversion": "4a07df152aba423b55fded1f",
      "documentId": "6041e7103bb40af449a81618",
      "elementId": "7a12328807be40cb1472cc52"
    },
    {
      "isStandardContent": false,
      "partId": "JHD",
      "bodyType": "solid",
      "fullConfiguration": "default",
      "configuration": "default",
      "documentMicroversion": "4a07df152aba423b55fded1f",
      "documentId": "6041e7103bb40af449a81618",
      "elementId": "7a12328807be40cb1472cc52"
    }
  ],
  "partStudioFeatures": []
}
"""


def main():
    parse_json = json.loads(json_string)
    root_dict = parse_json["rootAssembly"]
    del root_dict["occurrences"]
    root_dict["name"] = "root"
    root_subassemblies = parse_json[APIElements.subAssemblies]
    test = build_tree(root_dict, root_subassemblies)
    # OnshapeTreeNode.print_tree_elements(test)
    test.print_element_ids()
    test.print_names()


if __name__ == "__main__":
    main()