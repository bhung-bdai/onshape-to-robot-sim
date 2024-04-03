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
    create_onshape_tree,
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
    print(test.parent_nodes)
    test_sdf = RobotSDF(test, mesh_directory="/workspaces/bdai/test/sdf_viewr/2wheels")
    test_sdf.write_sdf("/home/bhung/bdai/test/sdf_viewr/2wheels/2wheels_no_mate")

def test_robot_sdf_extra_parts() -> None:
    with open("data/one_assembly.txt", "r") as fi:
        json_data = json.load(fi)
    test = build_tree(json_data, robot_name="2wheel_one_assem")
    test_sdf = RobotSDF(test, mesh_directory="/workspaces/bdai/test/sdf_viewr/2wheels")
    test_sdf.write_sdf("/home/bhung/bdai/test/sdf_viewr/2wheels/2wheels_one_assem")

def test_two_wheels_all_end_to_end() -> None:
    did = "6041e7103bb40af449a81618"
    wvmid = "78ea070002f23f4d1dd11250"
    eid = "aad7f639435879b7135dce0f"
    wvm = "v"
    tree = create_onshape_tree(did=did, wvm=wvm, wvmid=wvmid, eid=eid, robot_name="2wheel_all_added")
    test_sdf = RobotSDF(tree, mesh_directory="/workspaces/bdai/test/sdf_viewr/2wheels")
    test_sdf.write_sdf("/home/bhung/bdai/test/sdf_viewr/2wheels/2wheels_all_added")

def test_two_wheels_planar() -> None:
    did = "6041e7103bb40af449a81618"
    wvmid = "b6d602f59a1ea3dd30577849"
    eid = "aad7f639435879b7135dce0f"
    wvm = "v"
    tree = create_onshape_tree(did=did, wvm=wvm, wvmid=wvmid, eid=eid, robot_name="2wheel_planar")
    test_sdf = RobotSDF(tree, mesh_directory="/workspaces/bdai/test/sdf_viewr/2wheels")
    test_sdf.write_sdf("/home/bhung/bdai/test/sdf_viewr/2wheels/2wheels_planar")

def test_two_wheels_cyl() -> None:
    did = "6041e7103bb40af449a81618"
    wvmid = "f6f89c195eec60b2e5c8a73e"
    eid = "aad7f639435879b7135dce0f"
    wvm = "v"
    tree = create_onshape_tree(did=did, wvm=wvm, wvmid=wvmid, eid=eid, robot_name="2wheel_cyl")
    test_sdf = RobotSDF(tree, mesh_directory="/workspaces/bdai/test/sdf_viewr/2wheels")
    test_sdf.write_sdf("/home/bhung/bdai/test/sdf_viewr/2wheels/2wheels_cyl")


if __name__ == "__main__":
    # test_robot_sdf_no_mates()
    # test_robot_sdf_extra_parts()
    # test_two_wheels_all_end_to_end()
    # test_two_wheels_planar()
    test_two_wheels_cyl()


