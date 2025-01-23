import numpy as np
import pyvista as pv
import xml.etree.ElementTree as ET
from tkinter import Tk, filedialog
from math import radians

# 1. 打开文件选择对话框
def open_file_dialog():
    # 使用Tkinter创建一个隐藏的根窗口
    root = Tk()
    root.withdraw()  # 隐藏主窗口

    # 打开XML文件选择对话框
    xml_file_path = filedialog.askopenfilename(title="Select XML file", filetypes=(("XML files", "*.xml"), ("All files", "*.*")))
    if not xml_file_path:  # 用户取消选择
        print("No XML file selected.")
        return None, None
    
    # 打开STL文件选择对话框
    stl_file_path = filedialog.askopenfilename(title="Select STL file", filetypes=(("STL files", "*.stl"), ("All files", "*.*")))
    if not stl_file_path:  # 用户取消选择
        print("No STL file selected.")
        return None, None
    
    return xml_file_path, stl_file_path

# 2. 从XML文件读取数据
def read_xml_data(xml_file_path):
    # 解析XML文件
    tree = ET.parse(xml_file_path)
    root = tree.getroot()

    # 获取标注信息
    X = float(root.attrib['X'])
    Y = float(root.attrib['Y'])
    Z = float(root.attrib['Z'])  # 标注点的Z坐标
    LX = float(root.attrib['LX'])  # LX坐标
    LY = float(root.attrib['LY'])  # LY坐标
    LZ = float(root.attrib['LZ'])  # LZ坐标
    A = float(root.attrib['A'])  # 角度A，单位是度
    LA = float(root.attrib['LA'])  # 角度A，单位是度

    return X, Y, Z, LX, LY, LZ, A,LA

# 3. 渲染STL模型并添加标注点
def render_stl_and_mark_points(stl_file_path, X, Y, Z, LX, LY, LZ, A, LA):
    # 加载STL模型
    mesh = pv.read(stl_file_path)  # STL文件路径

    # 创建一个3D绘图环境，启用滑动条功能
    plotter = pv.Plotter()
    
    # 先渲染STL模型，设置半透明
    mesh_actor = plotter.add_mesh(mesh, color="lightblue", show_edges=True, opacity=0.8)
    
    # 添加透明度调节滑动条
    def update_opacity(value):
        mesh_actor.GetProperty().SetOpacity(value)
        plotter.render()  # 强制立即重新渲染
        
    plotter.add_slider_widget(
        callback=update_opacity,
        rng=[0, 1],  # 透明度范围从0到1
        value=0.8,   # 修改默认值为0.8
        title="Opacity",
        pointa=(0.02, 0.1),  # 滑动条起点位置
        pointb=(0.18, 0.1),  # 滑动条终点位置
        style='modern',
        event_type='always'  # 设置为始终触发事件
    )

    # 创建QR码矩形框（8mm x 4mm）
    qr_width, qr_height = 8, 4  # 单位：mm
    qr_corners = np.array([
        [-qr_width/2, -qr_height/2, 0],
        [qr_width/2, -qr_height/2, 0],
        [qr_width/2, qr_height/2, 0],
        [-qr_width/2, qr_height/2, 0]
    ])
    
    # 创建LOGO矩形框（4mm x 4mm）
    logo_size = 4  # 单位：mm
    logo_corners = np.array([
        [-logo_size/2, -logo_size/2, 0],
        [logo_size/2, -logo_size/2, 0],
        [logo_size/2, logo_size/2, 0],
        [-logo_size/2, logo_size/2, 0]
    ])

    # 创建QR码的旋转矩阵（与Y轴的夹角）
    qr_angle_rad = np.radians(90 - A)  # 将与Y轴夹角转换为与X轴夹角，并取负
    qr_rotation_matrix = np.array([
        [np.cos(qr_angle_rad), -np.sin(qr_angle_rad), 0],
        [np.sin(qr_angle_rad), np.cos(qr_angle_rad), 0],
        [0, 0, 1]
    ])

    # 创建LOGO的旋转矩阵（与Y轴的夹角）
    logo_angle_rad = np.radians(90 - LA)  # 将与Y轴夹角转换为与X轴夹角，并取负
    logo_rotation_matrix = np.array([
        [np.cos(logo_angle_rad), -np.sin(logo_angle_rad), 0],
        [np.sin(logo_angle_rad), np.cos(logo_angle_rad), 0],
        [0, 0, 1]
    ])

    # 分别旋转并平移矩形框
    qr_corners = np.dot(qr_corners, qr_rotation_matrix.T)
    qr_corners = qr_corners + np.array([X, Y, Z])
    
    logo_corners = np.dot(logo_corners, logo_rotation_matrix.T)
    logo_corners = logo_corners + np.array([LX, LY, LZ])

    # 添加QR码矩形框
    qr_rect = np.vstack((qr_corners, qr_corners[0]))  # 闭合矩形
    qr_line = pv.lines_from_points(qr_rect)
    plotter.add_mesh(qr_line, color="green", line_width=5, render_lines_as_tubes=True)

    # 添加LOGO矩形框
    logo_rect = np.vstack((logo_corners, logo_corners[0]))  # 闭合矩形
    logo_line = pv.lines_from_points(logo_rect)
    plotter.add_mesh(logo_line, color="red", line_width=5, render_lines_as_tubes=True)

    # 添加标注点
    plotter.add_points(np.array([[LX, LY, LZ]]), color="red", point_size=20, render_points_as_spheres=True)
    plotter.add_points(np.array([[X, Y, Z]]), color="green", point_size=20, render_points_as_spheres=True)

    # 添加文字标注，使用viewport坐标系统（0-1范围）
    plotter.add_text(f"LOGO Point:\n({LX:.2f}, {LY:.2f}, {LZ:.2f})", 
                    position=(0.02, 0.90),  # 左上角，左边距2%，顶部距离5%
                    font_size=12, 
                    color='red',
                    shadow=True,
                    viewport=True)  # 确保使用viewport坐标系

    plotter.add_text(f"QR Point:\n({X:.2f}, {Y:.2f}, {Z:.2f})", 
                    position=(0.02, 0.80),  # 在LOGO Point下方，左边距2%
                    font_size=12, 
                    color='green',
                    shadow=True,
                    viewport=True)  # 确保使用viewport坐标系

    # 显示结果
    plotter.show()

# 主程序
def main():
    # 通过对话框选择XML和STL文件
    xml_file_path, stl_file_path = open_file_dialog()
    
    if xml_file_path and stl_file_path:
        # 从XML文件中读取数据
        X, Y, Z, LX, LY, LZ, A, LA = read_xml_data(xml_file_path)
        # 渲染STL模型并添加标注点
        render_stl_and_mark_points(stl_file_path, X, Y, Z, LX, LY, LZ, A, LA)

if __name__ == "__main__":
    main()
