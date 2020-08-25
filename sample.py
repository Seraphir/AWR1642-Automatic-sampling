import cv2.cv2 as cv2
import time
import os
import win32gui
import win32api
import win32con

# pywin32 安装：
# pip install pypiwin32


def show_window_attr(hWnd):
    if not hWnd:
        return
    title = win32gui.GetWindowText(hWnd)
    clsname = win32gui.GetClassName(hWnd)
    print('窗口句柄:%s ' % (hWnd))
    print('窗口标题:%s' % (title))
    print('窗口类名:%s' % (clsname))
    print('')


# 配置摄像头和编码器
source = 0
cameraCapture = cv2.VideoCapture(source, cv2.CAP_DSHOW)  # 传入0代表0号摄像头
print(cameraCapture.isOpened())
if cameraCapture is None or not cameraCapture.isOpened():
    print('Warning: unable to open video source: ', source)
fps = 25  # 采集帧率设置
frame_num = 32  # 采集帧数
size = (int(cameraCapture.get(cv2.CAP_PROP_FRAME_WIDTH)),
        int(cameraCapture.get(cv2.CAP_PROP_FRAME_HEIGHT)))
fourcc = cv2.VideoWriter_fourcc("X", "V", "I", "D")
print(size)

# 获取窗口句柄
hWndList = []
win32gui.EnumWindows(lambda hWnd, param: param.append(hWnd), hWndList)
hwnd = None
for h in hWndList:
    title = win32gui.GetWindowText(h)
    if "mmWave" in title and "Studio" in title and not ("Radar"
                                                        in title):  #根据标题搜索窗口句柄
        show_window_attr(h)
        hwnd = h

# 开始批量采集
store_dir = ".\\store"
if not os.path.exists(store_dir):
    os.makedirs(store_dir)
max_times = 2500
start = 0
while True:
    try:
        start = eval(input("请输入从第几次采集开始（范围：0-{}）：".format(max_times - 1)))
        if 0 <= start < max_times:
            print("从第{}次开始采集".format(start))
            break
        else:
            print("超出范围，请重新输入")
    except:
        print("请重新输入")

print("请配置好上位机")
for idx in range(start, max_times):
    input("上位机准备后按任意键开始第{:04d}次采集".format(idx))
    # 配置视频输出
    output_video = os.path.join(store_dir, "{:04d}.avi".format(idx))
    videoWriter = cv2.VideoWriter(output_video, fourcc, fps, size)
    # 显示隐藏窗口
    if (win32gui.IsIconic(hwnd)):
        # win32gui.ShowWindow(hwnd, win32con.SW_SHOWNORMAL)
        win32gui.ShowWindow(hwnd, 4)
        time.sleep(0.5)
    # 需要先对当前窗口发送指令，才能激活特定窗口（win32com的bug）
    win32api.keybd_event(18, 0, 0, 0)  # 按下Alt（ASCII 18）
    win32api.keybd_event(18, 0, win32con.KEYEVENTF_KEYUP, 0)  # 松开Alt（ASCII 18）
    win32gui.SetForegroundWindow(hwnd)  # 置于顶层（目标窗口不能最小化或隐藏）
    win32api.keybd_event(13, 0, 0, 0)  # 按下回车（ASCII 13）
    win32api.keybd_event(13, 0, win32con.KEYEVENTF_KEYUP, 0)  # 松开回车（ASCII 13）
    print("第{:04d}次采集开始...".format(idx))

    # 采集摄像头数据并输出
    numFramesRemaining = frame_num - 1  # 计算剩余需要采集的帧数
    ret = True
    while ret and numFramesRemaining:
        t0 = time.time()
        ret, frame = cameraCapture.read()
        videoWriter.write(frame)
        numFramesRemaining -= 1
        dt = time.time() - t0
        # cv2.imshow("0",frame)
        # cv2.waitKey(10) # 等待下一帧（帧率过高会来不及储存，导致帧率不稳定）
        time.sleep(max(1 / fps - dt, 0))  # 等待下一帧（帧率过高会来不及储存，导致帧率不稳定）

    filename = os.path.join(store_dir, "temp")
    if not os.path.exists(filename):
        f = open(filename, "w+")
        f.close()
    os.rename(filename, os.path.join(store_dir, "{:04d}".format(idx)))

cameraCapture.release()