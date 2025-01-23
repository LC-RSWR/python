import os
import numpy as np
import open3d as o3d
import xml.etree.ElementTree as ET
from PyQt5.QtWidgets import QApplication, QMainWindow, QSlider, QLabel, QVBoxLayout, QWidget, QComboBox, QFileDialog
from PyQt5.QtCore import Qt, QTimer  # 导入 Qt 和 QTimer

# 1. 打开文件选择对话框
def open_file_dialog():
    root = Tk()
    root.withdraw()

    xml_file_path = filedialog.askopenfilename(title="Select XML file", filetypes=(("XML files", "*.xml"), ("All files", "*.*")))
    if not xml_file_path:
        print("No XML file selected.")
        return None, None
    
    stl_file_path = filedialog.askopenfilename(title="Select STL file", filetypes=(("STL files", "*.stl"), ("All files", "*.*")))
    if not stl_file_path:
        print("No STL file selected.")
        return None, None
    
    txt_file_path = filedialog.askopenfilename(title="Select TXT file", filetypes=(("TXT files", "*.txt"), ("All files", "*.*")))
    if not txt_file_path:
        print("No TXT file selected.")
        return None, None
    
    return xml_file_path, stl_file_path, txt_file_path

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
    with open(txt_file_path, 'r') as file:
        lines = file.readlines()
        cutting_points = []
        for line in lines:
            parts = line.strip().split()
            if len(parts) == 6:
                point = list(map(float, parts[:3]))  # 切割点位置
                direction = list(map(float, parts[3:]))  # 刀轴方向
                cutting_points.append((point, direction))
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
def render_stl_and_mark_points(vis, stl_file_path, X, Y, Z, LX, LY, LZ, A, LA, cutting_data):
    # 清除之前的几何体
    vis.clear_geometries()

    # 加载STL模型
    mesh = o3d.io.read_triangle_mesh(stl_file_path)
    mesh.compute_vertex_normals()
    mesh.paint_uniform_color([0.7, 0.8, 1.0])  # 浅蓝色

    # 添加网格模型
    vis.add_geometry(mesh)

    # 创建QR码矩形框
    qr_rect = create_rectangle(8, 4, [0, 1, 0])  # 绿色，8mm x 4mm
    qr_angle_rad = np.radians(90 - A)
    R_qr = qr_rect.get_rotation_matrix_from_xyz([0, 0, qr_angle_rad])
    qr_rect.rotate(R_qr, center=[0, 0, 0])
    qr_rect.translate([X, Y, Z])
    vis.add_geometry(qr_rect)

    # 创建LOGO矩形框
    logo_rect = create_rectangle(4, 4, [1, 0, 0])  # 红色，4mm x 4mm
    logo_angle_rad = np.radians(90 - LA)
    R_logo = logo_rect.get_rotation_matrix_from_xyz([0, 0, logo_angle_rad])
    logo_rect.rotate(R_logo, center=[0, 0, 0])
    logo_rect.translate([LX, LY, LZ])
    vis.add_geometry(logo_rect)

    # 添加标注点（使用小球体代替点云）
    qr_sphere = o3d.geometry.TriangleMesh.create_sphere(radius=0.5)  # 半径为0.5的球体
    qr_sphere.translate([X, Y, Z])
    qr_sphere.paint_uniform_color([0, 1, 0])  # 绿色
    vis.add_geometry(qr_sphere)

    logo_sphere = o3d.geometry.TriangleMesh.create_sphere(radius=0.5)  # 半径为0.5的球体
    logo_sphere.translate([LX, LY, LZ])
    logo_sphere.paint_uniform_color([1, 0, 0])  # 红色
    vis.add_geometry(logo_sphere)

    # 渲染切割点和刀轴方向
    for point, direction in cutting_data:
        # 添加切割点
        cutting_point = o3d.geometry.PointCloud()
        cutting_point.points = o3d.utility.Vector3dVector([point])
        cutting_point.paint_uniform_color([1, 1, 0])  # 黄色
        vis.add_geometry(cutting_point)

        # 判断是刀轴方向还是四元素
        if len(direction) == 3:  # 刀轴方向
            line_set = o3d.geometry.LineSet()
            line_set.points = o3d.utility.Vector3dVector([point, np.array(point) + np.array(direction) * 5])  # 刀轴长度加长
            line_set.lines = o3d.utility.Vector2iVector([[0, 1]])
            line_set.colors = o3d.utility.Vector3dVector([[1, 0, 0]])  # 红色
            vis.add_geometry(line_set)
        elif len(direction) == 4:  # 四元素
            q = np.array(direction)
            R = o3d.geometry.get_rotation_matrix_from_quaternion(q)
            end_point = np.array(point) + R @ np.array([0, 0, 5])  # 假设刀轴方向沿Z轴，长度加长
            line_set = o3d.geometry.LineSet()
            line_set.points = o3d.utility.Vector3dVector([point, end_point])
            line_set.lines = o3d.utility.Vector2iVector([[0, 1]])
            line_set.colors = o3d.utility.Vector3dVector([[1, 0, 0]])  # 红色
            vis.add_geometry(line_set)

    # 设置视图
    vis.get_view_control().set_zoom(0.8)

    # 添加坐标信息
    vis.add_geometry(create_coordinate_text(f"QR Point: ({X:.2f}, {Y:.2f}, {Z:.2f})", [0, 1, 0]))
    vis.add_geometry(create_coordinate_text(f"LOGO Point: ({LX:.2f}, {LY:.2f}, {LZ:.2f})", [1, 0, 0]))

def create_coordinate_text(text, color):
    # 创建3D文本（Open3D不直接支持2D文本叠加）
    text_geometry = o3d.geometry.TriangleMesh.create_coordinate_frame(size=0.1)
    return text_geometry

# 1. 打开文件夹并列出所有匹配的文件
def list_files_in_directory(directory):
    steps = {}
    
    # 首先收集所有 STL 文件
    for filename in os.listdir(directory):
        if filename.endswith(".stl"):
            base_name = filename.replace(".stl", "")  # 获取基础名称，例如 211207U01A
            steps[base_name] = [None, os.path.join(directory, filename), None]  # 初始化步骤，添加 STL 文件

    # 然后收集对应的 XML 和 TXT 文件
    for filename in os.listdir(directory):
        if filename.endswith("_Q.xml"):
            base_name = filename.replace("_Q.xml", "")  # 获取基础名称，例如 211207U01A
            if base_name in steps:
                steps[base_name][0] = os.path.join(directory, filename)  # 更新 XML 文件
        elif filename.endswith("_N.txt"):  # 只读取以 _N.txt 结尾的文件
            base_name = filename.replace("_N.txt", "")  # 获取基础名称，例如 211207U01A
            if base_name in steps:
                steps[base_name][2] = os.path.join(directory, filename)  # 更新 TXT 文件

    # 过滤出完整的步骤
    complete_steps = [step for step in steps.values() if all(step)]
    
    return complete_steps

# 3. 创建主窗口
class MainWindow(QMainWindow):
    def __init__(self, directory, steps):
        super().__init__()
        self.setWindowTitle("加工轨迹、打标查看器")
        self.setGeometry(100, 100, 800, 600)

        # 创建滑动条
        self.slider = QSlider(Qt.Horizontal, self)  # 使用 Qt.Horizontal
        self.slider.setRange(0, len(steps) - 1)
        self.slider.sliderReleased.connect(self.update_model)

        # 创建下拉框
        self.combo_box = QComboBox(self)
        self.combo_box.addItems([f"步骤 {i + 1}: {os.path.basename(step[1])}" for i, step in enumerate(steps)])  # 添加步骤索引和文件名
        self.combo_box.currentIndexChanged.connect(self.update_from_combobox)

        # 创建标签
        self.label = QLabel("选择步骤", self)

        # 创建当前选中的 STL 文件名标签
        self.stl_label = QLabel("当前 STL 文件: ", self)  # 新增标签

        # 布局
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.slider)
        layout.addWidget(self.combo_box)  # 添加下拉框到布局
        layout.addWidget(self.stl_label)  # 添加 STL 文件名标签到布局

        # 创建一个 QWidget 并设置布局
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Open3D 可视化
        self.vis = o3d.visualization.Visualizer()
        self.vis.create_window(window_name="Open3D Viewer", width=1280, height=768)

        self.steps = steps
        self.load_files(0)  # 加载初始步骤

        # 定时器设置
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_view)
        self.timer.start(100)  # 每100毫秒更新一次视图
    
    def closeEvent(self, event):
        self.timer.stop()  # 停止定时器
        self.vis.destroy_window()  # 销毁可视化窗口
        event.accept()  # 接受关闭事件

    def load_files(self, index):
        xml_file_path, stl_file_path, txt_file_path = self.steps[index]
        X, Y, Z, LX, LY, LZ, A, LA = read_xml_data(xml_file_path)
        cutting_data = read_cutting_data(txt_file_path)
        render_stl_and_mark_points(self.vis, stl_file_path, X, Y, Z, LX, LY, LZ, A, LA, cutting_data)

        # 更新当前 STL 文件名标签
        self.stl_label.setText(f"当前 STL 文件: {os.path.basename(stl_file_path)}")  # 显示文件名

    def update_model(self):
        index = self.slider.value()
        self.load_files(index)
        self.combo_box.setCurrentIndex(index)  # 更新下拉框的索引

    def update_from_combobox(self):
        index = self.combo_box.currentIndex()
        self.load_files(index)
        self.slider.setValue(index)  # 更新滑动条的值

    def update_view(self):
        self.vis.poll_events()  # 处理事件
        self.vis.update_renderer()  # 更新渲染器

    def run(self):
        self.vis.run()
        self.vis.destroy_window()

def main(directory):
    steps = list_files_in_directory(directory)
    app = QApplication([])
    window = MainWindow(directory, steps)
    window.show()
    app.exec_()  # 启动应用程序

if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication, QFileDialog

    app = QApplication(sys.argv)  # 创建 QApplication 实例

    if len(sys.argv) < 2:
        folder_path = QFileDialog.getExistingDirectory(None, "选择文件夹")  # 弹出选择文件夹对话框
        if folder_path:  # 如果用户选择了文件夹
            main(folder_path)
        else:
            print("未选择文件夹，程序将退出。")
            sys.exit(1)  # 退出程序
    else:
        main(sys.argv[1])
    #main(r"C:\Users\deskadmin\Desktop\211207")
