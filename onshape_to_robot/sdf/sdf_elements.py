#!/usr/bin/env python3
# Copyright (c) 2024 Boston Dynamics AI Institute LLC. All rights reserved.
"""Implements SDF elements based on the SDFormat 1.11.

Any used elements which contain more than a single data value should have a function that creates that element.
These 'complex elements' (as I've deemed them) should be passed as fully built elements to other elements
that contain them, instead of being built inside the higher level element. In essence, elements should only have 
a depth of 1 in terms of how far down they should be making new elements. Any element containing other elements 
with a depth greater than 1 should have their own specific functions to create them. 

Attribute and Element are TypeAliases of strings. This is because both SDF fields are implemented as blocks of strings
under the hood, but the user needs to understand the difference between them to properly parse them. 

An instance of an Element is a string that represents a fully formed SDF element. An instance of an Attribute is a 
string that represents a fully formed SDF attribute.

TODO(@bhung): add docstrings for everything
"""
from dataclasses import dataclass, asdict
from typing import Any, Optional, Sequence, TypeAlias

import numpy as np
import numpy.typing as npt

Attribute: TypeAlias = str
Element: TypeAlias = str

@dataclass
class Attributes:
    """Dataclass for keeping track of a SDF attribute."""
    attached_to: str = "attached_to"
    auto: str = "auto"
    axis: str = "axis"
    default: str = "default"
    degrees: str = "degrees"
    density: str = "density"
    elem_type: str = "type"
    enabled: str = "enabled"
    expressed_in: str = "expressed_in"
    filename: str = "filename"
    item_type: str = "type"
    joint: str = "joint"
    mass: str = "mass"
    merge: str = "merge"
    name: str = "name"
    placement_frame: str = "placement_frame"
    relative_to: str = "relative_to"
    rotation_format: str = "rotation_format"
    tension: str = "tension"
    uv_set: str = "uv_set"
    version: str = "version"
    world_name: str = "world_name"


@dataclass
class Elements:
    """Dataclass to keep track of useful SDF elements. Not comprehensive"""
    always_on: str = "always_on"
    ambient: str = "ambient"
    child: str = "child"
    damping: str = "damping"
    density: str = "density"
    diffuse: str = "diffuse"
    dissipation: str = "dissipation"
    effort: str = "effort"
    emissive: str = "emissive"
    empty: str = "empty"
    force_torque: str = "force_torque"
    friction: str = "friction"
    gearbox_ratio: str = "gearbox_ratio"
    geometry: str = "geometry"
    imu: str = "imu"
    inertia: str = "inertia"
    inertial: str = "inertial"
    ixx: str = "ixx"
    ixy: str = "ixy"
    ixz: str = "ixz"
    iyy: str = "iyy"
    iyz: str = "iyz"
    izz: str = "izz"
    joint: str = "joint"
    limit: str = "limit"
    lower: str = "lower"
    mass: str = "mass"
    material: str = "material"
    mesh: str = "mesh"
    parent: str = "parent"
    pose: str = "pose"
    specular: str = "specular"
    spring_reference: str = "spring_reference"
    spring_stiffness: str = "spring_stiffness"
    stiffness: str = "stiffness"
    topic: str = "topic"
    update_rate: str = "update_rate"
    upper: str = "upper"
    uri: str = "uri"
    velocity: str = "velocity"
    xyz: str = "xyz"


class Formatter:
    @staticmethod
    def floats(num_floats: int):
        return ("%.20g " * num_floats).strip()

    @staticmethod
    def strings():
        return "\"%s\""

    @staticmethod
    def bools():
        return "%s"

    @staticmethod
    def empty():
        return ""

    @staticmethod
    def elements(format_string: str):
        return format_string + "%s"


def _combine_attributes(
    attr_list: list[str],
    delimiter: str = " "
    ) -> str:
    """Combines the attributes in the attribute list, separated by a space"""
    return delimiter.join(attr_list)


def _wrap_ends(
    start_tag: str,
    body_string: str,
    end_tag: str,
    ) -> str:
    """Wraps the ends of the a string with the start and end tags"""
    return f"{start_tag}{body_string}{end_tag}"


def _element_start(body_string: str) -> str:
    """Wraps the start tag in XML brackets"""
    return _wrap_ends("<", body_string, ">\n")


def _element_end(body_string: str) -> str:
    """Wraps the end tag in XML brackets"""
    return _wrap_ends("</", body_string, ">\n")


def build_attribute(
    attr_name: str,
    attr_format: str,
    attr_data: Any,
    ) -> Attribute:
    """Build an attribute for an element"""
    if isinstance(attr_data, str):
        attr_data = (attr_data,)
    elif isinstance(attr_data, bool):
        attr_data = (f"{attr_data}".lower(),)
    elif isinstance(attr_data, float):
        attr_data = (attr_data,)
    return (attr_name + "=" + attr_format) % attr_data


def build_element(
    element_name: str,
    element_format: str,
    element_data: Optional[Any] = None,
    element_attributes_list: list[str] = [],
    element_fields_list: list[Element] = [],
    ) -> Element:
    """Build an element with the proper formatting.

    Args:
        element_name: Name of the attribute we are adding
        element_format: How the data is formatted 
        element_data: Data encapsulated as part of the elment
        element_fields_list: List of fields inside an element 

    Return:
        The element created for the SDF.
    """ 
    element_attributes = _combine_attributes(element_attributes_list)
    # Remove extra spaces
    element_name = element_name.strip()
    # Generate the start and end tags
    start_element = _element_start((element_name + " " + element_attributes).strip())
    end_element = _element_end(element_name)
    # Save the data included with this elements and parse the contained elements
    element_fields_string = _combine_attributes(element_fields_list, delimiter="")
    element_fields = (element_fields_string,)
    if element_data is not None:
        if isinstance(element_data, str):
            element_data = (element_data,)
        elif isinstance(element_data, bool):
            element_data = ((element_format % element_data).lower(),)
        elif isinstance(element_data, float):
            element_data = (element_data,)
        element_fields = element_data + element_fields
    # Format the body of the element properly
    element_body = (Formatter.elements(element_format) % element_fields).strip()
    return _wrap_ends(start_element, element_body, end_element)


def add_attribute(
    attr_list: list[Attribute],
    attr_name: str,
    attr_format: str,
    attr_data: Any,
    ) -> None:
    attr_list.append(build_attribute(attr_name, attr_format, attr_data))


def add_unbuilt_element(
    field_list: list[str],
    element_name: str,
    element_format: str,
    element_data: Optional[Any] = None,
    element_attributes_list: list[Attribute] = [],
    element_fields_list: list[Element] = [],
    ) -> None:
    """Formats element data and appends it to list appropriately.
    
    Args:
        TODO(@bhung) write this down
    """
    if element_data is None and element_format != Formatter.empty():
        raise ValueError("Must be formatted as empty to provide no element data!")

    field_list.append(
        build_element(element_name, element_format, element_data, element_attributes_list, element_fields_list)
    )


def append_optional_elements(
    field_list: list[Element],
    element_list: Optional[list[Element]],
    ) -> None:
    """Append a fully built element to the field list.

    This function makes it obvious when we have an existing element to append vs one we need to build from scratch.
    """
    if element_list is None:
        return
    for element in element_list:
        field_list.append(element)


def xyz(
    actuation_axis: npt.ArrayLike,
    reference_frame: Optional[str] = None
    ) -> Element:
    attr_list = []
    if reference_frame is not None:
        add_attribute(attr_list, Attributes.expressed_in, Formatter.strings(), reference_frame)

    return build_element(
        Elements.xyz,
        Formatter.floats(3),
        tuple(actuation_axis),
        element_attributes_list=attr_list,
    )


def axis(
    actuation_axis: Element,
    optional_elements: Optional[list[Element]] = None,
    ) -> Element:
    field_list = []
    field_list.append(actuation_axis)
    append_optional_elements(field_list, optional_elements)


def dynamics(
    spring_reference: float = 0.0,
    spring_stiffness: Optional[float] = None,
    damping: Optional[float] = None,
    friction: Optional[float] = None,
    ) -> Element:
    float_format = Formatter.floats(1)
    field_list = []

    add_unbuilt_element(field_list, Elements.spring_reference, float_format, spring_reference)
    if spring_stiffness is not None:
        add_unbuilt_element(field_list, Elements.spring_stiffness, float_format, spring_stiffness)
    if damping is not None:
        add_unbuilt_element(field_list, Elements.damping, float_format, damping)
    if friction is not None:
        add_unbuilt_element(field_list, Elements.friction, float_format, friction)

    return build_element(
        Elements.dynamics,
        Formatter.empty(),
        None,
        element_fields_list=field_list
    )


def limit(
    lower_limit: float,
    upper_limit: float,
    effort_limit: Optional[float] = None,
    velocity_limit: Optional[float] = None,
    joint_stop_stiffness: Optional[float] = None,
    joint_stop_dissipation: Optional[float] = None,
    ) -> Element:
    field_list = []
    float_format = Formatter.floats(1)
    add_unbuilt_element(field_list, Elements.lower, float_format, lower_limit)
    add_unbuilt_element(field_list, Elements.upper, float_format, upper_limit)

    if effort_limit is not None:
        add_unbuilt_element(field_list, Elements.effort, float_format, effort_limit)

    if velocity_limit is not None:
        add_unbuilt_element(field_list, Elements.velocity, float_format, velocity_limit)

    if joint_stop_stiffness is not None:
        add_unbuilt_element(field_list, Elements.stiffness, float_format, joint_stop_stiffness)

    if joint_stop_dissipation is not None:
        add_unbuilt_element(field_list, Elements.dissipation, float_format, joint_stop_dissipation)

    return build_element(
        Element.limit,
        Formatter.empty(),
        None,
        element_fields_list=field_list
    )
    

def gearbox_ratio(ratio: float) -> Element:
    return build_element(Elements.gearbox_ratio, Formatter.strings(), ratio)


def child(child_link: str) -> Element:
    return build_element(Elements.child, Formatter.strings(), child_link)


def parent(parent_link: str) -> Element:
    return build_element(Elements.parent, Formatter.strings(), parent_link)


def pose(
    se3_matrix: npt.ArrayLike,
    quaternion: bool = False,
    frame: Optional[str] = None
    ) -> Element:
    """Generates a pose and optional frame to append to the matrix for the SDF."""
    attr_list = []
    if frame is not None:
        add_attribute(attr_list, Attributes.relative_to, Formatter.strings(), frame)

    if quaternion:
        rot_format_data = "quat_xyzw"
    else:
        rot_format_data = "euler_rpy"

    add_attribute(attr_list, Attributes.rotation_format, Formatter.strings(), rot_format_data)

    x = se3_matrix[0, 3]
    y = se3_matrix[1, 3]
    z = se3_matrix[2, 3]
    rpy = rotationMatrixToEulerAngles(se3_matrix)
    
    return build_element(
        element_name=Elements.pose,
        element_format=Formatter.floats(6),
        element_data=(x, y, z, rpy[0], rpy[1], rpy[2]),
        element_attributes_list=attr_list,
    )


def inertial(
    auto_compute: bool = False,
    mass: Optional[float] = None,
    density: Optional[float] = None,
    optional_elements: Optional[list[Element]] = None
    ) -> Element:
    attr_list = []
    add_attribute(attr_list, Attributes.auto, Formatter.bools(), auto_compute)

    field_list = []
    if mass is not None:
        add_unbuilt_element(field_list, Elements.mass, Formatter.floats(1), mass)

    if density is not None:
        add_unbuilt_element(field_list, Elements.density, Formatter.floats(1), density,)
        
    append_optional_elements(field_list, optional_elements)

    return build_element(
        Elements.inertial,
        Formatter.empty(),
        None,
        element_attributes_list=attr_list,
        element_fields_list=field_list
    )


def geometry(
    empty: bool = False,
    optional_elements: Optional[list[Elements]] = None
    ) -> Element:
    field_list = []
    if empty:
        add_unbuilt_element(Elements.empty, Formatter.empty(), None)

    append_optional_elements(field_list, optional_elements)

    return build_element(
        Elements.geometry,
        Formatter.empty(),
        None,
        element_fields_list=field_list
    )


def material(
    ambient: Optional[npt.ArrayLike] = None,
    diffuse: Optional[npt.ArrayLike] = None,
    specular: Optional[npt.ArrayLike] = None,
    emissive: Optional[npt.ArrayLike] = None,
    ) -> Element:
    """Creates a material element corresponding to SDFormat 1.11"""
    field_list = []
    light_format = Formatter.floats(4)

    if ambient is not None:
        add_unbuilt_element(Elements.ambient, light_format, tuple(ambient))

    if diffuse is not None:
        add_unbuilt_element(Elements.diffuse, light_format, tuple(diffuse))

    if specular is not None:
        add_unbuilt_element(Elements.specular, light_format, tuple(specular))

    if emissive is not None:
        add_unbuilt_element(Elements.emissive, light_format, tuple(emissive))

    return build_element(
        Elements.material,
        Formatter.empty(),
        None,
        element_fields_list=field_list
    )


def joint(
    name: str,
    joint_type: str,
    parent: str,
    child: str,
    gearbox_ratio: Optional[float] = None,
    optional_elements: Optional[list[Elements]] = None
    ) -> Element:
    string_format = Formatter.strings()
    attr_list = []
    add_attribute(attr_list, Attributes.name, string_format, name)
    add_attribute(attr_list, Attributes.elem_type, string_format, joint_type)

    field_list = []
    add_unbuilt_element(field_list, Elements.parent, string_format, parent)
    add_unbuilt_element(field_list, Elements.child, string_format, child)

    if gearbox_ratio is not None:
        add_unbuilt_element(field_list, Elements.gearbox_ratio, string_format, gearbox_ratio)

    append_optional_elements(field_list, optional_elements)

    return build_element(
        Elements.joint,
        Formatter.empty(),
        None,
        element_attributes_list=attr_list,
        element_fields_list=fields_list,
    )


def sensor(
    name: str,
    sensor_type: str,
    always_on: Optional[bool] = None,
    update_rate: Optional[float] = None,
    topic: Optional[str] = None,
    optional_elements: Optional[list[Element]] = None,
    ) -> Element:
    string_format = Formatter.strings()
    attr_list = []
    add_attribute(attr_list, Attributes.name, string_format, name)
    add_attribute(attr_list, Attributes.elem_type, string_format, sensor_type)

    field_list = []
    if always_on is not None:
        add_unbuilt_element(field_list, Elements.always_on, Formatter.bools(), always_on)

    if update_rate is not None:
        add_unbuilt_element(field_list, Elements.update_rate, Formatter.floats(1), update_rate)

    if topic is not None:
        add_unbuilt_element(field_list, Elements.topic, string_format, topic)

    append_optional_elements(field_list, optional_elements)

    return build_element(
        Elements.sensor,
        Formatter.empty(),
        None,
        element_attributes_list=attr_list,
        element_fields_list=field_list
    )


    

    



    

    



