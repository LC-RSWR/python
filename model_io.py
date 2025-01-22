from stl import mesh
import numpy as np
import trimesh

def stl_to_obj(stl_file, obj_file):
    # 从STL文件加载模型
    stl_mesh = mesh.Mesh.from_file(stl_file)

    # 将STL模型保存为OBJ
    with open(obj_file, 'w') as f:
        for i in range(stl_mesh.points.shape[0]):
            f.write(f"v {stl_mesh.points[i][0]} {stl_mesh.points[i][1]} {stl_mesh.points[i][2]}\n")
        for i in range(stl_mesh.vectors.shape[0]):
            f.write(f"f {stl_mesh.vectors[i][0]+1} {stl_mesh.vectors[i][1]+1} {stl_mesh.vectors[i][2]+1}\n")

def obj_to_stl(obj_file, stl_file):
    # 从OBJ文件加载模型
    obj_mesh = trimesh.load_mesh(obj_file)

    # 将OBJ模型保存为STL
    obj_mesh.export(stl_file)

# 使用示例
stl_to_obj('input.stl', 'output.obj')
#obj_to_stl('input.obj', 'output.stl')

