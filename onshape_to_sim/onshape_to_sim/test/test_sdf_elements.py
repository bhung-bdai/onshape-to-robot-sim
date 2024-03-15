#!/usr/bin/env python3
# Copyright (c) 2024 Boston Dynamics AI Institute LLC. All rights reserved.
"""Tests the formation of the SDF elements"""
import json
import os

import numpy as np

from gz.math7 import (
    Color,
    Inertiald,
    MassMatrix3d,
    Pose3d,
)
from sdformat13 import (
    Collision,
    Frame,
    Geometry,
    Link,
    Material,
    Mesh,
    Model,
    Root,
    Visual,
)
from onshape_to_sim.onshape_api.onshape_tree import (
    build_tree,
)
from onshape_to_sim.sdf.sdf_description import (
    make_color_gz,
    make_inertia_gz,
    make_inertial_gz,
    RobotSDF,
)

def test_robot_sdf_no_mates() -> None:
    with open("data/no_assembly.txt", "r") as fi:
        json_data = json.load(fi)
    test = build_tree(json_data, robot_name="2wheel_no_mate")
    test_sdf = RobotSDF(test)
    test_sdf.write_sdf(os.path.join("data", "2wheels_no_mate"))

def test_robot_sdf_extra_parts() -> None:
    with open("data/one_assembly.txt", "r") as fi:
        json_data = json.load(fi)
    test = build_tree(json_data, robot_name="2wheel_one_assem")
    test_sdf = RobotSDF(test)
    test_sdf.write_sdf(os.path.join("data", "2wheels_one_assem"))


if __name__ == "__main__":
    # test_robot_sdf_no_mates()
    test_robot_sdf_extra_parts()


