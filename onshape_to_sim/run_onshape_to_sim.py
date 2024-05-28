from typing import Union
import json
import pdb
import pickle
import sys

import numpy as np

from onshape_to_sim.onshape_api.client import Client
from onshape_to_sim.onshape_api.onshape_tree import (
    build_tree,
    create_onshape_tree,
    download_all_rigid_bodies_meshes,
    _add_instances_mass_properties,
)
from onshape_to_sim.onshape_api.utils import (
    API,
    convert_stls_to_objs,
)
from onshape_to_sim.sdf.sdf_description import RobotSDF

def main():
    ############## Configuration information #######################
    did = "cdd2ab0ab8757afe3d9e7315" # document id of assembly
    wvmid = "92c1a74a6045990ebdb0faf4" # workspace, version, or microversion id of assembly
    eid = "c9b31228c9895c798565949b" # element id of assembly
    wvm = "v" # "w"orkspace, "v"ersion, or "m"icroversion of assembly
    stl_dir = "example_dir/mesh" # Directory to download the stls to
    obj_dir = "example_dir/mesh" # Directory to download the objs to
    sdf_path = "example_dir/sdf" # Directory to download SDF to 
    sdf_name = "testy" # name of the SDF to test
    store_data = True # Whether or not to store the data in a pickle file
    load_from_file = False # Whether or not to load data from a pickle file
    file_path = f"example_dir/{sdf_name}.pickle" # Filepath of the pickle file
    onshape_client = Client(creds="example_config.json", logging=False) # Onshape client
    ####################################################
    # Creates an Onshape Tree
    if not load_from_file:
        print("Creating tree...")
        tree = create_onshape_tree(
            did = did,
            wvm = wvm,
            wvmid = wvmid,
            eid = eid,
            store_data = store_data,
            load_data = load_from_file,
            file_path = file_path,
            robot_name = sdf_name,
            api_client = onshape_client
        )
        if store_data:
            with open(file_path, "wb") as fi:
                pickle.dump(tree, fi)
    else:
        with open(file_path, "rb") as fi:
            tree = pickle.load(fi)["tree"]
    # Creates the SDF
    print("Creating SDF...")
    test_sdf = RobotSDF(tree, mesh_directory=sdf_path, sdf_name=sdf_name)
    test_sdf.write_sdf(f"{sdf_path}/{sdf_name}")
    # Downloads the rigid body meshes
    print("Downloading meshes...")
    try:
        mesh_files = download_all_rigid_bodies_meshes(
            tree.get_occurrence_id_to_rigid_body_node().values(),
            data_directory = stl_dir,
            file_type = API.stl
        )
        convert_stls_to_objs(
            mesh_files,
            stl_dir,
            obj_dir,
            "/home/bhung/private-onshape-fork/onshape_to_sim/onshape_to_sim/onshape_api"
        )
    except Exception as e:
        pdb.post_mortem()


if __name__ == "__main__":
    main()