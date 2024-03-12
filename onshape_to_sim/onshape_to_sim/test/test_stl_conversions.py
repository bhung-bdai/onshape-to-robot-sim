import os

from onshape_to_sim.onshape_api.utils import (
    convert_stls_to_objs
)

def test_stl_to_obj():
    stl_dir = os.path.join("data", "stl_test")
    stl_files = os.listdir(stl_dir)
    convert_stls_to_objs(stl_files, stl_dir=stl_dir, save_dir=os.path.join("data", "obj_test"))

if __name__ == "__main__":
    test_stl_to_obj()