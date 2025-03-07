import numpy as np
import open3d as o3d
import xml.etree.ElementTree as ET
from tkinter import Tk, filedialog, Button

# 1. 打开文件选择对话框
def open_file_dialog(title, filetypes):
    return filedialog.askopenfilename(title=title, filetypes=filetypes)

# 2. 从XML文件读取数据
def read_xml_data(xml_file_path):
    tree = ET.parse(xml_file_path)
    root = tree.getroot()

    X = float(root.attrib['X'])
    Y = float(root.attrib['Y'])
    Z = float(root.attrib['Z'])
    LX = float(root.attrib['LX'])
    LY = float(root.attrib['LY'])
    LZ = float(root.attrib['LZ'])
    A = float(root.attrib['A'])
    LA = float(root.attrib['LA'])

    return X, Y, Z, LX, LY, LZ, A, LA

# 3. 从TXT文件读取切割点和刀轴方向
def read_cutting_data(txt_file_path):
    cutting_points = []
    with open(txt_file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            parts = line.strip().split()
            if len(parts) == 6:  # 切割点位置 + 刀轴方向
                point = list(map(float, parts[:3]))  # 切割点位置
                direction = list(map(float, parts[3:]))  # 刀轴方向
                cutting_points.append((point, direction))
            elif len(parts) == 7:  # 四元素形式
                point = list(map(float, parts[:3]))  # 切割点位置
                quaternion = list(map(float, parts[3:]))  # 四元素
                cutting_points.append((point, quaternion))
    return cutting_points

# 4. 创建矩形框线条
def create_rectangle(width, height, color):
    points = [
        [-width/2, -height/2, 0],
        [width/2, -height/2, 0],
        [width/2, height/2, 0],
        [-width/2, height/2, 0],
        [-width/2, -height/2, 0]
    ]
    lines = [[i, i+1] for i in range(4)]
    
    line_set = o3d.geometry.LineSet()
    line_set.points = o3d.utility.Vector3dVector(points)
    line_set.lines = o3d.utility.Vector2iVector(lines)
    line_set.colors = o3d.utility.Vector3dVector([color for _ in range(len(lines))])
    
    return line_set

# 5. 渲染STL模型并添加标注点
def render_stl_and_mark_points(stl_file_path, X, Y, Z, LX, LY, LZ, A, LA, cutting_data):
    # 加载STL模型
    mesh = o3d.io.read_triangle_mesh(stl_file_path)
    mesh.compute_vertex_normals()
    mesh.paint_uniform_color([0.7, 0.8, 1.0])  # 浅蓝色

    # 创建可视化窗口
    vis = o3d.visualization.Visualizer()
    vis.create_window(window_name="3D Viewer", width=1024, height=768)
    
    # 设置渲染选项
    opt = vis.get_render_option()
    opt.background_color = np.asarray([1, 1, 1])  # 白色背景
    opt.mesh_show_wireframe = True
    opt.mesh_show_back_face = True
    
    # 添加网格模型
    vis.add_geometry(mesh)

    # 创建QR码矩形框
    qr_rect = create_rectangle(8, 4, [0, 1, 0])  # 绿色，8mm x 4mm
    # 旋转QR码矩形框
    qr_angle_rad = -np.radians(90 - A)
    R_qr = qr_rect.get_rotation_matrix_from_xyz([0, 0, qr_angle_rad])
    qr_rect.rotate(R_qr, center=[0, 0, 0])
    qr_rect.translate([X, Y, Z])
    vis.add_geometry(qr_rect)

    # 创建LOGO矩形框
    logo_rect = create_rectangle(4, 4, [1, 0, 0])  # 红色，4mm x 4mm
    # 旋转LOGO矩形框
    logo_angle_rad = -np.radians(90 - LA)
    R_logo = logo_rect.get_rotation_matrix_from_xyz([0, 0, logo_angle_rad])
    logo_rect.rotate(R_logo, center=[0, 0, 0])
    logo_rect.translate([LX, LY, LZ])
    vis.add_geometry(logo_rect)

    # 添加标注点
    qr_point = o3d.geometry.PointCloud()
    qr_point.points = o3d.utility.Vector3dVector([[X, Y, Z]])
    qr_point.paint_uniform_color([0, 1, 0])  # 绿色
    vis.add_geometry(qr_point)

    logo_point = o3d.geometry.PointCloud()
    logo_point.points = o3d.utility.Vector3dVector([[LX, LY, LZ]])
    logo_point.paint_uniform_color([1, 0, 0])  # 红色
    vis.add_geometry(logo_point)

    # 渲染切割点和刀轴方向
    for point, direction in cutting_data:
        # 添加切割点
        cutting_point = o3d.geometry.PointCloud()
        cutting_point.points = o3d.utility.Vector3dVector([point])
        cutting_point.paint_uniform_color([1, 1, 0])  # 黄色
        vis.add_geometry(cutting_point)

        # 判断是刀轴方向还是四元素
        if len(direction) == 3:  # 刀轴方向
            # 添加刀轴方向
            line_set = o3d.geometry.LineSet()
            line_set.points = o3d.utility.Vector3dVector([point, np.array(point) + np.array(direction) * 3])  # 刀轴长度加长
            line_set.lines = o3d.utility.Vector2iVector([[0, 1]])
            line_set.colors = o3d.utility.Vector3dVector([[1, 0, 0]])  # 红色
            vis.add_geometry(line_set)
        elif len(direction) == 4:  # 四元素
            # 计算旋转矩阵
            q = np.array(direction)
            R = o3d.geometry.get_rotation_matrix_from_quaternion(q)
            # 计算刀轴方向的终点
            end_point = np.array(point) + R @ np.array([0, 0, 3])  # 假设刀轴方向沿Z轴，长度加长
            line_set = o3d.geometry.LineSet()
            line_set.points = o3d.utility.Vector3dVector([point, end_point])
            line_set.lines = o3d.utility.Vector2iVector([[0, 1]])
            line_set.colors = o3d.utility.Vector3dVector([[1, 0, 0]])  # 红色
            vis.add_geometry(line_set)

    # 设置视图
    vis.get_view_control().set_zoom(0.7)
    
    # 添加坐标信息
    vis.add_geometry(create_coordinate_text(f"QR Point: ({X:.2f}, {Y:.2f}, {Z:.2f})", [0, 1, 0]))
    vis.add_geometry(create_coordinate_text(f"LOGO Point: ({LX:.2f}, {LY:.2f}, {LZ:.2f})", [1, 0, 0]))

    # 运行可视化
    vis.run()
    vis.destroy_window()

def create_coordinate_text(text, color):
    # 创建3D文本（Open3D不直接支持2D文本叠加）
    text_geometry = o3d.geometry.TriangleMesh.create_coordinate_frame(size=0.1)
    return text_geometry

def main():
    xml_file_path, stl_file_path, txt_file_path = open_file_dialog("Select Files", [("XML files", "*.xml"), ("STL files", "*.stl"), ("TXT files", "*.txt")])
    
    if xml_file_path and stl_file_path and txt_file_path:
        X, Y, Z, LX, LY, LZ, A, LA = read_xml_data(xml_file_path)
        cutting_data = read_cutting_data(txt_file_path)
        render_stl_and_mark_points(stl_file_path, X, Y, Z, LX, LY, LZ, A, LA, cutting_data)

if __name__ == "__main__":
    main()
