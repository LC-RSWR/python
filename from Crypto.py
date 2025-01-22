import win32api
import win32con
hid = win32gui.WindowFromPoint((100, 100))
# 获取窗口标题
title = win32gui.GetWindowText(hid)
# 获取窗口类名
class_name = win32gui.GetClassName(hid)
# 模拟鼠标在(400, 500)位置进行点击操作
point = (400, 500)
win32api.SetCursorPos(point)
win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

