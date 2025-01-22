# 导入open3d和所有其他必要的库。
# 堆代码 duidaima.com
import open3d as o3d
import os
import copy
import numpy as np
import pandas as pd
np.random.seed(42)
#正在检查open3d上安装的版本。
o3d.__version__
# Open3D version used in this exercise: 0.16.0
 
# 指定要加载的网格文件路径
mesh_file = ""
 
#定义三维模型文件的路径。
mesh_path = "C:/Users/deskadmin/Desktop/TEST/U.stl"
# 使用open3d将三维模型文件读取为三维网格。
mesh = o3d.io.read_triangle_mesh(mesh_path)

# 计算网格的法线。
mesh.compute_vertex_normals()


# 创建XYZ轴笛卡尔坐标系的网格。
# 该网格将显示X、Y和Z轴指向的方向，并且可以覆盖在3D网格上，以可视化其在欧几里得空间中的方向。
# X-axis : 红色箭头
# Y-axis : 绿色箭头
# Z-axis : 蓝色箭头
mesh_coord_frame = o3d.geometry.TriangleMesh.create_coordinate_frame(size=5, origin=[0, 0, 0])
#使用坐标系可视化网格，以了解方向。
#draw_geoms_list = [mesh_coord_frame, mesh]
#o3d.visualization.draw_geometries(draw_geoms_list)

#从网格中均匀采样100000个点，将其转换为点云。
n_pts = 100_000
pcd = mesh.sample_points_uniformly(n_pts)
#可视化点云。
draw_geoms_list = [mesh_coord_frame, pcd]
o3d.visualization.draw_geometries(draw_geoms_list)