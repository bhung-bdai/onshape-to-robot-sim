from dataclasses import dataclass, asdict
from typing import Any, Optional

import numpy as np
import numpy.typing as npt

@dataclass
class Attributes:
    """Class for keeping track of an item in inventory."""
    attached_to: str = "attached_to"
    auto: str = "auto"
    axis: str = "axis"
    default: str = "default"
    degrees: str = "degrees"
    density: str = "density"
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
    ambient: str = "ambient"
    density: str = "density"
    diffuse: str = "diffuse"
    emissive: str = "emissive"
    empty: str = "empty"
    geometry: str = "geometry"
    inertia: str = "inertia"
    inertial: str = "inertial"
    ixx: str = "ixx"
    ixy: str = "ixy"
    ixz: str = "ixz"
    iyy: str = "iyy"
    iyz: str = "iyz"
    izz: str = "izz"
    joint: str = "joint"
    mass: str = "mass"
    material: str = "material"
    mesh: str = "mesh"
    pose: str = "pose"
    specular: str = "specular"
    uri: str = "uri"


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
        return format_string + " %s"


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
    return start_tag + body_string + end_tag


def _element_start(body_string: str) -> str:
    return _wrap_ends("<", body_string, ">\n")


def _element_end(body_string: str) -> str:
    return _wrap_ends("</", body_string, ">\n")


def build_attribute(
    attr_name: str,
    attr_format: str,
    attr_data: Any,
    ) -> str:
    """Build an attribute for an element"""
    return attr_name + "=" + (attr_format % attr_data) 


def build_element(
    element_name: str,
    element_format: str,
    element_data: Optional[Any] = None,
    element_attributes_list: list[str] = [],
    element_fields_list: list[str] = [],
    ) -> str:
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
        element_fields = element_data + element_fields
    # Format the body of the element properly
    element_body = (Formatter.elements(element_format) % element_fields).strip()
    return _wrap_ends(start_element, element_body, end_element)


def pose(
    se3_matrix: npt.ArrayLike,
    quaternion: bool = False,
    frame: Optional[str] = None
    ) -> str:
    """Generates a pose and optional frame to append to the matrix for the SDF."""
    attr_list = []
    if frame is not None:
        attr_list.append(build_attribute(Attributes.relative_to, Formatter.strings(), frame))

    if quaternion:
        rot_format_data = "quat_xyzw"
    else:
        rot_format_data = "euler_rpy"

    attr_list.append(build_attribute(Attributes.rotation_format, Formatter.strings(), rot_format_data))

    x = se3_matrix[0, 3]
    y = se3_matrix[1, 3]
    z = se3_matrix[2, 3]
    rpy = rotationMatrixToEulerAngles(se3_matrix)
    
    return build_element(
        element_name=Elements.pose,
        element_format=Formatter.floats(6),
        element_data=(x, y, z, rpy[0], rpy[1], rpy[2]),
        element_attributes_list=attr_list,
        element_fields_list=[]
    )


def inertial(
    auto_compute: bool = False,
    mass: Optional[float] = None,
    density: Optional[float] = None,
    pose: Optional[str] = None,
    inertia: Optional[str] = None,
    ) -> str:
    attribute_list = []
    attribute_list.append(build_attribute(Attributes.auto, Formatter.bools(), auto_compute))

    field_list = []
    if mass is not None:
        field_list.append(build_element(Elements.mass, Formatter.floats(1), (mass,)))

    if density is not None:
        field_list.append(build_element(Elements.density, Formatter.floats(1), (density,)))

    if pose is not None:
        field_list.append(build_element(Elements.pose, Formatter.strings(), (pose,)))

    if inertia is not None:
        field_list.append(build_element(Elements.inertia, Formatter.strings(), (inertia,)))

    return build_element(
        Elements.inertial,
        Formatter.empty(),
        None,
        element_attributes_list=attribute_list,
        element_fields_list=field_list
    )
    
def geometry(
    empty: bool = False,
    mesh: Optional[str] = None,
    ) -> str:
    field_list = []
    if empty:
        field_list.append(build_element(Elements.empty, Formatter.empty(), None))

    elif mesh is not None:
        mesh_list = []
        mesh_list.append(build_element(Elements.uri, Formatter.strings(), (mesh,)))
        field_list.append(build_element(Elements.mesh, Formatter.empty(), None, element_fields_list=mesh_list))

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
    ) -> str:
    field_list = []
    light_format = Formatter.floats(4)

    if ambient is not None:
        field_list.append(build_element(Elements.ambient, light_format, tuple(ambient)))

    if diffuse is not None:
        field_list.append(build_element(Elements.diffuse, light_format, tuple(diffuse)))

    if specular is not None:
        field_list.append(build_element(Elements.specular, light_format, tuple(specular)))

    if emissive is not None:
        field_list.append(build_element(Elements.emissive, light_format, tuple(emissive)))

    return build_element(
        Elements.material,
        Formatter.empty(),
        None,
        element_fields_list=field_list
    )
    

    



