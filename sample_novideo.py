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


## 获取窗口句柄
hWndList = []
win32gui.EnumWindows(lambda hWnd, param: param.append(hWnd), hWndList)
hwnd = None
for h in hWndList:
    title = win32gui.GetWindowText(h)
    if "mmWave" in title and "Studio" in title and not ("Radar"
                                                        in title):  #根据标题搜索窗口句柄
        show_window_attr(h)
        hwnd = h

## 开始批量采集
# 文件存储路径
store_dir = "D:\\radardata"
# 需要连续修改的文件名
# filetype_list=["adc_data_CP_0.bin","adc_data_CQ_0.bin","adc_data_DSP_0.bin","adc_data_LogFile.txt","adc_data_R4F_0.bin","adc_data_Raw_0.bin"]
filetype_list=["adc_data_Raw_0.bin"]
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
    input("按下 “DCA1000 ARM” 后按回车开始第{:04d}次采集".format(idx))
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

    # 重命名指定文件
    time.sleep(3)
    for filetype in filetype_list:
        filename = os.path.join(store_dir, filetype)
        os.rename(filename, os.path.join(store_dir, "{:04d}_{}".format(idx, filetype)))
    
    print("第{:04d}次采集完成并已重命名".format(idx))