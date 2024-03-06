import os

import numpy as np
import numpy.typing as npt
from xml.sax.saxutils import escape

# Most of the follow code was adapted or lifted from the Onshape to Robot original file:
# https://github.com/Rhoban/onshape-to-robot/blob/master/onshape_to_robot/robot_description.py

def xml_escape(unescaped: str) -> str:
    """Escapes XML characters in a string so that it can be safely added to an XML file
    """
    return escape(unescaped, entities={
        "'": "&apos;",
        "\"": "&quot;"
    })

def rotationMatrixToEulerAngles(R: npt.ArrayLike) -> npt.ArrayLike:
    sy = np.sqrt(R[0, 0] * R[0, 0] + R[1, 0] * R[1, 0])

    singular = sy < 1e-6

    if not singular:
        x = np.arctan2(R[2, 1], R[2, 2])
        y = np.arctan2(-R[2, 0], sy)
        z = np.arctan2(R[1, 0], R[0, 0])
    else:
        x = np.arctan2(-R[1, 2], R[1, 1])
        y = np.arctan2(-R[2, 0], sy)
        z = 0

    return np.array([x, y, z])

def pose(se3_matrix: npt.ArrayLike) -> npt.ArrayLike:
    """Extracts a pose (represented by x, y, z, roll, pitch, yaw) from an SE3 matrix"""
    xyz = se3_matrix[:3, 3]
    rpy = rotationMatrixToEulerAngles(se3_matrix)
    return np.concatenate((xyz, rpy), axis=0)

# TODO Look into seeing if we need to express other properties in relative frames. This has the world one
def express_mass_properties_in_element_frame(
    world_tform_element: npt.ArrayLike,
    mass: float,
    com: npt.ArrayLike,
    inertia: npt.ArrayLike
    ) -> tuple: 
    world_r_element = world_tform_element[:3, :3]

    # Expressing COM in the link frame
    com_in_element_frame = (world_tform_element @ np.array([com[0], com[1], com[2], 1]))[:3]

    # Expressing inertia in the link frame
    inertia_in_element_frame = world_r_element @ inertial @ world_r_element.T
    return (mass, com_in_element_frame, inertia_in_element_frame)


def combine_inertial_properties(
    masses: npt.ArrayLike,
    coms: npt.ArrayLike,
    inertias: npt.ArrayLike,
) -> tuple:
    """Combines a set of bodies with inertial properties expressed in the same frame into a single rigid body
    
    Args:
        masses: a (num_bodies, 1) array of mass values in kg(?)
        coms: a (num_bodies, 3) array of center of masses in meters (?)
        inertias: a (num_bodies, 3, 3) array of inertial masses in whatever units this uses

    Returns:
        A mass, com, and inertia equivalent of the listed bodies as a single rigid body (SRB)
    """
    mass_srb = 0
    com_srb = np.zeros((3,))
    inertia_srb = np.zeros((3, 3))
    I = np.eye(3)
    num_bodies = masses.shape[0]

    for i in range(num_bodies):
        mass_body = masses[i]
        com_body = coms[i, :]
        inertia_body = inertias[i, :, :]

        mass_srb += mass_body
        com_srb += com_body
        inertia_srb += inertia_body + (np.dot(r, r) * I - np.outer(r, r)) * mass_body

    if mass_srb > 0:
        com_srb /= mass_srb

    return (mass_srb, com_srb, inertia_srb)


