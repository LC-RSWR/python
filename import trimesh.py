import trimesh
import numpy as np
from trimesh import transformations

def rotate_to_meshlab_standards(stl_file, output_file):
    # 读取 STL 文件
    mesh = trimesh.load_mesh(stl_file)
    
    # 获取包围盒（bounding box）
    bounding_box = mesh.bounding_box
    extents = bounding_box.extents  # 取得包围盒的尺寸
    
    # 取得包围盒的旋转矩阵
    rotation_matrix = bounding_box.rotation  # 获取包围盒的旋转矩阵
    
    # 如果模型的高度（Z轴）方向不符合MeshLab标准，需要调整
    # MeshLab标准通常是Z轴向上，需要判断Z轴的方向并调整
    if np.abs(rotation_matrix[2, 2]) < 0.9:  # 判断Z轴是否接近上方向
        # 绕 X 或 Y 轴旋转90度
        rotation_matrix = transformations.rotation_matrix(np.pi / 2, [1, 0, 0])  # 绕 X 轴旋转90度
    
    # 应用旋转矩阵
    mesh.apply_transform(rotation_matrix)

    # 保存调整后的 STL 文件
    mesh.export(output_file)

    print(f"STL 文件已保存为: {output_file}")

# 使用示例
input_stl = r"input_model.stl"
output_stl = r"output_model.stl"
rotate_to_meshlab_standards(input_stl, output_stl)
