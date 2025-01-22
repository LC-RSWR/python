from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors

# 创建PDF文件
doc = SimpleDocTemplate("table_example.pdf", pagesize=letter)

# 创建数据
data = [['Name', 'Age', 'Country'],
        ['Alice', 25, 'USA'],
        ['Bob', 30, 'Canada'],
        ['Charlie', 22, 'UK']]

# 创建表格
table = Table(data)

# 添加样式
style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)])

table.setStyle(style)

# 构建PDF文件
elements = []
elements.append(table)
doc.build(elements)

