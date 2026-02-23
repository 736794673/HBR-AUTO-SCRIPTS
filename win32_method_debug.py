import win32gui, win32ui, win32con,win32api
from ctypes import windll
from PIL import Image
import cv2,os
import numpy
import pynput.mouse as pm
import threading
import time
import pyautogui
child_windows = []
import subprocess as sp
from  tkinter import  messagebox,Tk

import HBR_ldvbox
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
            print(center,[(rect[0]+rect[2])/2,(rect[1]+rect[3])/2])
            return center,[(rect[0]+rect[2])/2,(rect[1]+rect[3])/2]
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
        
        print("控件类名：", class_name,child_handle)
        print("控件文本：", txt)
        print("控件位置：", rect)
        center=[(rect[0]+rect[2])/2,(rect[1]+rect[3])/2]
   
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
class Property:
    def __init__(self):
        
        self.runtime=60#分钟
        self.maxcount=5#刷本次数
        self.face=3#副本有几面
        self.curRound=0#当前在几面
        self.helperOrder=1#顺位1、2、3
        self.playerName='Nemu'
        self.useapple=3#1234金、银、青铜、赤铜
        self.ceTime=20
        self.hce=0
        self.hmumu=0
        self.skillTo=dict()
        self.freeCenter=[]
        self.cardCenter1=[]
        self.cardCenter2=[]
        self.cardCenter3=[]
        self.cardCenter4=[]
        self.helperCenter=[]
        self.isuseskill=False
        self.appleImg=''
        self.error=0
        #以窗口左上角为参考系，窗口大小为比例
        self.skillCenterXOffsetRate=[0.13,0.373,0.619]#1 4 7
        self.skillCenterYOffsetRate=0.801
        self.skillOffsetRate=0.067#1 2
        self.skillDistXOffsetRate=[0.288,0.525,0.787]#1 2 3
        self.skillDistYOffsetRate=0.616
        self.windowInfo=[]
        self.atkCenter=[]
        self.atkCenterOffset=[0.877,0.835]
    
    # def showBox(self,mes=''):
    #         top.withdraw()
    #         isCancel=messagebox.askquestion('提示:error',mes)
    #         if isCancel=='no':
    #             return False
    #         else:
    #             return True
    def checkRound(self):
        if isMatch("uipictures/3round.png",0.98):
            self.curRound=3
            return True
        if isMatch("uipictures/1round.png",0.98):
            self.curRound=1
            return True
        if isMatch("uipictures/2round.png",0.98):
            self.curRound=2
            return True
        
        self.curRound=(self.curRound+1)%4
        
    def readFile(self, file_name):
        # 读取文件
        with open(file_name, encoding='utf8') as file:
            # 逐行(对象)遍历
            lines=file.readlines()
            for line in lines:
               # print(line)
                s=[]
                a=[]
                if line[0] !='#':
                    
                    s=line.split('=')[0]
                    a=line.split('=')[1]
                if '技能' in s and '>' in a:
                    t=a.split('>')
                    print(t)
                    self.skillTo[int(t[0].strip())]=[int(t[1].strip()),int(t[2].strip())]
                if '最大运行时长' in s:
                    self.runtime=int(a.strip())
                if '模拟器'in s:
                    self.playerName=a.strip()
                
                if '修改器' in s and '时长' in s:
                    self.ceTime=int(a.strip())
                if '面数' in s :
                    self.face=int(a.strip())
                if '使用苹果'  in s:
                    self.useapple=int(a.strip())
                if '是否使用技能' in s:
                    if '是'in a:
                        self.isuseskill=True
                        print('确定使用技能')
                    else:
                        self.isuseskill=False
                if '助战顺位' in s:
                    self.helperOrder=int(a.strip())
            print('读取文件成功')    
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
def get_window_shot(hWnd=0,name='',path='',left=0,top=0,width=1400,height=810,save=1):
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
            #if name in title[1]:
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
    # saveBitMap.SaveBitmapFile(saveDC,path)
    ###获取位图信息
    bmpinfo = saveBitMap.GetInfo()
    bmpstr = saveBitMap.GetBitmapBits(True)
    ###生成图像
    im_PIL = Image.frombuffer('RGB',(bmpinfo['bmWidth'],bmpinfo['bmHeight']),bmpstr,'raw','BGRX',0,1)
    #PIL保存
    im_PIL.save("im_PIL.png") #保存
    im_PIL.show() #显示
    
    
    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hWnd,hWndDC)
def get_center_confidence_locateonwindow(hWnd=0,confid=0.8,name='',templatePath='',left=0,top=0,width=1400,height=810):
    #获取后台窗口的句柄，注意后台窗口不能最小化
    def get_all_hwnd(hwnd, mouse):
        if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
            hwnd_title.update({hwnd: win32gui.GetWindowText(hwnd)})
    hwnd_map = {}
    hwnd_title = dict()
    win32gui.EnumWindows(get_all_hwnd, 0)
    if hWnd==0:
        print("hWnd==0")
        for title in hwnd_title.items():
            #if '命运-冠位指定' in title[1] and '模拟器' in title[1]:
            if name in title[1]:
                hWnd=title[0]
                # print(hWnd,title[1])
    #获取句柄窗口的大小信息
    # win32gui.GetWindowRect(hWnd)
    # print(win32gui.GetWindowRect(hWnd))

    left, top, right, bot = win32gui.GetWindowRect(hWnd)
    print(f"{hWnd}left, top, right, bot:{left} {top} {right}")
    width = right - left
    height = bot - top



    win32gui.ShowWindow(hWnd, win32con.SW_SHOWNORMAL)
    
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
        #x,y相反  -0-（y,x）
    result = windll.user32.PrintWindow(hWnd,saveDC.GetSafeHdc(),1)
    print(result) #PrintWindow成功则输出1
     # 将位图转换为OpenCV格式的数组
    signedIntsArray = saveBitMap.GetBitmapBits(True)
    im_opencv = numpy.frombuffer(signedIntsArray, dtype = 'uint8')
    im_opencv.shape = (height, width, 4)
    
    im_opencv = cv2.cvtColor(im_opencv, cv2.COLOR_BGRA2RGB)
    #显示原图
    cv2.imshow("imgRec",im_opencv)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    template=cv2.imread(templatePath)
    template = cv2.cvtColor(template, cv2.COLOR_BGRA2RGB)
    
    screen = im_opencv
    result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
    
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    top_left = max_loc
    bottom_right = (top_left[0] + template.shape[1], top_left[1] + template.shape[0])
    center=(int((top_left[0]+bottom_right[0])/2),int((top_left[1]+bottom_right[1])/2))
    print(templatePath,max_val)
#     #显示匹配
    cv2.rectangle(screen,top_left, bottom_right,(0,0,255),3)
    cv2.imshow("imgRec",screen)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    cv2.imwrite("pic.jpg",screen)
    # #内存释放
    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hWnd,hWndDC)
    print(templatePath,center,max_val)
    
    return center,max_val
# 向X,Y坐标点发送鼠标左键点击事件
def get_center_locateonwindow(hWnd=0,confid=0.8,name='',templatePath='',left=0,top=0,width=1400,height=810):
    center,confidence=[],0
    
    center,confidence=get_center_confidence_locateonwindow(hWnd=hWnd,confid=confid,name=name,templatePath=templatePath,left=left,top=top,width=width,height=height)
    if confid<confidence:
        return center
    else:
        return None
def window_click(hwnd,center):
#     try:
#         win32gui.ShowWindow(hwnd, win32con.SW_SHOWNORMAL)
        lParam = win32api.MAKELONG(int(center[0]),int(center[1]))
        win32api.SendMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
        
        win32api.SendMessage(hwnd, win32con.WM_LBUTTONUP, None, lParam)
        return True
#     except Exception:
#         exit()
#         return False
def window_button_click(hwnd,text,class_name='Button',match=0):
    def enum_child_windows(hwnd, lParam):
        child_windows.append(hwnd)
        return True
    print(hwnd,'所有控件:')
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
            print(class_name_,txt)
            break
    if f==0:
        print('未找到控件')
    else:
        print('找到控件',item_hwnd)
        win32api.SendMessage(item_hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, 0)

        win32api.SendMessage(item_hwnd, win32con.WM_LBUTTONUP,0,0)
        print('点击控件成功')
        return True
    try:
#         win32gui.ShowWindow(hwnd, win32con.SW_SHOWNORMAL)
        win32api.SendMessage(item_hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, 0)

        win32api.SendMessage(item_hwnd, win32con.WM_LBUTTONUP,0,0)
        print('点击控件成功')
        return True
    except Exception:
        print('点击错误')
        return False
def window_scroll(hwnd,center,offset):
    win32gui.ShowWindow(hwnd, win32con.SW_SHOW)
#     center[0]=int(center[0])
#     center[1]=int(center[1])
#     point = win32api.MAKELONG(center[0],center[1])   #  定义起始点    
# 
#     point1 = win32api.MAKELONG(center[0]+offset[0],center[1]+offset[1])    #   定义终点
    center2=[int(center[0]),int(center[1])]
    center=center2
    point = win32api.MAKELONG(center[0],center[1])   #  定义起始点    

    point1 = win32api.MAKELONG(center[0]+offset[0],center[1]+offset[1])    #   定义终点
    print(center,[center[0]+offset[0],center[1]+offset[1]])
    win32gui.SendMessage(hwnd,win32con.WM_LBUTTONDOWN,win32con.MK_LBUTTON, point)
    time.sleep(0.1)# 起始点按住    
    win32gui.SendMessage(hwnd, win32con.WM_LBUTTONUP, None, point)

    time.sleep(0.1)
    win32gui.SendMessage(hwnd,win32con.WM_LBUTTONDOWN,win32con.MK_LBUTTON, point)
    time.sleep(0.1)
    win32gui.SendMessage(hwnd,win32con.WM_MOUSEMOVE, win32con.MK_LBUTTON,point1)   #   移动到终点    
    time.sleep(3)
    win32gui.SendMessage(hwnd, win32con.WM_LBUTTONUP, None, point1)   # 松开
#     time.sleep(1)
#     window_click(hwnd,[center[0]+offset[0],center[1]+offset[1]])


def isMatch(hWnd=0,confid=0.8,name='',templatePath='',left=0,top=0,width=1400,height=810):
    center,confidence=get_center_confidence_locateonwindow(hWnd=hWnd,confid=confid,name=name,templatePath=templatePath,left=left,top=top,width=width,height=height)
    if confidence is not None and confid<confidence :
        return True
    else:
        return False
def matchAndClick(hWnd=0,confid=0.8,name='',templatePath='',left=0,top=0,width=1400,height=810):
    center,confidence=get_center_confidence_locateonwindow(hWnd=hWnd,confid=confid,name=name,templatePath=templatePath,left=left,top=top,width=width,height=height)
    if confid<confidence:
        return window_click(hWnd,center)
    else:
        return False
myproperty=Property()
def drag_to(hwnd, start_x, start_y, end_x, end_y):
    # Move to the starting point
    win32api.SetCursorPos((start_x, start_y))

    # Press the left mouse button
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)

    # Move to the end point
    win32api.SetCursorPos((end_x, end_y))
    
    # Pause for a short duration (adjust as needed)
    time.sleep(0.1)

    # Release the left mouse button
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)


if __name__ == '__main__':
    Hwnd=197706
    get_window_item_center_by_text(hwnd=Hwnd, text='运行')
    hwnd=Hwnd
    get_window_shot()
    get_window_item_center_by_text(hwnd=Hwnd,text='运行')
    print(isMatch(templatePath="uipictures/menu.png",confid= 0.7 ,hWnd=hwnd))
    if isMatch(templatePath="uipictures/menu.png",confid= 0.7 ,hWnd=hwnd) :
        
        center=get_center_locateonwindow(templatePath='uipictures/2spot2.png', confid=0.8, hWnd=hwnd)
        print("scroll")
        window_scroll(hwnd, center, [0, 10])

#     center=get_center_locateonwindow(hWnd=hwnd,confid=0.8,name='',templatePath='uipictures/nextStage2.png')
#     print("center：",center)
#     #center[0],center[1]
#     adb_click(center)
#     matchAndClick(hWnd=hwnd,confid=0.5,name='',templatePath='uipictures/nextStage2.png')
#     
# #     point = win32api.MAKELONG(center[0],center[1])   #  定义起始点    
#     offset=[0,250]
#       #   定义终点
#     print(center,[center[0]+offset[0],center[1]+offset[1]])
#     cur=center[1]
#     win32gui.SendMessage(hwnd,win32con.WM_LBUTTONDOWN,win32con.MK_LBUTTON, point)   # 起始点按住    
#     while(cur<center[1]+offset[1]):
#         cur+=50
#         point1 = win32api.MAKELONG(center[0]+offset[0],cur)  
#         win32gui.SendMessage(hwnd,win32con.WM_MOUSEMOVE, win32con.MK_LBUTTON,point1)   #   移动到终点    
#         
#         print(cur)
#         time.sleep(0.3)
#     win32gui.SendMessage(hwnd, win32con.WM_LBUTTONUP, 0, 0)   # 松开
# 
#     
    
    
#     lParam = win32api.MAKELONG (center[0],center[1])
#     win32api.PostMessage (hwnd,win32con.WM_MOUSEWHEEL,win32con.MK_LBUTTON,lParam)
#     win32api.PostMessage(hwnd, win32con.WM_MOUSEWHEEL, win32con.WHEEL_DELTA * 5, lParam)






#     window_scroll(hwnd,center,offset=[0,250])
#     print('点击完成')
#     show_windows_items(hwnd)