import os
from io import BytesIO
import PyPDF2
from PIL import Image
def pdf_to_images(file_path, output_folder):
    # 打开PDF文件
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        # 遍历每一页
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            # 将PDF页转换为Pillow Image对象
            img = page_to_image(page)
            # 保存图片到文件夹
            save_image(img, page_num, output_folder)
def page_to_image(page):
    # 获取PDF页的尺寸
    page_size = page.mediabox
    # 创建空白的Pillow Image对象
    img = Image.new('RGB', (int(page_size.width), int(page_size.height)), 'white')
    return img
def save_image(img, page_num, output_folder):
    # 创建输出文件夹
    if not os.path.exists(output_folder):
        os.makedirs(output_folder, exist_ok=True)
    # 保存图片到输出文件夹
    file_path = os.path.join(output_folder, f'{page_num}.png')
    img.save(file_path)
# 使用示例
pdf_file = "C:/Users/deskadmin/Desktop/012402010001/overViewFile.pdf"
pdf_to_images(pdf_file, 'C:/Users/deskadmin/Desktop/012402010001')