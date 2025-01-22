import open3d as o3d
import numpy as np

# 读取 STL 文件
mesh = o3d.io.read_triangle_mesh("input.stl")

# 提取顶点和法线信息
mesh.compute_vertex_normals()

# 创建点云对象
point_cloud = mesh.sample_points_uniformly(number_of_points=50000)

# 进行点云重建
print("Reconstructing point cloud...")
o3d.utility.set_verbosity_level(o3d.utility.VerbosityLevel.Error)

distances = point_cloud.compute_nearest_neighbor_distance()
avg_dist = np.mean(distances)
radius = 7 * avg_dist

print(f"Avg. distance: {avg_dist:.4f}")
print(f"Voxel grid radius: {radius:.4f}")

mesh_reconstructed = o3d.geometry.TriangleMesh.create_from_point_cloud_ball_pivoting(point_cloud, o3d.utility.DoubleVector([radius, radius * 2]))

# 对三角网格进行细化操作
#mesh.subdivide_loop(number_of_iterations=2)

#
# 将模型导出为 STL 文件
o3d.io.write_triangle_mesh("output_mesh.stl", mesh_reconstructed)

# 可视化结果
o3d.visualization.draw_geometries([mesh_reconstructed])
