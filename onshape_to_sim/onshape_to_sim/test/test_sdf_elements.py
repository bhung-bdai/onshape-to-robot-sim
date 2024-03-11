#!/usr/bin/env python3
# Copyright (c) 2024 Boston Dynamics AI Institute LLC. All rights reserved.
"""Tests the formation of the SDF elements"""
import numpy as np

from sdf.sdf_elements import (
    Attribute,
    Element,
    Formatter,
    add_attribute,
    add_unbuilt_element,
    axis,
    build_attribute,
    build_element,
    pose
)

def test_build_attribute() -> None:
    string_name = "test"
    string_format = Formatter.strings()
    string_data = "updog"
    string_attr_output = build_attribute(string_name, string_format, string_data)
    string_output = "test=\"updog\""
    assert string_output == string_attr_output

    bool_name = "test"
    bool_format = Formatter.bools()
    bool_data = False
    bool_attr_output = build_attribute(bool_name, bool_format, bool_data)
    bool_output = "test=false"
    assert bool_output == bool_attr_output

    float_name = "test"
    float_format = Formatter.floats(5)
    float_data = np.arange(5)
    float_attr_output = build_attribute(float_name, float_format, tuple(float_data))
    float_output = "test=0 1 2 3 4"
    assert float_output == float_attr_output

def test_add_attribute() -> None:
    attr_list = []
    string_name = "test"
    string_format = Formatter.strings()
    string_data = "updog"
    string_output = "test=\"updog\""
    add_attribute(attr_list, string_name, string_format, string_data)
    assert string_output in attr_list

    bool_name = "test"
    bool_format = Formatter.bools()
    bool_data = False
    bool_output = "test=false"
    add_attribute(attr_list, bool_name, bool_format, bool_data)
    assert bool_output in attr_list

    float_name = "test"
    float_format = Formatter.floats(5)
    float_data = np.arange(5)
    float_output = "test=0 1 2 3 4"
    add_attribute(attr_list, float_name, float_format, tuple(float_data))
    assert float_output in attr_list


def test_build_element() -> None:
    element_list = []
    attr_list = []
    string_name = "string"
    string_format = Formatter.strings()
    string_data = "string"
    add_attribute(attr_list, string_name, string_format, string_data)

    bool_name = "bool"
    bool_format = Formatter.bools()
    bool_data = False
    add_attribute(attr_list, bool_name, bool_format, bool_data)

    float_name = "float"
    float_format = Formatter.floats(1)
    float_data = 0.0
    add_attribute(attr_list, float_name, float_format, float_data)

    sub_element_name = "sub"
    sub_element_format = Formatter.empty()
    sub_element_data = None
    add_unbuilt_element(element_list, sub_element_name, sub_element_format, sub_element_data)

    element_name = "test"
    element_format = Formatter.strings()
    element_data = "updog"

    element = build_element(element_name, element_format, element_data, attr_list, element_list)
    real_element = "<test string=\"string\" bool=false float=0>\n\"updog\"<sub>\n</sub></test>\n"
    assert repr(real_element) == repr(element)


