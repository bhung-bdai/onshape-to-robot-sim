import argparse

import open3d as o3d

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("obj_file")
    args = parser.parse_args()
    obj_file = args.obj_file
    if not obj_file.endswith(".obj"):
        obj_file += ".obj"
    mesh = o3d.io.read_triangle_mesh(obj_file)
    o3d.visualization.draw_geometries([mesh])

