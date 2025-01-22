
# 设置输入PDF文件路径
pdf_file = "C:/Users/deskadmin/Desktop/012402010001/overViewFile.pdf"
import fitz  # pip install pymupdf -i https://pypi.tuna.tsinghua.edu.cn/simple/
import os

def pdf2img(pdf_path, zoom_x, zoom_y):
    """
    参数说明
    :param pdf_path: pdf文件的路径
    :param zoom_x: x轴方向的缩放系数
    :param zoom_y: y轴方向的缩放系数
    """
    doc = fitz.open(pdf_path)  # 打开pdf文件
    for page in doc:  # 逐页循环
        pic = page.get_pixmap(matrix=fitz.Matrix(zoom_x, zoom_y))  # 将页面渲染为图片
        dir_save = os.path.dirname(pdf_path)  # 结果保存的路径与pdf文件所在的路径同级
        pdf_name = os.path.basename(pdf_path).split('.pdf')[0]
        pic.save(f'{dir_save}/{pdf_name}-page-{page.number+1}.png')  # 逐页将pdf存储为PNG格式
    doc.close()  # 关闭读取pdf文件

pdf2img(
    pdf_file,
    zoom_x=3,
    zoom_y=3
)
