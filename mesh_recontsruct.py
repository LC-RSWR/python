import open3d as o3d




# 读取三角网格文件
mesh = o3d.io.read_triangle_mesh("input.stl")

# 从三角网格中采样点云数据
pcd = mesh.sample_points_poisson_disk(80000)

# 显示原始点云
print("Displaying input point cloud...")
o3d.visualization.draw_geometries([pcd])

# 运行 Poisson 表面重建，并减少孔洞
print("Running Poisson surface reconstruction...")
mesh_reconstructed, densities = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(pcd, depth=12)  # 增加 depth 的值

# 将模型导出为 STL 文件
o3d.io.write_triangle_mesh("output_mesh.stl", mesh)
# 显示重建后的网格
print("Displaying reconstructed mesh...")
mesh_reconstructed.paint_uniform_color((0, 1, 1))
o3d.visualization.draw_geometries([mesh_reconstructed])

