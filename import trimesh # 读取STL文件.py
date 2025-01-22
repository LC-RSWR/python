


import trimesh # 读取STL文件 
mesh = trimesh.load('C:/Users/deskadmin/Desktop/TEST/U.stl') # 保存为STL文件 
mesh.export('output.stl') 

vertices = mesh.vertices 
faces = mesh.faces 
area = mesh.area 
print("area", area)
center = mesh.center_mass 
print("center", center)

import trimesh
 
# 假设有点和面的信息
vertices = [[0, 0, 0], [1, 0, 0], [0, 1, 0]]
faces = [[0, 1, 2]]
 
# 创建 trimesh 网格对象
mesh = trimesh.Trimesh(vertices=vertices, faces=faces)
 
# 访问顶点法向量
vertex_normals = mesh.vertex_normals
 
# 访问面法向量
face_normals = mesh.face_normals
 
# 打印结果
print("Vertex Normals:", vertex_normals)
print("Face Normals:", face_normals)

import numpy as np
import open3d as o3d


points = np.random.rand(10000, 3)
point_cloud = o3d.geometry.PointCloud()
point_cloud.points = o3d.utility.Vector3dVector(points)
#o3d.visualization.draw_geometries([point_cloud])

#o3d.visualization.draw_geometries(mesh.vertices)

