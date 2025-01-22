import open3d as o3d
import os


# 设置工作目录为代码文件所在的目录
os.chdir(os.path.dirname(__file__))

output_directory = "simplified_models"
os.makedirs(output_directory, exist_ok=True)



def simplify_stl(input_file, output_dir):
    # 加载STL模型
    if os.path.exists(input_file):
        mesh = o3d.io.read_triangle_mesh(input_file)
    # 继续处理模型...
    else:
        print("File not found:", input_file)

    # 获取原始模型的三角形数量
    num_triangles = len(mesh.triangles)
    mesh.compute_vertex_normals()

    # 按照不同的简化比例进行简化并保存
    for percentage in range(1, 99, 1):
        # 计算目标三角形数量
        target_triangles = int(num_triangles * (100 -percentage) / 100.0)
        simplified_mesh = mesh.simplify_quadric_decimation(target_triangles)
        output_file = f"{output_dir}/{percentage}%.stl"
        o3d.io.write_triangle_mesh(output_file, simplified_mesh)
        print(f"Saved simplified model at {output_file}")

# 输入STL文件和输出目录
input_stl_file = "input.stl"
output_directory = "simplified_models"

# 执行简化并保存不同比例的模型
simplify_stl(input_stl_file, output_directory)
