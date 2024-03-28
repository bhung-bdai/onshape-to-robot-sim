from typing import Union
import json
import time

import numpy as np

from onshape_to_sim.onshape_api.client import Client
from onshape_to_sim.onshape_api.onshape_tree import (
    build_tree,
    _add_instances_mass_properties,
    _build_mass_properties_map
)

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


def test_assembly_definition():
    assem_def = onshape_client.assembly_definition(
        did = "6041e7103bb40af449a81618", 
        wvmid = "7e51d7b6b381bd79481e2033",
        eid = "aad7f639435879b7135dce0f",
        wvm = "v",
        )
    with open("../test/data/multi_features_version_locked.txt", "r") as fi:
        json_data = json.load(fi)
    assert _check_equality_based_on_type(assem_def["rootAssembly"], json_data["rootAssembly"])


def test_single_part_metadata():
    metadata_retrieved = onshape_client.part_metadata(
        did = "6041e7103bb40af449a81618",
        wvmid = "cddf1867f39445633530cda9",
        eid = "7a12328807be40cb1472cc52",
        partid = "JHD",
        wvm = "v",
    )
    with open("../test/data/one_part_metadata.txt", "r") as fi:
        json_data = json.load(fi)
    assert _check_equality_based_on_type(json_data, metadata_retrieved)
    

def test_all_part_metadata():
    metadata_retrieved = onshape_client.all_part_metadata(
        did = "6041e7103bb40af449a81618",
        wvmid = "cddf1867f39445633530cda9",
        eid = "7a12328807be40cb1472cc52",
        wvm = "v",
    )
    with open("../test/data/all_part_metadata.txt", "r") as fi:
        json_data = json.load(fi)
    assert _check_equality_based_on_type(json_data, metadata_retrieved)


def test_assembly_obj_exporter():
    resp = onshape_client.assembly_export_obj(
        did = "6041e7103bb40af449a81618",
        wvm = "w",
        wvmid = "43424f4f4c4a96485262232a",
        eid = "aad7f639435879b7135dce0f",
        filename = "test",
    )
    print(resp)
    url = resp["id"]
    time.sleep(2.0)
    resp = onshape_client.ping_async_export_call(url)
    print(resp)
    return resp


def test_obj_download(fid: str):
    resp = onshape_client.download_document_external_data(
        did = "6041e7103bb40af449a81618",
        fid = fid,
        filename = "data/obj_test/test"
    )
    print(resp.headers)
    print(resp.headers.get('content-type'))
    # print(f"Resp {resp.content}")


if __name__ == "__main__":
    # test_assembly_definition()
    # test_single_part_metadata()
    # test_all_part_metadata()
    resp = test_assembly_obj_exporter()
    test_obj_download(fid=resp["resultExternalDataIds"][0])
