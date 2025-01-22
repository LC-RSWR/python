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

    return X, Y, Z, LX, LY, LZ, A

# 3. 渲染STL模型并添加标注点
def render_stl_and_mark_points(stl_file_path, X, Y, Z, LX, LY, LZ, A):
    # 加载STL模型
    mesh = pv.read(stl_file_path)  # STL文件路径

    # 创建一个3D绘图环境
    plotter = pv.Plotter()

    # 渲染STL模型
    plotter.add_mesh(mesh, color="lightblue", show_edges=True)

    # 直接使用原始标注点 (无需旋转)
    plotter.add_points(np.array([[LX, LY, LZ]]), color="red", point_size=10)

    # 添加文字标注
    plotter.add_text(f"QR Point: ({LX:.2f}, {LY:.2f}, {LZ:.2f})", font_size=12, color='black')

    # 显示结果
    plotter.show()

# 主程序
def main():
    # 通过对话框选择XML和STL文件
    xml_file_path, stl_file_path = open_file_dialog()
    
    if xml_file_path and stl_file_path:
        # 从XML文件中读取数据
        X, Y, Z, LX, LY, LZ, A = read_xml_data(xml_file_path)

        # 渲染STL模型并添加标注点
        render_stl_and_mark_points(stl_file_path, X, Y, Z, LX, LY, LZ, A)

if __name__ == "__main__":
    main()
