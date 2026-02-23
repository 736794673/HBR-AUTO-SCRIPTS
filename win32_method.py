import win32gui, win32ui, win32con,win32api,os
from  property import Property
from ctypes import windll
from PIL import  Image
import re
from  base64 import b64encode,b64decode
#需要有，不然窗口显示不全
import pyautogui
from wmi import  WMI
import cv2
import  uuid
import numpy
import pynput.mouse as pm
import threading
import time,datetime
import subprocess as sp
from pymem import Pymem
child_windows = []
from tkinter import messagebox,Tk
myProperty=property()
def adb_click(center):
    if center is None:
        return False
    elif  center is not None:
        sp.Popen(f"adb shell input tap {center[0]} {center[1]}")
        return True
def get_window_item_center_by_text(hwnd=0,text='',classtype='',match=0):
    def enum_child_windows(hwnd, lParam):
        child_windows.append(hwnd)
        return True
    print(hwnd,'所有控件:')
    child_windows=[]
    win32gui.EnumChildWindows(hwnd, enum_child_windows, None)
    left, top, right, bot = win32gui.GetWindowRect(hwnd)
    print()
    if match==1:
        for child_handle in child_windows:
            class_name = win32gui.GetClassName(child_handle)
            txt = win32gui.GetWindowText(child_handle)
            rect = win32gui.GetWindowRect(child_handle)
            if text == txt:
                print("控件类名：", class_name)
                print("控件文本：", text)
                print("控件位置：", rect)
                center=[(rect[0]+rect[2])/2-left,(rect[1]+rect[3])/2-top]

                return center
    for child_handle in child_windows:
        class_name = win32gui.GetClassName(child_handle)
        txt = win32gui.GetWindowText(child_handle)
        rect = win32gui.GetWindowRect(child_handle)
        if text in txt:
            print("控件类名：", class_name)
            print("控件文本：", txt)
            print("控件位置：", rect)
            center=[(rect[0]+rect[2])/2-left,(rect[1]+rect[3])/2-top]
            print(center)
            return center
    print('未找到控件',text)
    return None
def show_windows_items(hwnd=0,text='',classtype=''):
    child_windows=[]
    def enum_child_windows(hwnd, lParam):
        child_windows.append(hwnd)
        return True
    win32gui.EnumChildWindows(hwnd, enum_child_windows, None)
    for child_handle in child_windows:
        class_name = win32gui.GetClassName(child_handle)
        txt = win32gui.GetWindowText(child_handle)
        rect = win32gui.GetWindowRect(child_handle)
        if text==txt:
            print("控件类名：", class_name)
            print("控件文本：", txt)
            print("控件位置：", rect)
            center=[(rect[0]+rect[2])/2,(rect[1]+rect[3])/2]
            return center
#获取鼠标点击坐标
def analyse_pic_thread():
    def on_click(x, y, button, pressed):
    # 监听鼠标点击
        if pressed:
            print("按下坐标")
            mxy="{},{}".format(x, y)
            print(mxy)
            print(button)
        if not pressed:
        # Stop listener
            return False
    def ls_k_thread():
        while(1):
            with pm.Listener(on_click=on_click) as pmlistener:
                pmlistener.join()
    r = threading.Thread(target=ls_k_thread)
    r.start()
def get_window_pos_size(hwnd,maxerrorcount=10):#唤醒前台
    count=0
    while(1):
        if hwnd==0:
            print('无效句柄',hwnd,'可能未找到目标窗口句柄')
            return -1, -1, -1, -1
        else:
            try:
                #invoke_window_EX(hwnd)
                hwnd = win32gui.GetForegroundWindow()
                window_rect = win32gui.GetWindowRect(hwnd)

                x = window_rect[0]
                y = window_rect[1]
                width = window_rect[2] - x
                height = window_rect[3] - y
                return x, y, width, height
            except Exception:
                print('获取窗口信息失败,正在重试')
                count+=1
                time.sleep(1)
                if count==maxerrorcount:
                    print('达到最大错误数')
                    return  -1, -1, -1, -1
class Timeline(threading.Thread):
    def __init__(self,myProperty=Property()):
        threading.Thread.__init__(self)
        self.maxruntime=myProperty.runtime*60
    def run(self):
        print('运行时长检测线程已开启\n')
        start=time.time()
        while(1):
            time.sleep(5)
            end=time.time()
            if end-start>self.maxruntime:
                os.system("shutdown -s -t 60")
                top=Tk()
                top.withdraw()
                isCancel=messagebox.askquestion('提示:60秒后关机', '是否取消关机')
                if isCancel=='no':
                    exit(0)
                    pass
                else:
                    os.system("shutdown -a")
                    return
def get_window_shot(hWnd=0,name='',path='logpictures/',left=0,top=0,width=1400,height=810,save=1):
    '''0整个窗口，1客户区，'''
    #获取后台窗口的句柄，注意后台窗口不能最小化
    def get_all_hwnd(hwnd, mouse):
        if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
            hwnd_title.update({hwnd: win32gui.GetWindowText(hwnd)})
    hwnd_map = {}
    hwnd_title = dict()
    win32gui.EnumWindows(get_all_hwnd, 0)
    if hWnd==0:
        for title in hwnd_title.items():
            #if '命运-冠位指定' in title[1] and '模拟器' in title[1]:
            if name == title[1]:
                hWnd=title[0]
                print(hWnd,title[1])
#     #获取句柄窗口的大小信息
    left, top, right, bot = win32gui.GetWindowRect(hWnd)
    width = right - left
    height = bot - top
    #返回句柄窗口的设备环境，覆盖整个窗口，包括非客户区，标题栏，菜单，边框
    hWndDC = win32gui.GetWindowDC(hWnd)
    print(hWndDC)
    #创建设备描述表
    mfcDC = win32ui.CreateDCFromHandle(hWndDC)
    #创建内存设备描述表
    saveDC = mfcDC.CreateCompatibleDC()
    #创建位图对象准备保存图片
    saveBitMap = win32ui.CreateBitmap()
    #为bitmap开辟存储空间
    saveBitMap.CreateCompatibleBitmap(mfcDC,width,height)
    #将截图保存到saveBitMap中
    saveDC.SelectObject(saveBitMap)
    #保存bitmap到内存设备描述表
    saveDC.BitBlt((0,0), (width,height), mfcDC, (left,top), win32con.SRCCOPY)

    #如果要截图到打印设备：
    ###最后一个int参数：0-保存整个窗口，1-只保存客户区。如果PrintWindow成功函数返回值为1
#****
    result = windll.user32.PrintWindow(hWnd,saveDC.GetSafeHdc(),save)
    print(result) #PrintWindow成功则输出1
    saveBitMap.SaveBitmapFile(saveDC,path)


    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hWnd,hWndDC)
def get_center_confidence_locateonwindow(hWnd=0,confid=0.8,name='',templatePath='',left=0,top=0,width=1400,height=810):
    ##获取后台窗口的句柄，注意后台窗口不能最小化
    def get_all_hwnd(hwnd, mouse):
        if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
            hwnd_title.update({hwnd: win32gui.GetWindowText(hwnd)})
    hwnd_map = {}
    hwnd_title = dict()
    win32gui.EnumWindows(get_all_hwnd, 0)
    if hWnd==0:
        for title in hwnd_title.items():
            #if '命运-冠位指定' in title[1] and '模拟器' in title[1]:
            if name in title[1]:
                hWnd=title[0]
                # print(hWnd,title[1])
    #获取句柄窗口的大小信息

    left, top, right, bot = win32gui.GetWindowRect(hWnd)
    width = right - left
    height = bot - top
    win32gui.ShowWindow(hWnd, win32con.SW_SHOWNORMAL)
    #返回句柄窗口的设备环境，覆盖整个窗口，包括非客户区，标题栏，菜单，边框
    hWndDC = win32gui.GetWindowDC(hWnd)
    #创建设备描述表
    mfcDC = win32ui.CreateDCFromHandle(hWndDC)
    #创建内存设备描述表
    saveDC = mfcDC.CreateCompatibleDC()
    #创建位图对象准备保存图片
    saveBitMap = win32ui.CreateBitmap()
    #为bitmap开辟存储空间
    saveBitMap.CreateCompatibleBitmap(mfcDC,width,height)
    #将截图保存到saveBitMap中
    saveDC.SelectObject(saveBitMap)
    #保存bitmap到内存设备描述表
    saveDC.BitBlt((0,0), (width,height), mfcDC, (left,top), win32con.SRCCOPY)
        #x,y相反  -0-（y,x）
    result = windll.user32.PrintWindow(hWnd,saveDC.GetSafeHdc(),1)
     # 将位图转换为OpenCV格式的数组
    signedIntsArray = saveBitMap.GetBitmapBits(True)
    im_opencv = numpy.frombuffer(signedIntsArray, dtype = 'uint8')
    im_opencv.shape = (height, width, 4)

    im_opencv = cv2.cvtColor(im_opencv, cv2.COLOR_BGRA2RGB)
    # #显示原图
    # cv2.imshow(f"imgRec{templatePath}",im_opencv)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    template=cv2.imread(templatePath)
    template = cv2.cvtColor(template, cv2.COLOR_BGRA2RGB)

    screen = im_opencv
    result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)

    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    top_left = max_loc
    bottom_right = (top_left[0] + template.shape[1], top_left[1] + template.shape[0])
    center=(int((top_left[0]+bottom_right[0])/2),int((top_left[1]+bottom_right[1])/2))

# #     #显示匹配
#     cv2.rectangle(screen,top_left, bottom_right,(0,0,255),3)
#     cv2.imshow("imgRec",screen)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()

    # #内存释放
    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hWnd,hWndDC)
    return center,max_val
# 向X,Y坐标点发送鼠标左键点击事件
def get_center_locateonwindow(hWnd=0,confid=0.8,name='',templatePath='',left=0,top=0,width=1400,height=810):
    center,confidence=[],0
    try:
        center,confidence=get_center_confidence_locateonwindow(hWnd=hWnd,confid=confid,name=name,templatePath=templatePath,left=left,top=top,width=width,
                                                               height=height)
    except Exception:
        print('获取图片匹配坐标失败')
    if confid<confidence:
        return center
    else:
        return None
def window_click(hwnd=0,center=[],isadb=0):
        if isadb is not 0 :
            adb_click(center)
            return True
        win32gui.ShowWindow(hwnd, win32con.SW_SHOWNORMAL)

        lParam = win32api.MAKELONG(int(center[0]),int(center[1]))
        win32api.SendMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
        time.sleep(0.1)
        win32api.SendMessage(hwnd, win32con.WM_LBUTTONUP, None, lParam)
        return True

def window_button_click(hwnd,text,class_name='Button',match=0):#match:是否全字匹配
    win32gui.ShowWindow(hwnd, win32con.SW_SHOWNORMAL)
    def enum_child_windows(hwnd, lParam):
        child_windows.append(hwnd)
        return True
#     print(hwnd,'所有控件:')
    child_windows=[]
    win32gui.EnumChildWindows(hwnd, enum_child_windows, None)
    item_hwnd=0
    f=0
    if match==1:
        for child_handle in child_windows:
            class_name_ = win32gui.GetClassName(child_handle)
            txt = win32gui.GetWindowText(child_handle)
            rect = win32gui.GetWindowRect(child_handle)
            if text == txt:
                item_hwnd=child_handle
                f=1
                break


    for child_handle in child_windows:
        class_name_ = win32gui.GetClassName(child_handle)
        txt = win32gui.GetWindowText(child_handle)
        rect = win32gui.GetWindowRect(child_handle)
        if text in txt and class_name in class_name_:
            item_hwnd=child_handle
            f=1
#             print(class_name_,txt)
            break
    if f==0:
        print('未找到控件')
    else:
#         print('找到控件',item_hwnd)
        win32gui.ShowWindow(item_hwnd, win32con.SW_SHOWNORMAL)
        win32api.SendMessage(item_hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, 0)
        time.sleep(0.1)
        win32api.SendMessage(item_hwnd, win32con.WM_LBUTTONUP,0,0)
#         print('点击控件成功')
        return True
    try:
#         win32gui.ShowWindow(hwnd, win32con.SW_SHOWNORMAL)
        win32api.SendMessage(item_hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, 0)
        time.sleep(0.1)
        win32api.SendMessage(item_hwnd, win32con.WM_LBUTTONUP,0,0)
        time.sleep(1)
        win32api.SendMessage(item_hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, 0)
        time.sleep(0.1)
        win32api.SendMessage(item_hwnd, win32con.WM_LBUTTONUP,0,0)
#         print('点击控件成功')
        return True
    except Exception:
        print('点击错误')
        return False
def window_scroll(hwnd,center,offset):
    win32gui.ShowWindow(hwnd, win32con.SW_SHOWNORMAL)
    center2=[int(center[0]),int(center[1])]
    center=center2
    point = win32api.MAKELONG(center[0],center[1])   #  定义起始点

    point1 = win32api.MAKELONG(center[0]+offset[0],center[1]+offset[1])    #   定义终点
    win32gui.SendMessage(hwnd,win32con.WM_LBUTTONDOWN,win32con.MK_LBUTTON, point)   # 起始点按住

    win32gui.SendMessage(hwnd,win32con.WM_MOUSEMOVE, win32con.MK_LBUTTON,point1)   #   移动到终点

    win32gui.SendMessage(hwnd, win32con.WM_LBUTTONUP, 0, point1)   # 松开

    time.sleep(1)
    window_click(hwnd,[center[0]+offset[0],center[1]+offset[1]])

def isMatch(hWnd=0,confid=0.8,name='',templatePath='',left=0,top=0,width=1400,height=810):
    center,confidence=get_center_confidence_locateonwindow(hWnd=hWnd,confid=confid,name=name,templatePath=templatePath,left=left,top=top,width=width,height=height)
    if confidence is not None and confid<confidence:
        return True
    else:
        return False
def matchAndClick(hWnd=0,confid=0.8,name='',templatePath='',isadb=0,left=0,top=0,width=1400,height=810):
    center,confidence=get_center_confidence_locateonwindow(hWnd=hWnd,confid=confid,name=name,templatePath=templatePath,left=left,top=top,width=width,height=height)
    if confid<confidence:
        if isadb==1:
            return  adb_click(center)
        else:
            return window_click(hWnd,center)
    else:
        return False
def findSoleData(name="Ld9BoxHeadless.exe",data=""):

    proc = Pymem(name)

    if proc is None:
        print("name" + "打开失败")
        return proc
    # datas=data.split('+')
    data2 = '\\x' + data
    datas = data2.replace(' ', '\\x')
    pattern = datas
    bPattern = pattern.encode()

    return proc.pattern_scan_all(bPattern)

def modeifySoleData(name="Ld9BoxHeadless.exe",data="",value=100,offset=0,addr=None):
    ret=True
    proc=Pymem(name)

    if proc is None:
        print("name"+"打开失败")
        return False
    if addr is not None:
        proc.write_int(addr + offset, value)
    #datas=data.split('+')
    data2='\\x'+data
    datas=data2.replace(' ','\\x')
    pattern=datas
    bPattern=pattern.encode()

    addresses = proc.pattern_scan_all(bPattern)
    if addresses is not None:
            #print(f"{addresses:X}")
            a = addresses

            proc.write_int(a+offset, value)
    else:
            print(f"error:未找到地址")
            ret=False

    # ind = 0
    # for i in bPatterns:
    #     ind += 1
    #     addresses = proc.pattern_scan_all(i)
    #     if addresses is not None:
    #         print(f"{addresses:X}")
    #         a = addresses
    #         curSp = a - 0xd4
    #         maxDp = a - 0x10
    #         curDp = a + 0x20
    #         li = a
    #         ling = a + 0x4
    #         ti = a + 0x14
    #         jing = a + 0xC
    #         zhi = a + 0x10
    #         yun = a + 0x8
    #         proc.write_int(maxDp, 7000)
    #         time.sleep(0.1)
    #
    #
    #         time.sleep(0.1)
    #         proc.write_int(li, value)
    #         time.sleep(0.1)
    #         proc.write_int(ling, value)
    #         time.sleep(0.1)
    #         proc.write_int(ti, value)
    #         time.sleep(0.1)
    #         proc.write_int(jing, value)
    #         time.sleep(0.1)
    return ret
def dataModeify(name="Ld9BoxHeadless.exe",data="",value=2000,dataOffset=0):
    ret=True
    proc=Pymem(name)

    if proc is None:
        print("name"+"打开失败")
        return proc
    #datas=data.split('+')
    datas=re.split('\+',data)
    pattern=''
    bPatterns=[]
    datas16=[]
    cnt=0
    ss = ''
    for i in datas:
        data16=hex(int(i)+dataOffset)
        s=str(data16)[2:]

        cnt+=1
        ss=''
        if len(s)==3:
            ss = '\\x' +s[1]+s[2]+'\\x'+'0'+s[0]+'\\x00\\x00'
        elif len(s)==2:
            ss='\\x' +s[0]+s[1]+'\\x'+'00'+'\\x00\\x00'
        pattern+=(ss)
        if cnt %3==0:#一个角色的3个数据
        # print(ss,ss.encode(),pattern)

            bPattern=pattern.encode()
            bPatterns.append(bPattern)
            pattern=''
    #print(f"{proc.base_address:X}")
    #\\xF8\\x00\\x00\\x00\\x++\\x++
    ind=0
    for i in bPatterns:
        ind+=1
        addresses = proc.pattern_scan_all(i)
        if addresses is not None:
            print(f"{addresses:X}")
            a = addresses
            curSp = a - 0xd4
            maxHp = a + 0x18
            maxDp = a + 0x1C
            curDp = a + 0x20
            breakLevel= a + 0x24
            li = a
            ling = a + 0x4
            ti = a + 0x8
            jing = a + 0xC
            zhi = a + 0x10
            yun = a + 0x14
            proc.write_int(maxDp, 10000)


            proc.write_int(li, value)

            proc.write_int(ling, value)

            proc.write_int(ti, value)

            proc.write_int(jing, value)

            # proc.write_int(curDp, 18000)
            proc.write_int(zhi, value)

            proc.write_int(yun, value)

            proc.write_int(breakLevel, 16)


            # proc.write_int(li, value)
            # time.sleep(0.1)
            # proc.write_int(ling, value)
            # time.sleep(0.1)
            # proc.write_int(ti, value)
            # time.sleep(0.1)
            # proc.write_int(jing, value)
            # time.sleep(0.1)
            proc.write_int(curDp, 8000)
            # time.sleep(0.1)
        else:
            print(f"error:未找到第{ind}个角色地址")
            ret=False
    # ind = 0
    # for i in bPatterns:
    #     ind += 1
    #     addresses = proc.pattern_scan_all(i)
    #     if addresses is not None:
    #         print(f"{addresses:X}")
    #         a = addresses
    #         curSp = a - 0xd4
    #         maxDp = a - 0x10
    #         curDp = a + 0x20
    #         li = a
    #         ling = a + 0x4
    #         ti = a + 0x14
    #         jing = a + 0xC
    #         zhi = a + 0x10
    #         yun = a + 0x8
    #         proc.write_int(maxDp, 7000)
    #         time.sleep(0.1)
    #
    #
    #         time.sleep(0.1)
    #         proc.write_int(li, value)
    #         time.sleep(0.1)
    #         proc.write_int(ling, value)
    #         time.sleep(0.1)
    #         proc.write_int(ti, value)
    #         time.sleep(0.1)
    #         proc.write_int(jing, value)
    #         time.sleep(0.1)
    return ret

def serToClient(plaintext='',cla='A'):#A1天，B1周，C一月，D永久
    time = []
    time.append(datetime.datetime.now().strftime('%Y'))
    time.append(datetime.datetime.now().strftime('%m'))
    time.append(datetime.datetime.now().strftime('%d'))
    time.append(datetime.datetime.now().strftime('%H'))
    p = plaintext[::-1] + ":" + cla + (datetime.datetime.now().strftime('%Y%m%d%H'))[::-1]
    msg = b64encode(p.encode()).decode()
    print(msg)
    return msg

def parseMsg(txt=''):
    if txt=='此生挚爱久岛鸥':
        return None,None,None
    parts=b64decode(txt.encode()).decode()
    id=parts[0:-12:][::-1]
    cla=parts[-11]
    date=parts[-10::][::-1]
    #print(f"{id},{cla},{date}")
    return id ,cla,date
def clientToServer():
    result = ''
    for board_id in WMI().Win32_BaseBoard():
        result += board_id.SerialNumber + ' '
    part1 = result.strip().upper()
    MACAddress = ''
    for nw in WMI().Win32_NetworkAdapterConfiguration(IPEnabled=1):
        MACAddress += nw.MACAddress + ' '
    part2 = MACAddress.replace(":", "").replace(" ", "").upper()
    plaintext = part1[::2] + part2[::7]
    print(plaintext)
    ciphertext = b64encode(plaintext.encode())
    # print(str(ciphertext)[2:-1])
    return plaintext,ciphertext

def getTime(txt='2024112012'):#年月日时
    date2=datetime.datetime.now()
    date1 = datetime.datetime.strptime(txt,'%Y%m%d%H')
    dur=date2-date1
    # 对计算差值进行天数（days）和秒数(seconds)的提取，并将秒数转换为小时数
    day = dur.days
    hour = dur.seconds / 3600
    #print(f"注册时长：{day*24+hour}小时")
    return day*24+hour
myproperty=Property()

if __name__ == '__main__':

    # serToClient('Y0731C5051','C')
    # Hwnd = 984918
    # hwnd = Hwnd
    # #get_window_item_center_by_text(hwnd=Hwnd, text='运行')
    # print(matchAndClick(templatePath="uipictures/menu.png", confid=0.7, hWnd=hwnd,isadb=1))
    # getTime()
    print(serToClient("Y0731C5051",'B'))
    # parseMsg("WTA3MzFDNTA1MUIzMTIyMDE0MjAy")
    # generPassword()
    #dataModeify()
    get_window_shot(hWnd=264012,save=0)
    # ctypes.cdll.LoadLibrary("ker")
#     win32gui.ShowWindow(hwnd, win32con.SW_SHOWNORMAL)
#     print(get_center_locateonwindow(name='雷电模拟器',templatePath='uipictures/attack.png'))
#     adb_click((473, 374))
