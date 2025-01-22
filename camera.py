import cv2
import time

# 创建VideoCapture对象，0表示默认摄像头
cap = cv2.VideoCapture(0)

# 设置视频编解码器和输出文件名
fourcc = cv2.VideoWriter_fourcc(*'XVID')
output_filename = 'output.avi'
out = cv2.VideoWriter(output_filename, fourcc, 20.0, (640, 480))

# 开始录制
while(cap.isOpened()):
    ret, frame = cap.read()
    if ret==True:
        out.write(frame)
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

# 释放资源
cap.release()
out.release()
cv2.destroyAllWindows()
