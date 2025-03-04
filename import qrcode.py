import qrcode
from fpdf import FPDF
from PIL import Image
import os

def generate_qr_code(data, version=1, box_size=10, border=4, error_correction=qrcode.constants.ERROR_CORRECT_L):
    """
    生成二维码并返回二维码图像对象。
    
    参数:
    - data: 二维码包含的信息（例如URL或文本）
    - version: 二维码的版本，决定二维码的复杂度，1是最简单的
    - box_size: 每个二维码单元的像素大小
    - border: 二维码的边框宽度
    - error_correction: 错误修正级别，控制二维码的容错能力
    
    返回:
    - img: 生成的二维码图像
    """
    # 创建二维码对象
    qr = qrcode.QRCode(
        version=version,
        error_correction=error_correction,
        box_size=box_size,
        border=border
    )
    # 添加数据
    qr.add_data(data)
    qr.make(fit=True)

    # 生成二维码图像并返回
    img = qr.make_image(fill='black', back_color='white')
    return img


# 示例使用函数
data = "084442qr"
qr_image = generate_qr_code(data)

# 保存二维码图片
qr_image.save("qr_code.png")
print("QR Code generated and saved as 'qr_code.png'")



def insert_qr_to_pdf(pdf, qr_image_path, qr_width=30):
    """
    在现有PDF中插入二维码图片到右上角。

    参数:
    - pdf: FPDF对象，已经创建并添加页面的PDF
    - qr_image_path: 二维码图片的文件路径
    - qr_width: 二维码图片的宽度
    """
    # 获取PDF页面的宽度和高度
    pdf_width = pdf.w - 2 * pdf.l_margin  # 页面宽度减去左右边距
    pdf_height = pdf.h - 2 * pdf.t_margin  # 页面高度减去上下边距

    # 设置二维码的位置和大小，放置在右上角
    qr_x = pdf_width - qr_width - 10  # x位置：右边距为10
    qr_y = 10  # y位置：距离顶部10个单位

    # 插入二维码图片
    pdf.image(qr_image_path, x=qr_x, y=qr_y, w=qr_width)

# 创建PDF并插入二维码图片
pdf = FPDF()
pdf.add_page()
insert_qr_to_pdf(pdf,"qr_code.png")

# 保存PDF文件
pdf.output("qr_code_pdf.pdf")

# 删除二维码图片文件
os.remove("qr_code.png")

print("QR Code saved as PDF successfully!")
