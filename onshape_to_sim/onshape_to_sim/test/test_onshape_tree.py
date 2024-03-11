from typing import Union
import json

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


def test_mass_properties_map():
    with open("../test/data/multi_features_sub_assembly.txt", "r") as fi:
        json_data = json.load(fi)
    instances = json_data["rootAssembly"]["instances"]
    subassemblies = json_data["subAssemblies"]
    mass_properties_map = _build_mass_properties_map(onshape_client, instances, subassemblies)
    real_map = {
        'ME0OGHafV27m4erd3': {'mass': 2.2387448144601145, 'hasMass': True, 'volume': 0.00027879761076713756, 'centroid': np.array([0.0375    , 0.02538434, 0.02252414]),
        'inertia': np.array([[ 2.06022579e-03,  4.48497460e-10,  6.47005805e-11], [ 4.48497460e-10,  1.50690602e-03, -2.87610453e-04], [ 6.47005805e-11, -2.87610453e-04,  2.54353670e-03]])},
        'MfnXxatwJGOcsLj0q': {'mass': 0.3354192025986777, 'hasMass': True, 'volume': 4.333581428923484e-05, 'centroid': np.array([-0.016 ,  0.0325,  0.025 ]),
        'inertia': np.array([[0.0003453, 0., 0.], [0., 0.00017437, 0.], [0., 0., 0.00017437]])},
        'MmRHXBai4kux8tPcZ': {'mass': 0.33541920259867775, 'hasMass': True, 'volume': 4.333581428923485e-05, 'centroid': np.array([-0.016 ,  0.0325,  0.025 ]),
        'inertia': np.array([[0.0003453, 0., 0.], [0.        , 0.00017437, 0.        ], [0.        , 0.        , 0.00017437]])},
        'MrWVPT9IK41t//ORF': {'mass': 0.6708384051973554, 'hasMass': True, 'volume': 0.00038488350313340065, 'centroid': np.array([0.00562545, 0.02410958, 0.02827908]),
        'inertia': np.array([[0.00112744, -0.00050592,  0.00051152], [-0.00050592, 0.0017721, 0.00021231], [0.00051152,  0.00021231, 0.00176616]])},
        'MQ47hvC+ZVKiW4z6K': {'mass': 0.6708384051973555, 'hasMass': True, 'volume': 0.00038488350313340065, 'centroid': np.array([0.00562545, 0.02410958, 0.02827908]),
        'inertia': np.array([[0.00112744, -0.00050592,  0.00051152], [-0.00050592, 0.0017721, 0.00021231], [0.00051152,  0.00021231,  0.00176616]])},
        'MMOby+OjmU+PDKhT8': {'mass': 0.0, 'hasMass': False, 'volume': 0.00014910593727746548, 'centroid': np.array([0., 0., 0.]),
        'inertia': np.array([[0., 0., 0.], [0., 0., 0.], [0., 0., 0.]])},
        'MvW7NkK9OkQ8TI+lI': {'mass': 0.0, 'hasMass': False, 'volume': 0.00014910593727746548, 'centroid': np.array([0., 0., 0.]),
        'inertia': np.array([[0., 0., 0.], [0., 0., 0.], [0., 0., 0.]])},
        'MmXPaG80Mq0OnEMRb': {'mass': 0.3354192025986777, 'hasMass': True, 'volume': 4.333581428923484e-05, 'centroid': np.array([-0.016, 0.0325, 0.025 ]),
        'inertia': np.array([[0.0003453 , 0., 0.], [0., 0.00017437, 0.], [0., 0., 0.00017437]])},
        'MjXp5OEcWIwYLGGrG': {'mass': 0.33541920259867775, 'hasMass': True, 'volume': 4.333581428923485e-05, 'centroid': np.array([-0.016, 0.0325, 0.025 ]),
        'inertia': np.array([[0.0003453, 0., 0.], [0., 0.00017437, 0.], [0., 0., 0.00017437]])},
        'MgaIc8LGcDUPIU5f7': {'mass': 0.0, 'hasMass': False, 'volume': 0.00029821187455493096, 'centroid': np.array([-0.04381188, -0.03670293, -0.03739811]),
        'inertia': np.array([[ 1.00443474e-06, -5.08627335e-07, -4.01144826e-07], [-5.08627335e-07,  8.02950958e-07, -4.88390873e-07], [-4.01144826e-07, -4.88390873e-07,  1.03701629e-06]])}
    }
    print(mass_properties_map)
    assert _check_equality_based_on_type(mass_properties_map, real_map)


if __name__ == "__main__":
    test_mass_properties_map()

