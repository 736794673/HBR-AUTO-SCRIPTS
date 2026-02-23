import time
import win32gui
import os
from tkinter import messagebox,Tk

import subprocess as sp
import threading
class Property:
    def __init__(self):
        self.runtime = 60  # 分钟
        self.maxcount = 5  # 刷本次数
        self.maxface = 3  # 副本有几面
        self.curFace = 1  # 当前在几面
        self.helperOrder = 1  # 顺位1、2、3
        self.playerName = '雷电模拟器'
        self.gameName = 'Ld9BoxHeadless'
        self.useapple = 3  # 1234金、银、青铜、赤铜
        self.ceTime = 20
        self.hce = 0
        self.hldvbox = 0
        self.skillTo = dict()
        self.freeCenter = []
        self.cardCenter1 = []
        self.cardCenter2 = []
        self.cardCenter3 = []
        self.cardCenter4 = []
        self.helperCenter = []
        self.isuseskill = False
        self.appleImg = ''
        self.error = 0
        self.isshutdown = 0
        # 以窗口左上角为参考系，窗口大小为比例

        self.windowInfo = []
        self.atkCenter = []
        self.atkCenterOffset = [0.877, 0.835]
        self.maxErrorLoop = 10
        self.curErrorLoop = 0
        self.isadb = 0

    def showBox(self, mes=''):
        top = Tk()
        top.withdraw()
        isCancel = messagebox.askquestion('提示:error', mes)
        if isCancel == 'no':
            return False
        else:
            return True

    def readFile(self, file_name):
        # 读取文件
        with open(file_name, encoding='utf8') as file:
            # 逐行(对象)遍历
            lines = file.readlines()
            for line in lines:
                # print(line)
                s = []
                a = []
                if line[0] != '#':
                    s = line.split('=')[0]
                    a = line.split('=')[1]
                if '技能' in s and '>' in a:
                    t = a.split('>')
                    print(t)
                    self.skillTo[int(t[0].strip())] = [int(t[1].strip()), int(t[2].strip())]
                if '最大运行时长' in s:
                    self.runtime = int(a.strip())
                if '模拟器进程名' in s:
                    self.playerName in a.strip()

                if '修改器' in s and '时长' in s:
                    self.ceTime = int(a.strip())
                if '面数' in s:
                    self.maxface = int(a.strip())
                if '使用苹果' in s:
                    self.useapple = int(a.strip())
                if '自动关机' in s:
                    self.isshutdown = int(a.strip())
                if 'adb' in s:
                    self.isadb = int(a.strip())
                    print('adb:', self.isadb)
                if '是否使用技能' in s:
                    if '是' in a:
                        myProperty.isuseskill = True
                        # print('确定使用技能')
                    else:
                        myProperty.isuseskill = False
                if '助战顺位' in s:
                    self.helperOrder = int(a.strip())
                    # print('助战:',a)
            print('读取文件成功', self.isshutdown)

    def checkRound(self):
        if isMatch("uipictures/3round.png", 0.97, self.hldvbox):
            self.curFace = 3
            return True
        if isMatch("uipictures/1round.png", 0.97, self.hldvbox):
            self.curFace = 1
            return True
        if isMatch("uipictures/2round.png", 0.97, self.hldvbox):
            self.curFace = 2
            return True

        self.curFace = (self.curFace + 1) % 4
        return True

    def modifyRound(self):
        pass