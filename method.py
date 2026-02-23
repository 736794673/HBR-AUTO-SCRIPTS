import pyautogui,time
import win32api,win32con,win32gui
from windows_invoke import invoke_window,get_all_windows,get_all_hwnd
from tkinter import *
import os
import cv2
from windows_invoke import *

def match_template(image_path, template_path):
    screen = cv2.imread(image_path)
    template = cv2.imread(template_path)
    try:
        result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
    except Exception :
        return -1,-1,-1
        
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    top_left = max_loc
    bottom_right = (top_left[0] + template.shape[1], top_left[1] + template.shape[0])
    return top_left,bottom_right,max_val
def matchAndClickEX(path,confid=0.75,hwnd=0):#返回在整个屏幕的坐标
    center=getCenterOnScreenEX(path,confid,hwnd)
    if center is not None:
        pyautogui.click(center)
        return center
    else:
        return None#未找到
def getCenterOnScreenEX(templatePath='',confid=0.75,hwnd=0):#在整个屏幕的坐标
    path='screenshot.png'
    offset=[0,0]
    center=[0,0]
    if hwnd==0:
        im=pyautogui.screenshot()
        im.save(path)
    else:
        #invoke_window(hwnd)
        print(hwnd)
#         x, y, width, height = get_window_pos_size(hwnd)
#         center=[x,y]
#         time.sleep(0.5)
#         im=pyautogui.screenshot(region=(x, y, width, height))
#         im.save(path)
        while(1):
            res=get_window_pos_size(hwnd)
            if res is not None:
                x, y, width, height = res[0],res[1],res[2],res[3]
                center=[x,y]
                time.sleep(0.5)
                im=pyautogui.screenshot(region=(x, y, width, height))
                im.save(path)
                break
            else:
                pass
    top_left,bottom_right,max_val=match_template(templatePath,path)
    if max_val>confid:
        center=[center[0]+(top_left[0]+bottom_right[0])/2,center[1]+(top_left[1]+bottom_right[1])/2]
        print(path,max_val)
        return center
    else:
        center=[center[0]+(top_left[0]+bottom_right[0])/2,center[1]+(top_left[1]+bottom_right[1])/2]
        print(path,max_val)
        return center
#         return  None
def get_window_pos_size(hwnd):
    if hwnd==0:
        print('无效句柄',hwnd)
        return
    else:
        try:
            invoke_window(hwnd)
            hwnd = win32gui.GetForegroundWindow()
            window_rect = win32gui.GetWindowRect(hwnd)

            x = window_rect[0]
            y = window_rect[1]
            width = window_rect[2] - x
            height = window_rect[3] - y
        except Exception:
            print('获取窗口信息失败')
            return None
    return [x, y, width, height]  
def getScreenshot(hwnd=0,path='screenshot.png'):
    if hwnd==0:
        im=pyautogui.screenshot()
    else:
        #invoke_window(hwnd)
        x, y, width, height = get_window_pos_size(hwnd)
        im=pyautogui.screenshot(region=(x, y, width, height))
    im.save(path)
    return path
