import pygame, sys
#from pygame.locals import
# 初始化pygame
pygame.init()
# 设置窗口的大小，单位为像素
screen = pygame.display.set_mode((500,400), 0, 32)
# 设置窗口的标题
pygame.display.set_caption('用户事件监控')
# 设置背景
screen.fill((255, 255, 255))
# 程序主循环
while True:
  # 获取事件
  for event in pygame.event.get():
    # 判断事件是否为退出事件
    if event.type == QUIT:
      print("00")
      # 退出pygame
      #pygame.quit()
      # 退出系统
      #sys.exit()
    # 获得键盘按下的事件  
    if event.type == KEYDOWN:
      if(event.key==K_UP or event.key==K_w):
        print("上")
      if(event.key==K_DOWN or event.key==K_s):
        print("下")
      if(event.key==K_LEFT or event.key==K_a):
        print("左")
      if(event.key==K_RIGHT or event.key==K_d):
        print("右")
      # 按下键盘的Esc键退出
      if(event.key==K_ESCAPE):
        # 退出pygame
        pygame.quit()
        # 退出系统
        sys.exit()
    # 获得鼠标当前的位置  
    if event.type ==MOUSEMOTION:
      print(event.pos)
    # 获得鼠标按下的位置
    if event.type ==MOUSEBUTTONDOWN:
      print("鼠标按下：", event.pos)
    # 获得鼠标抬起的位置
    if event.type ==MOUSEBUTTONUP:
      print("鼠标抬起：", event.pos) 
  # 绘制屏幕内容
  pygame.display.update()
