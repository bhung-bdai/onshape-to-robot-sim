import os

from onshape_to_sim.onshape_api.client import Client

if __name__ == "__main__":
    client = Client(creds="test_config.json")
    did = "6041e7103bb40af449a81618"
    wid = "43424f4f4c4a96485262232a"
    wvm = "w"
    eid = "7a12328807be40cb1472cc52"
    resp = client.part_export_stl(did=did, wvm=wvm, wvmid=wid, part_id="JHD", eid=eid)
    stl_dir = os.path.join("data", "stl_test")
    with open(os.path.join(stl_dir, "test.stl"), "wb") as f:
        f.write(resp.content)
