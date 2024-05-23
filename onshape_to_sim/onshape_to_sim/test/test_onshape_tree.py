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

onshape_client = Client(creds="test_config.json", logging=False)


def _check_equality_based_on_type(
    value_one: Union[str, bool, float, int, np.ndarray, dict, list],
    value_two: Union[str, bool, float, int, np.ndarray, dict, list]
    ) -> bool:
    assert type(value_one) == type(value_two)
    match type(value_one):
        case __builtins__.str | __builtins__.bool | __builtins__.int:
            return value_one == value_two
        case __builtins__.float:
            return np.isclose(value_one, value_two, atol=1e-5)
        case __builtins__.list:
            # Can't really test this so we just skip it
            if len(value_one) == 0 and len(value_two) == 0:
                return True
            if len(value_one) > 0 and isinstance(value_one[0], dict):
                return True
            return set(value_one) == set(value_two)
        case np.ndarray:
            return np.allclose(value_one, value_two, atol=1e-5)
        case __builtins__.dict:
            for key, value in value_one.items():
                if key not in value_two:
                    print(f"Key {key} not in dictionary {value_two}")
                    return False
                if not _check_equality_based_on_type(value, value_two[key]):
                    if key == "href":
                        return True
                    print(f"Key {key} failed!")
                    print(f"{value} and {value_two[key]} not the same")
                    return False
            return True 
    return True


def test_add_instances_mass_properties():
    with open("../test/data/multi_features_sub_assembly.txt", "r") as fi:
        json_data = json.load(fi)
    instances = json_data["rootAssembly"]["instances"]
    test_dict = {}
    _add_instances_mass_properties(onshape_client, instances, test_dict)
    real_ans = {
        'ME0OGHafV27m4erd3': {'mass': 2.238744814460115, 'hasMass': True, 'volume': 0.0002787976107671376, 'centroid': np.array([0.0375, 0.02538434, 0.02252414]),
        'inertia': np.array([[2.06022579e-03,  4.48497460e-10,  6.47005805e-11], [ 4.48497460e-10,  1.50690602e-03, -2.87610453e-04], [ 6.47005805e-11, -2.87610453e-04,  2.54353670e-03]])},
        'MfnXxatwJGOcsLj0q': {'mass': 0.33541920259867775, 'hasMass': True, 'volume': 4.333581428923485e-05, 'centroid': np.array([-0.016 ,  0.0325,  0.025 ]), 
        'inertia': np.array([[0.0003453, 0., 0.], [0., 0.00017437, 0.], [0., 0., 0.00017437]])},
        'MmRHXBai4kux8tPcZ': {'mass': 0.33541920259867775, 'hasMass': True, 'volume': 4.333581428923485e-05, 'centroid': np.array([-0.016 ,  0.0325,  0.025 ]),
        'inertia': np.array([[0.0003453, 0., 0.], [0., 0.00017437, 0.], [0., 0., 0.00017437]])},
        'MrWVPT9IK41t//ORF': {'mass': 0.6708384051973555, 'hasMass': True, 'volume': 0.00038488350313340065, 'centroid': np.array([0.00562545, 0.02410958, 0.02827908]),
        'inertia': np.array([[ 0.00112744, -0.00050592,  0.00051152], [-0.00050592,  0.0017721 ,  0.00021231], [ 0.00051152,  0.00021231,  0.00176616]])},
        'MQ47hvC+ZVKiW4z6K': {'mass': 0.6708384051973555, 'hasMass': True, 'volume': 0.00038488350313340065, 'centroid': np.array([0.00562545, 0.02410958, 0.02827908]),
        'inertia': np.array([[ 0.00112744, -0.00050592,  0.00051152], [-0.00050592,  0.0017721 ,  0.00021231], [ 0.00051152,  0.00021231,  0.00176616]])}
        }
    assert _check_equality_based_on_type(real_ans, test_dict)


def test_stl_download():
    # f = open('output.txt','w')
    # sys.stdout = f
    did = "dc7bc8baf40949ec82a161ab"
    wvmid = "f403096346539d04d483a5e3"
    eid = "e246deec97cc75cedfed8035"
    wvm = "v"
    stl_dir = "/home/bhung/bdai/test/sdf_viewr/throwy/throwy"
    obj_dir = "/home/bhung/bdai/test/sdf_viewr/throwy/throwy"
    print("Creating tree...")
    # tree = create_onshape_tree(did=did, wvm=wvm, wvmid=wvmid, eid=eid, robot_name="throwy")
    # with open("throwy_tree.pickle", "wb") as fi:
    #     pickle.dump(tree, fi)
    with open("throwy_tree.pickle", "rb") as fi:
        tree = pickle.load(fi)
    # item = tree.search_by_occurrence_id("MFsBZ/Px6SfioMMrpMDRYr4POebo8qzdQh")
    # breakpoint()
    print("Creating SDF...")
    test_sdf = RobotSDF(tree, mesh_directory="/workspaces/bdai/test/sdf_viewr/throwy")
    test_sdf.write_sdf("/home/bhung/bdai/test/sdf_viewr/throwy/throwy")
    rigid_bodies = tree.rigid_bodies
    with open("throwy_dict.pickle", "wb") as fi:
        pickle.dump(rigid_bodies, fi)
    with open("throwy_dict.pickle", "rb") as fi:
        rigid_bodies = pickle.load(fi)
    # breakpoint()
    print("Downloading meshes...")
    try:
        mesh_files = download_all_rigid_bodies_meshes(
            rigid_bodies, data_directory=stl_dir, file_type=API.stl
        )
        convert_stls_to_objs(
            mesh_files,
            stl_dir,
            obj_dir,
            "/home/bhung/private-onshape-fork/onshape_to_sim/onshape_to_sim/onshape_api"
        )
    except Exception as e:
        pdb.post_mortem()


def test_full_pipeline():
    # f = open('output.txt','w')
    # sys.stdout = f
    # bf00afda41c872721af031c9/v/ee2d293125671a90033598ff/e/2c6cc034f38ef101337dcb9f
    # d2b65b007cccdccd672c9efe/v/8b21eaeb7705b07014b18f35/e/d64d0511810bd7d9d742d1bb
    ############## THROWY HAND ######################
    # did = "bf00afda41c872721af031c9"
    # wvmid = "a0a05ea9d3ac08f6f9cd3e6a"
    # eid = "2c6cc034f38ef101337dcb9f"
    # wvm = "v"
    # stl_dir = "/home/bhung/bdai/test/sdf_viewr/throwy/throwy"
    # obj_dir = "/home/bhung/bdai/test/sdf_viewr/throwy/throwy"
    # sdf_path = "/home/bhung/bdai/test/sdf_viewr/throwy"
    # sdf_name = "throwy_hand"
    ##################################################
    ############## SIMPLE ARM #######################
    did = "d2b65b007cccdccd672c9efe"
    wvmid = "6798c9b07bd476ed792df435"
    eid = "d64d0511810bd7d9d742d1bb"
    wvm = "v"
    stl_dir = "/home/bhung/bdai/test/sdf_viewr/basic_arm/basic_arm"
    obj_dir = "/home/bhung/bdai/test/sdf_viewr/basic_arm/basic_arm"
    sdf_path = "/home/bhung/bdai/test/sdf_viewr/basic_arm"
    sdf_name = "basic_arm"
    ####################################################
    # ############### HARDER ARM #######################
    # did = "9e58c2c2298902a0b2526461"
    # wvmid = "cf0d6030ccb0d5a12e0a9b91"
    # eid = "5048884906d62c21e634d119"
    # wvm = "v"
    # stl_dir = "/home/bhung/bdai/test/sdf_viewr/harder_arm/harder_arm"
    # obj_dir = "/home/bhung/bdai/test/sdf_viewr/harder_arm/harder_arm"
    # sdf_path = "/home/bhung/bdai/test/sdf_viewr/harder_arm"
    # sdf_name = "harder_arm"
    # #####################################################
    ################ ALPHA ARM ########################
    did = "e8781b431f32606ea5c54965"
    wvmid = "b111151b56b22ef3c70af6cf"
    eid = "aa4e98a002272561ed7c1de9"
    wvm = "v"
    stl_dir = "/home/bhung/bdai/test/sdf_viewr/alpha/alpha_arm"
    obj_dir = "/home/bhung/bdai/test/sdf_viewr/alpha/alpha_arm"
    sdf_path = "/home/bhung/bdai/test/sdf_viewr/alpha"
    sdf_name = "alpha_arm"
    store_data = False
    load_from_file = True
    file_path = f"data/{sdf_name}.pickle"
    #####################################################
    # ################ Alpha Shoulder ########################
    # did = "170c4feeceb4442201428f82"
    # wvmid = "91cebc008d1370c9420c69ed"
    # eid = "d04e6666d7681a875fac4ed7"
    # wvm = "v"
    # stl_dir = "/home/bhung/bdai/test/sdf_viewr/alpha/alpha_shoulder"
    # obj_dir = "/home/bhung/bdai/test/sdf_viewr/alpha/alpha_shoulder"
    # sdf_path = "/home/bhung/bdai/test/sdf_viewr/alpha"
    # sdf_name = "alpha_shoulder"
    # store_data = True
    # load_from_file = True
    # file_path = f"data/{sdf_name}.pickle"
    #####################################################
    ################## Testy ############################
    did = "cdd2ab0ab8757afe3d9e7315"
    wvmid = "92c1a74a6045990ebdb0faf4"
    eid = "c9b31228c9895c798565949b"
    wvm = "v"
    stl_dir = "/home/bhung/bdai/test/sdf_viewr/testy/mesh"
    obj_dir = "/home/bhung/bdai/test/sdf_viewr/testy/mesh"
    sdf_path = "/home/bhung/bdai/test/sdf_viewr/testy"
    sdf_name = "testy"
    store_data = True
    load_from_file = False
    file_path = f"data/{sdf_name}.pickle"
    #####################################################
    ################## Boxy ############################
    # # https://theaiinstitute.onshape.com/documents/cdd2ab0ab8757afe3d9e7315/v/ca50d0300b33af4b46547e6c/e/d4c2fa9afeb1b9c911720621
    # did = "cdd2ab0ab8757afe3d9e7315"
    # wvmid = "ecd861fa451ba2c80cb2386e"
    # eid = "d4c2fa9afeb1b9c911720621"
    # wvm = "v"
    # stl_dir = "/home/bhung/bdai/test/sdf_viewr/testy/mesh"
    # obj_dir = "/home/bhung/bdai/test/sdf_viewr/testy/mesh"
    # sdf_path = "/home/bhung/bdai/test/sdf_viewr/testy"
    # sdf_name = "testy"
    # store_data = True
    # load_from_file = False
    # file_path = f"data/{sdf_name}.pickle"
    #####################################################
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
            robot_name = sdf_name
        )
        if store_data:
            with open(file_path, "wb") as fi:
                pickle.dump(tree, fi)
    else:
        with open(file_path, "rb") as fi:
            tree = pickle.load(fi)["tree"]
    # print("Downloading meshes...")
    # try:
    #     breakpoint()
    #     mesh_files = download_all_rigid_bodies_meshes(
    #         tree.get_occurrence_id_to_rigid_body_node().values(),
    #         data_directory = stl_dir,
    #         file_type = API.stl
    #     )
    #     convert_stls_to_objs(
    #         mesh_files,
    #         stl_dir,
    #         obj_dir,
    #         "/home/bhung/private-onshape-fork/onshape_to_sim/onshape_to_sim/onshape_api"
    #     )
    # except Exception as e:
    #     pdb.post_mortem()
    print(tree.get_joint_parents())
    print("Creating SDF...")
    test_sdf = RobotSDF(tree, mesh_directory=sdf_path, sdf_name=sdf_name)
    test_sdf.write_sdf(f"{sdf_path}/{sdf_name}")
    # rigid_bodies = tree.rigid_bodies
    # with open(f"{sdf_name}_dict.pickle", "wb") as fi:
    #     pickle.dump(tree.rigid_bodies, fi)
    # with open("throwy_dict.pickle", "rb") as fi:
    #     rigid_bodies = pickle.load(fi)
    # # breakpoint()
    print("Downloading meshes...")
    try:
        breakpoint()
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


def stl_converter(stl_dir: str, obj_dir: str, mesh_files: str, stl_to_obj_location: str) -> None:
    # stl_dir = "/home/bhung/bdai/test/sdf_viewr/simple_arm/simple_arm"
    # obj_dir = "/home/bhung/bdai/test/sdf_viewr/simple_arm/simple_arm"
    # tree = create_onshape_tree(did=did, wvm=wvm, wvmid=wvmid, eid=eid, robot_name="simple_arm")
    # mesh_files = download_all_rigid_bodies_meshes(tree, data_directory=stl_dir, file_type=API.stl)
    convert_stls_to_objs(mesh_files, stl_dir, obj_dir, "/home/bhung/private-onshape-fork/onshape_to_sim/onshape_to_sim/onshape_api")


if __name__ == "__main__":
    # test_stl_download()
    test_full_pipeline()
    # test_mass_properties_map()
    # stl_obj_dir =  "/home/bhung/bdai/test/sdf_viewr/throwy/throwy"
    # mesh_files = ["base.stl", "part_assem.stl", "x_shaft.stl", "y_shaft.stl", "z_shaft.stl"]
    # mesh_files = ["elbowdrive.stl", "forearm.stl", "housing.stl", "rotor.stl", "uaassembly.stl"]
    # stl_converter(
    #     stl_obj_dir,
    #     stl_obj_dir,
    #     mesh_files,
    #     "/home/bhung/private-onshape-fork/onshape_to_sim/onshape_to_sim/onshape_api"
    # )

    # test_stl_download()

