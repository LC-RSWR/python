import pyautogui as p
import time
import os 

document_x = 1774  #点击创建订单按钮
document_y = 319
p.click(document_x, document_y)
time.sleep(1)  # 程序会暂停运行1秒钟
# 输入患者姓名
text_to_type = "Hello"
p.typewrite(text_to_type)#写患者姓名
document_x = 1198       #点选择性别按钮'''
document_y = 507
p.click(document_x, document_y)
time.sleep(1)  # 程序会暂停运行1秒钟

document_x = 674       #点出生日期按钮'''
document_y = 570
p.click(document_x, document_y)   
time.sleep(1)  # 程序会暂停运行1秒钟

document_x = 1034       #点出生日期按钮'''
document_y = 558
p.click(document_x, document_y)
time.sleep(1)  # 程序会暂停运行1秒钟

document_x = 677       #点门诊医院按钮'''
document_y = 635
p.click(document_x, document_y)
time.sleep(1)  # 程序会暂停运行1秒钟  

document_x = 675       #点门诊医院按钮'''
document_y = 704
p.click(document_x, document_y)
time.sleep(1)  # 程序会暂停运行1秒钟

document_x = 1368       #点门诊医院按钮'''
document_y = 904
p.click(document_x, document_y)
time.sleep(1)  # 程序会暂停运行1秒钟

document_x = 1314       #点矫治器系列按钮'''
document_y = 582
p.click(document_x, document_y)
time.sleep(1)  # 程序会暂停运行1秒钟

document_x = 991       #点确定按钮'''
document_y = 941
p.click(document_x, document_y)
time.sleep(1)  # 程序会暂停运行1秒钟

#####开始导入照片###############

document_x = 1607       #点本地导入按钮'''
document_y = 468
p.click(document_x, document_y)
time.sleep(1)  # 程序会暂停运行1秒钟

document_x = 786       #点文件夹路径
document_y = 154
p.click(document_x, document_y)
time.sleep(2)  # 程序会暂停运行1秒钟
text_to_type = r"C:\Users\fengshuang-ls\Desktop\shuju\huanze"
p.typewrite(text_to_type)#写患者姓名
time.sleep(3)  # 程序会暂停运行1秒钟C:\Users\fengshuang-ls\Desktop\shuju\huanze