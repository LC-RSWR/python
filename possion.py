import open3d as o3d

# 读取点云文件
#point_cloud = o3d.io.read_point_cloud("input_point_cloud.ply")

# 读取 STL 文件
mesh = o3d.io.read_triangle_mesh("input.stl")

# 提取顶点和法线信息
mesh.compute_vertex_normals()

# 创建点云对象
point_cloud = mesh.sample_points_uniformly(number_of_points=100000)

# 进行点云重建
print("Reconstructing point cloud...")
o3d.utility.set_verbosity_level(o3d.utility.VerbosityLevel.Error)  # 设置日志级别为Error

mesh, densities = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(point_cloud, depth=9)

# 将模型导出为 STL 文件
o3d.io.write_triangle_mesh("output_mesh.stl", mesh)

# 可视化结果
o3d.visualization.draw_geometries([mesh])
