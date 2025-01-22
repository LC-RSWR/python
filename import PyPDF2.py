from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# 创建PDF文件
c = canvas.Canvas("reportlab_example.pdf", pagesize=letter)

# 添加文本
c.drawString(100, 750, "Hello, World!")

# 添加图像
#c.drawImage("德甲.png", 100, 600, width=200, height=100)

# 保存生成的PDF文件
c.save()


