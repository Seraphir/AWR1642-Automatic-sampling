import time
import os


# 数据存储路径
store_dir = "D:\\radardata"
# 需要重命名的文件名
filetype_list=["adc_data_Raw_0.bin"]
# 默认重命名之后的文件名为"XXXX_原文件名"，可根据需要在第35行os.rename()函数处修改

max_times = 2500
start = 0

if not os.path.exists(store_dir):
    os.makedirs(store_dir)

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

print("请开始使用上位机进行采集")
print("按下“DCA1000 ARM”和“Trigger Frame”并等待采集完成视为完成一次采集")
for idx in range(start, max_times):
    input("上位机完成第{:04d}次采集后按回车自动修改文件名".format(idx))
    time.sleep(2) # 延时以防上位机未解除文件占用，可根据实际情况修改
    for filetype in filetype_list:
        filename = os.path.join(store_dir, filetype)
        os.rename(filename, os.path.join(store_dir, "{:04d}_{}".format(idx, filetype)))
