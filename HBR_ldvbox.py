import datetime
import time

import win32con

from property import *
import win32_method
#adb连接
os.system('adb start-server')
os.system('adb devices')
myProperty=Property()
def creatNewObj(p2=Property()):
        p=Property()
        p.runtime=p2.runtime#分钟
        p.maxcount=p2.maxcount#刷本次数
        p.maxface=p2.maxface#副本有几面
        p.helperCenterOffset=p2.helperCenterOffset#顺位1、2、3
        p.playerName=p2.playerName
        p.useapple=p.useapple#1234金、银、青铜、赤铜
        p.ceTime=p2.ceTime
        p.hce=p2.hce
        p.hldvbox=p2.hldvbox
        
        p.freeCenter=[]
        p.cardCenter1=[]
        p.cardCenter2=[]
        p.cardCenter3=[]
        p.cardCenter4=[]
        p.helperCenter=[]
        p.appleImg=''
        p.error=0
def msg():
    if h >= 0 and h <= 4:
        print('凌晨了,晚安~')
    elif h >= 5 and h <= 7:
        print('早上好!')
    elif h >= 8 and h <= 11:
        print('上午好~')
    elif h >= 12 and h <= 18:
        print('下午好~')
    elif h >= 19 and h <= 24:
        print('晚上好~')
    print("作者：久岛鸥的小屋 （闲鱼id：）xy624861081853 如遇问题可私信找我解决~\n\n")
    getMsg=''
    with open('__password.txt', encoding='gbk') as file:
        # 逐行(对象)遍历
        lines = file.readlines()
        for line in lines:
            s = []
            if line[0] != '#':
                s = line.split(':')[0]
                a = line.split(':')[1]
            if '密码' in s:
                getMsg=a.strip()
                break
    isRegisterd=True
    id, trueword = win32_method.clientToServer()
    while(1):
        if getMsg == '':
            isRegisterd=False
            print(f"提示:未注册,请发送‘{id}’给管理员，获得注册码（一机一个）")
            getMsg = input("请输入注册码:")
        password, cla, date = win32_method.parseMsg(getMsg)

        if password == id or getMsg=="此生挚爱久岛鸥":
            print(f"认证成功！会员等级:{cla} 注册时间:{date}")
            if getMsg=="此生挚爱久岛鸥":
                break
            if isRegisterd==False:
                with open('__password.txt', 'w',encoding="gbk") as f:
                    f.write("密码:"+getMsg)
            dur=win32_method.getTime(date)
            if cla=='A':
                if dur <0:
                    print("当前系统时间错误，请修改")
                    exit(1)

                elif dur>24:
                    print("提示：会员到期")
                    getMsg=''
                    continue
                else:
                    break
            elif cla=='B':
                if dur <0:
                    print("当前系统时间错误，请修改后重启程序")
                    exit(1)

                elif dur>24*7:
                    print("提示：会员到期")
                    getMsg = ''
                    continue
                else:
                    break
            elif cla=='C':
                if dur <0:
                    print("当前系统时间错误，请修改后重启程序")
                    exit(1)

                elif dur>24*31:
                    print("提示：会员到期")
                    getMsg = ''
                    continue
                else:
                    break
            elif cla=='D':
                break


        else:
            print("error:认证失败！")
            getMsg=''
            continue
def init(myProperty=Property()):
    
    def get_all_hwnd(hwnd, mouse):
        if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
            hwnd_title.update({hwnd: win32gui.GetWindowText(hwnd)})
    hwnd_map = {}
    hwnd_title = dict()
    win32gui.EnumWindows(get_all_hwnd, 0)
    # while(myProperty.hldvbox==0 or myProperty.hce==0):
    while (myProperty.hldvbox == 0 ):
        for title in hwnd_title.items():
        #if '命运-冠位指定' in title[1] and '模拟器' in title[1]:
            if myProperty.hldvbox==0:
                pass
            else:
                break
            if  myProperty.playerName == title[1]:
                myProperty.hldvbox=title[0]
                #print( myProperty.playerName,title[0])
                #修改器hwnd获取
#             if 'HBR' in title[1] and 'LUA'  in title[1] and '脚本'in title[1]:
# #             if 'Cheat Engine' in title[1]:
#                 myProperty.hce=title[0]
#                 print('CE修改器',title[0])

#         if  myProperty.hldvbox==0:
#             print('模拟器未获取')
#             continue
# #       elif myProperty.hce==0 :
# #             print('修改器未获取')
# #             continue
#         else:
#             break
    
    time.sleep(1)
    while(1):
        left, top, right, bot = win32gui.GetWindowRect(myProperty.hldvbox)
        width = right - left
        height = bot - top
        x,y=0,0
#         x=left
#         y=top
        
        myProperty.windowInfo.append(x)
        myProperty.windowInfo.append(y)
        myProperty.windowInfo.append(width)
        myProperty.windowInfo.append(height)
        print('模拟器',myProperty.hldvbox)
        print("窗口位置：({}, {})".format(x, y))
        print("窗口大小：{}x{}".format(width, height))
        if width>0:
            print('获取窗口信息成功')
            break
        else :
            print('获取窗口信息失败，正在重新获取')
    
    myProperty.freeCenter=[x+width*0.1,y+height*0.35]
    # myProperty.cardCenter1=[x+width*0.097,y+height*0.701]
    # myProperty.cardCenter2=[x+width*0.306,y+height*0.701]
    # myProperty.cardCenter3=[x+width*0.514,y+height*0.701]
    # myProperty.cardCenter4=[x+width*0.722,y+height*0.701]
    # myProperty.helperCenter=[x+width*0.5,y+height/4*(myProperty.helperOrder+0.5)]
    # myProperty.atkCenter=[x+width*myProperty.atkCenterOffset[0],y+height*myProperty.atkCenterOffset[1]]
    # myProperty.appleImg='uipictures/apple'+str(myProperty.useapple)+'.png'
    # print(myProperty.appleImg,myProperty.cardCenter1)
    return myProperty
def eachInit(myProperty=Property()):
    myProperty=init(myProperty)
    return myProperty

def useSkill(myProperty=Property(),count=1):
    if myProperty.isuseskill==False:
        return
    for f,t in myProperty.skillTo.items():
        if t[1] ==count:
            pass
        else:
            continue
        print('释放技能')
        center=[myProperty.windowInfo[0]+myProperty.skillCenterXOffsetRate[(f-1)//3]*myProperty.windowInfo[2]+myProperty.skillOffsetRate*myProperty.windowInfo[2],
                myProperty.windowInfo[1]+myProperty.skillCenterYOffsetRate*myProperty.windowInfo[3]]
       
        window_click(center,myProperty.hldvbox)
        
        
        if t[0] == 0:

            window_click(myProperty.freeCenter,myProperty.hldvbox)
            time.sleep(1)
            window_click(myProperty.freeCenter,myProperty.hldvbox)
            window_click(myProperty.freeCenter,myProperty.hldvbox)
            time.sleep(1)
            continue
        else:
             center=[myProperty.windowInfo[0]+myProperty.skillDistXOffsetRate[(t[0]-1)%3]*myProperty.windowInfo[2],
                myProperty.windowInfo[1]+myProperty.skillDistYOffsetRate*myProperty.windowInfo[3]]
             window_click(center,myProperty.hldvbox,)
             
             window_click(myProperty.freeCenter,myProperty.hldvbox)
             time.sleep(1)
             window_click(myProperty.freeCenter,myProperty.hldvbox)
             window_click(myProperty.freeCenter,myProperty.hldvbox)
             time.sleep(1)
        

    


def window_click(center,hwnd,isadb=myProperty.isadb):
    ret= win32_method.window_click(hwnd,center,isadb)
    
    return ret
def isMatch(path='',confid=0.7,hwnd=myProperty.hldvbox):
    return win32_method.isMatch(hWnd=hwnd,confid=confid,templatePath=path)

def matchAndClick(path='',confid=0.7,hwnd=myProperty.hldvbox,isAdb=myProperty.isadb,xOffset=0,yOffset=-50):
    try:
        center = get_center_locateonwindow(path=path, confidence=confid, hwnd=myProperty.hldvbox)
        if center is None:
            return False
        else:
            return win32_method.window_click(hwnd, [center[0]+xOffset,center[1]+yOffset], isAdb)
    except Exception as e:
        print(e)
def get_center_locateonwindow(path='',confidence=0.8,hwnd=myProperty.hldvbox):
    return win32_method.get_center_locateonwindow(hWnd=hwnd,confid=confidence,templatePath=path)
def eatApple():
    pass
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


def storyPass0():  #主线剧情
    flag = 0
    f = 0  # 步骤
    count = 0
    ea = 0
    center, startcenter = [0, 0], [0, 0]
    global myProperty
    myProperty = Property()
    isadb = True
    # myProperty.maxcount = int(input('最大运行次数:'))
    myProperty.readFile('__init.txt')
    runtime = myProperty.runtime * 60

    start = time.time()
    if myProperty.isshutdown == 1:
        timeline = Timeline(myProperty)
        timeline.start()
    myProperty = eachInit(myProperty)
    hwnd = myProperty.hldvbox
    while (1):

        # f = 0(尚未选择)，1(选择完关卡) ，2（选择完助战），3（战斗完成），
        # 选择关卡



        if isMatch("uipictures/skip.png", 0.7, hwnd):
            print("跳过")
            # print("center：",center)
            matchAndClick("uipictures/skip.png", 0.7, hwnd=myProperty.hldvbox,isAdb=1)
            time.sleep(2)
        if isMatch("uipictures/auto.png", 0.7, hwnd) and not isMatch("uipictures/autoOn.png", 0.7, hwnd):


            print("autoOn：main")
            if isadb:
                matchAndClick("uipictures/auto.png", 0.7, hwnd=myProperty.hldvbox,isAdb=myProperty.isadb)
                time.sleep(2)
            else:
                center = get_center_locateonwindow('uipictures/auto.png', 0.4, hwnd)
                win32_method.window_click(myProperty.hldvbox, center)
                pass

        #         elif ( f==0  or ff==0 or f>2 ) and isMatch('uipictures/end.png', 0.9, hwnd=myProperty.hldvbox):
        #             matchAndClick('uipictures/end.png', 0.9, hwnd=myProperty.hldvbox)
        #             f=0
        #             ff=0
        #             time.sleep(1)
        # elif isMatch("uipictures/autoOff.png", 0.8, hwnd):
        #
        #
        #     print("autoOn：")
        #     if isadb:
        #         matchAndClick("uipictures/auto.png", 0.8, hwnd=myProperty.hldvbox,isAdb=isadb)
        # #         time.sleep(2)
        elif isMatch("uipictures/startAttack.png", 0.8, hwnd):


            print("/startAttack：")
            if isadb:
                matchAndClick("uipictures/startAttack.png", 0.8, hwnd=myProperty.hldvbox,isAdb=isadb)
        #         time.sleep(2)
        elif isMatch("uipictures/ok.png", 0.8, hwnd):


            print("ok：")
            if isadb:
                matchAndClick("uipictures/ok.png", 0.8, hwnd=myProperty.hldvbox,isAdb=isadb)
        elif matchAndClick("uipictures/passTime.png", 0.8, hwnd=myProperty.hldvbox,isAdb=isadb):
            time.sleep(2)
            pass
        #         time.sleep(2)
        # elif isMatch("uipictures/wait.png", 0.7, hwnd):
        #     time.sleep(3)
        #
        # elif isMatch("uipictures/end.png", 0.7, hwnd):
        #     step = 0
        #     count += 1
        #     print(f"第{count}次运行")
        #     matchAndClick("uipictures/cancel.png", hwnd=myProperty.hldvbox)
        #     while (1):
        #         if step == 0 and matchAndClick("uipictures/map.png", hwnd=myProperty.hldvbox):
        #             step = 1
        #             time.sleep(1)
        #         if step == 1 and matchAndClick("uipictures/map1.png", 0.8, hwnd=myProperty.hldvbox):
        #             step = 2
        #             time.sleep(1)
        #         if step == 2 and matchAndClick("uipictures/spot.png", 0.8, hwnd=myProperty.hldvbox):
        #             time.sleep(1)
        #             step = 3
        #         if step == 3 and matchAndClick("uipictures/ok.png", 0.8, hwnd=myProperty.hldvbox):
        #             break
        # # elif isMatch("uipictures/select1.png", 0.7, hwnd=myProperty.hldvbox):
        # #     matchAndClick("uipictures/select1.png", hwnd=myProperty.hldvbox)
        # #     time.sleep(10)
        elif  isMatch("uipictures/autoOff.png", 0.8, hwnd)or isMatch("uipictures/redPoint.png",0.9,hwnd):
            pass
        elif  isMatch("uipictures/phone.png",0.7,hwnd) or isMatch("uipictures/home.png",0.7,hwnd)  or isMatch("uipictures/story.png",0.7,hwnd) or isMatch("uipictures/continue.png",0.7,hwnd):
            print("freeclick")
            win32_method.window_click(myProperty.hldvbox, [720,400],isadb=isadb)
            time.sleep(0.5)
            win32_method.window_click(myProperty.hldvbox, [720,100], isadb=isadb)
            time.sleep(0.5)
            win32_method.window_click(myProperty.hldvbox, [720,250], isadb=isadb)
            time.sleep(1)
        if count > myProperty.maxcount:
            if myProperty.isshutdown == 1:
                os.system("shutdown -s -t 60")
            return
def storyPass1():#3-14/21
    flag = 0
    f=0#步骤
    count = 0
    ea=0
    center, startcenter = [0, 0], [0, 0]
    global myProperty
    myProperty = Property()
    isadb=True
    myProperty.maxcount = int(input('最大运行次数:'))
    myProperty.readFile('__init.txt')
    runtime = myProperty.runtime * 60

    start = time.time()
    if myProperty.isshutdown == 1:
        timeline = Timeline(myProperty)
        timeline.start()
    myProperty = eachInit(myProperty)
    hwnd = myProperty.hldvbox
    while (1):
        
        #f = 0(尚未选择)，1(选择完关卡) ，2（选择完助战），3（战斗完成），
        # 选择关卡
        if isMatch("uipictures/auto.png", 0.8, hwnd):

            
            
            center = get_center_locateonwindow('uipictures/auto.png', 0.4, hwnd)
            # print("autoOn：",center)
            if isadb:
                win32_method.window_click(myProperty.hldvbox,center)
                time.sleep(2)
            else:
                win32_method.window_click(myProperty.hldvbox,center)
                pass


        elif  isMatch("uipictures/skip.png", 0.7, hwnd):
            print("跳过")
            center = get_center_locateonwindow('uipictures/skip.png', 0.6, hwnd)
            # print("center：",center)
            center2 = [center[0], center[1] - 35]
            win32_method.window_click(myProperty.hldvbox,center2)
            win32_method.window_click(myProperty.hldvbox,center2)
            time.sleep(2)

#         elif ( f==0  or ff==0 or f>2 ) and isMatch('uipictures/end.png', 0.9, hwnd=myProperty.hldvbox):
#             matchAndClick('uipictures/end.png', 0.9, hwnd=myProperty.hldvbox)
#             f=0
#             ff=0
#             time.sleep(1)
     

        # ea=0 #ea:是否检测到苹果logo
        # 检测是否要嗑苹果
        elif isMatch("uipictures/wait.png", 0.7, hwnd):
            time.sleep(3)
#         elif isMatch("uipictures/x.png", 0.7, hwnd):
#             matchAndClick("uipictures/x.png", hwnd=myProperty.hldvbox)
#             time.sleep(1)
#         elif isMatch("uipictures/nextAttack.png", 0.7, hwnd):
#             matchAndClick("uipictures/nextAttack.png", hwnd=myProperty.hldvbox)
#             time.sleep(1)
#         elif isMatch("uipictures/close.png", 0.7, hwnd):
#             matchAndClick("uipictures/close.png", hwnd=myProperty.hldvbox)
#             time.sleep(1)
#         else :
#             win32_method.adb_click(myProperty.freeCenter)
#             print("自由点击")
#             time.sleep(4)
        elif isMatch("uipictures/end.png", 0.7, hwnd):
            step=0
            count+=1
            print(f"第{count}次运行")
            matchAndClick("uipictures/cancel.png", hwnd=myProperty.hldvbox)
            while(1):
                if step==0 and matchAndClick("uipictures/map.png", hwnd=myProperty.hldvbox):
                    step=1
                    time.sleep(1)
                if step==1 and matchAndClick("uipictures/map1.png", 0.8,hwnd=myProperty.hldvbox):
                    step=2
                    time.sleep(1)
                if step==2 and matchAndClick("uipictures/spot.png",0.8, hwnd=myProperty.hldvbox):
                    time.sleep(1)
                    step=3
                if step==3 and matchAndClick("uipictures/ok.png",0.8, hwnd=myProperty.hldvbox):
                    break
        elif isMatch("uipictures/select1.png", 0.7, hwnd=myProperty.hldvbox) :
            matchAndClick("uipictures/select1.png", hwnd=myProperty.hldvbox)
            time.sleep(10)
        else :
            matchAndClick("uipictures/attackEnd.png", 0.7, hwnd=myProperty.hldvbox)
            time.sleep(2)
        if count>myProperty.maxcount:
            if myProperty.isshutdown==1:
                os.system("shutdown -s -t 60")
            return
        
def storyPass2():#鬼屋
    flag = 0
    f=0#步骤
    count = 0
    ea=0
    toEnd=True
    center, startcenter = [0, 0], [0, 0]
    global myProperty
    myProperty = Property()
    isadb=True

    myProperty.maxcount = 999999
    myProperty.readFile('__init.txt')
    lparam_down = (1 << 0) | (0x39 << 16) | (0 << 24) | (0 << 29) | (0 << 30) | (0 << 31)
    win32gui.SendMessage(myProperty.hldvbox, win32con.WM_KEYDOWN, win32con.VK_SPACE, lparam_down)

    # 空格键抬起消息
    lparam_up = (1 << 0) | (0x39 << 16) | (0 << 24) | (0 << 29) | (0 << 30) | (1 << 31)
    win32gui.SendMessage(myProperty.hldvbox, win32con.WM_KEYUP, win32con.VK_SPACE, lparam_up)
    runtime = myProperty.runtime * 60

    start = time.time()
    if myProperty.isshutdown == 1:
        timeline = Timeline(myProperty)
        timeline.start()
    myProperty = eachInit(myProperty)
    hwnd = myProperty.hldvbox

    while (1):
        
        #f = 0(尚未选择)，1(选择完关卡) ，2（选择完助战），3（战斗完成），
        # 选择关卡
#         if isMatch("uipictures/menu.png", 0.8, hwnd):
#             #右向
#             sp.Popen(f"adb shell input swipe  600 400 1100 400 800") #x y x y ms
#             time.sleep(1)
#
        if isMatch("uipictures/menu.png", 0.7, hwnd=hwnd) :
            step=0
            count+=1
            f=1#还未选择目标地
            print(f"第{count/2}个来回")
            #返回起点
            while(not toEnd and f ):
                #小地图坐标

                if step==0 and win32_method.window_click(myProperty.hldvbox,[1100,120],isadb=myProperty.isadb):
                    step=1
                    print("终点到起点")
                    time.sleep(1)
                if step==1 and matchAndClick("uipictures/2map1.png", 0.8,hwnd=myProperty.hldvbox,isAdb=myProperty.isadb):
                    step=2
                    time.sleep(1)

                if step==2:
                    if matchAndClick("uipictures/2spot.png",0.7, hwnd=myProperty.hldvbox,isAdb=myProperty.isadb):
                        time.sleep(1)

                        step=3
                    elif isMatch("uipictures/cur2spot.png",0.7, hwnd=myProperty.hldvbox):
                        print('在图1')
                        time.sleep(1)
                        step=3

#                     elif matchAndClick("uipictures/x.png",0.8, hwnd=myProperty.hldvbox):
#                         step=0
#                         break
                    else:
                        #左滑
                        sp.Popen(f"adb shell input swipe 600 400 1100 400  800") #x y x y ms

                if step==3:
                    step=0
                    if matchAndClick("uipictures/ok.png",0.8, hwnd=myProperty.hldvbox,isAdb=myProperty.isadb):
                        toEnd=not toEnd
                        f=0
                        time.sleep(1)
                    #matchAndClick("uipictures/x.png",0.8, hwnd=myProperty.hldvbox)
                        break
            time.sleep(1)
            #自动前往自定义终点
            step=0
            while(toEnd and f):

                center=[]
                win32_method.window_click(myProperty.hldvbox,[1100,120],isadb=1)
                if step==0 and matchAndClick("uipictures/2map2.png", 0.9,hwnd=myProperty.hldvbox,isAdb=myProperty.isadb):
                    step=1
                    print("起点到终点")
                    time.sleep(1)
                if step==1 :
                    if isMatch("uipictures/2spot.png", 0.7,hwnd=myProperty.hldvbox):
                        center=get_center_locateonwindow("uipictures/2spot.png", 0.7,hwnd=myProperty.hldvbox)
                        time.sleep(1)
                        step=2
                    else:
                        #左滑
                        sp.Popen(f"adb shell input swipe 600 400 1100 400  800") #x y x y ms
                        time.sleep(1)
                                                    #终点相对坐标
                if step==2 and win32_method.window_click(hwnd=myProperty.hldvbox,center=[center[0]+500,center[1]],isadb=myProperty.isadb):
                    step=3

                    time.sleep(1)
                if step==3 and matchAndClick(path="uipictures/ok.png",confid=0.8, hwnd=myProperty.hldvbox,isAdb=myProperty.isadb):

                    toEnd=not toEnd
                    time.sleep(3)
                    f=0
                    break
                
            time.sleep(1)

        # elif isMatch("uipictures/default.png", 0.8, hwnd):
        #     #右向
        #
        #     time.sleep(2)
        elif isMatch("uipictures/auto.png", 0.8, hwnd):
            center = get_center_locateonwindow('uipictures/auto.png', 0.8, hwnd)
            # print("autoOn：",center)
            win32_method.window_click(myProperty.hldvbox,center,isadb=myProperty.isadb)




        elif  isMatch("uipictures/skip.png", 0.7, hwnd):
            print("跳过")
            center = get_center_locateonwindow('uipictures/skip.png', 0.6, hwnd)
            # print("center：",center)
            center2 = [center[0], center[1] - 35]
            win32_method.window_click(myProperty.hldvbox,center2,isadb=myProperty.isadb)
            win32_method.window_click(myProperty.hldvbox,center2,isadb=myProperty.isadb)
            time.sleep(2)

#         elif ( f==0  or ff==0 or f>2 ) and isMatch('uipictures/end.png', 0.9, hwnd=myProperty.hldvbox):
#             matchAndClick('uipictures/end.png', 0.9, hwnd=myProperty.hldvbox)
#             f=0
#             ff=0
#             time.sleep(1)
     

        # ea=0 #ea:是否检测到苹果logo
        # 检测是否要嗑苹果
        elif isMatch("uipictures/wait.png", 0.7, hwnd):
            time.sleep(3)

        elif isMatch("uipictures/end.png", 0.7, hwnd):
            step=0
            count+=1
            print(f"第{count}次运行")
            matchAndClick("uipictures/cancel.png", hwnd=myProperty.hldvbox,isAdb=myProperty.isadb)
            while(not toEnd):
                if step==0 and matchAndClick("uipictures/2map.png", hwnd=myProperty.hldvbox,isAdb=myProperty.isadb):
                    step=1
                    time.sleep(1)
                if step==1 and matchAndClick("uipictures/2map1.png", 0.7,hwnd=myProperty.hldvbox,isAdb=myProperty.isadb):
                    step=2
                    time.sleep(1)
                if step==2 and matchAndClick("uipictures/2spot.png",0.7, hwnd=myProperty.hldvbox,isAdb=myProperty.isadb):
                    time.sleep(1)
                    step=3
                if step==3 and matchAndClick("uipictures/ok.png",0.7, hwnd=myProperty.hldvbox,isAdb=myProperty.isadb):
                    toEnd=not toEnd
                    break
#         elif isMatch("uipictures/select1.png", 0.7, hwnd=myProperty.hldvbox) :
#             matchAndClick("uipictures/select1.png", hwnd=myProperty.hldvbox)
#             time.sleep(10)
        else :
            matchAndClick("uipictures/x.png",0.8, hwnd=myProperty.hldvbox,isAdb=myProperty.isadb)
            time.sleep(2)
        if count>myProperty.maxcount:
            if myProperty.isshutdown==1:
                os.system("shutdown -s -t 60")
            return

def storyPass3(data_Offset=0):#宝珠迷宫
    flag = 0
    f=0#步骤
    count = 0
    ea=0
    toEnd=True
    center, startcenter = [0, 0], [0, 0]
    global myProperty
    myProperty = Property()
    isadb=True
    myProperty.maxcount = 10000
    myProperty.readFile('__init.txt')
    runtime = myProperty.runtime * 60

    start = time.time()
    if myProperty.isshutdown == 1:
        timeline = Timeline(myProperty)
        timeline.start()
    myProperty = eachInit(myProperty)
    hwnd = myProperty.hldvbox
    firMod=1
    address=win32_method.findSoleData(data='64 00 00 00 01 00 00 00 00 00 00')
    #能量：40 00 00 00 01 00 00 00 00 00 00 00 6D 48 1E 67
    while (1):

        #f = 0(尚未选择)，1(选择完关卡) ，2（选择完助战），3（战斗完成），
        # 选择关卡
#         if isMatch("uipictures/menu.png", 0.8, hwnd):
#             #右向
#             sp.Popen(f"adb shell input swipe  600 400 1100 400 800") #x y x y ms
#             time.sleep(1)
#
#         if isMatch("uipictures/menu.png", 0.8, hwnd):
#             step=0
#             count+=1
#             f=1#还未选择目标地
#             print(f"第{count}次运行")
#             #返回起点
#
#             time.sleep(3)
#             #自动前往自定义终点
#             step=0


#         elif isMatch("uipictures/default.png", 0.8, hwnd):
#             #右向
#
#             time.sleep(1)
        if firMod==1 and matchAndClick("uipictures/autoOn.png", 0.8, hwnd=hwnd, isAdb=1):
            #matchAndClick("uipictures/autoOn.png", 0.7, hwnd=hwnd, isAdb=1)
            print("autoon")
            #右向
            time.sleep(1)
            matchAndClick("uipictures/autoOn.png", 0.7, hwnd=hwnd, isAdb=1)
            matchAndClick("uipictures/autoOn.png", 0.7, hwnd=hwnd, isAdb=1)
            win32_method.modeifySoleData(data='64 00 00 00 01 00 00 00 00 00 00', value=100,offset=0,addr=address)
            #matchAndClick("uipictures/autoOn.png", 0.8, hwnd=hwnd,isAdb=1)
            # if isMatch("uipictures/a.png", 0.7, hwnd):
            print("modify")
            print("run:正在读取文件数据...")
            txt = readDataTxt()

            if txt == '':
                print("error:文件数据读取失败")
                pass
            print(txt)

            win32_method. dataModeify(data=txt,dataOffset=data_Offset)
            print("完成修改")
            time.sleep(1)
            while(not isMatch("uipictures/autoOn.png", 0.7, hwnd=myProperty.hldvbox)):
                time.sleep(1)
                if matchAndClick("uipictures/normal.png", 0.7, hwnd=myProperty.hldvbox, isAdb=1):

                    time.sleep(1)
                    break
                else:
                    matchAndClick("uipictures/autoOff.png", 0.7, hwnd=myProperty.hldvbox,isAdb=1)
            time.sleep(1)

            firMod=0
        # elif isMatch("uipictures/autoOff.png", 0.7, hwnd=hwnd):
        #     print('autooff')
        elif firMod==0 and isMatch("uipictures/mp.png", 0.7, hwnd):
            firMod=1
#         elif isMatch("uipictures/auto.png", 0.8, hwnd):
#             center = get_center_locateonwindow('uipictures/auto.png', 0.4, hwnd)
#             # print("autoOn：",center)
#             if isadb:
#                 win32_method.adb_click(center)
#                 time.sleep(2)
#             else:
#                 pass
        if count>myProperty.maxcount:
            if myProperty.isshutdown==1:
                os.system("shutdown -s -t 60")
            return


def storyPass6(data_Offset=0,consume=2 ,maxCount=1):#
    """
    consume 1/2
    """
    flag = 0
    f=0#步骤
    count = 1
    ea=0
    toEnd=True
    center, startcenter = [0, 0], [0, 0]
    global myProperty
    myProperty = Property()
    isadb=True
    myProperty.maxcount = 10000
    myProperty.readFile('__init.txt')
    runtime = myProperty.runtime * 60

    start = time.time()
    if myProperty.isshutdown == 1:
        timeline = Timeline(myProperty)
        timeline.start()
    myProperty = eachInit(myProperty)
    hwnd = myProperty.hldvbox
    firMod=1
    round=1
    address=win32_method.findSoleData(data='64 00 00 00 01 00 00 00 00 00 00')
    #能量：40 00 00 00 01 00 00 00 00 00 00 00 6D 48 1E 67
    while (1):
        if round==0 :
            win32_method.adb_click([700,400])
            if matchAndClick("uipictures/nextchallenge.png", 0.8, hwnd=hwnd, isAdb=1):
                while(1):
                    time.sleep(3)
                    #gqrcq tls
                    if consume==2:
                        matchAndClick("uipictures/tls.png", 0.8, hwnd=hwnd, isAdb=1)
                        time.sleep(1)
                        matchAndClick("uipictures/max2.png", 0.8, hwnd=hwnd, isAdb=1)
                        time.sleep(1)
                        matchAndClick("uipictures/ok.png", 0.8, hwnd=hwnd, isAdb=1)
                        time.sleep(1)
                        #matchAndClick("uipictures/xhtls.png", 0.8, hwnd=hwnd, isAdb=1)

                        matchAndClick("uipictures/max2.png", 0.8, hwnd=hwnd, isAdb=1)
                        matchAndClick("uipictures/ok.png", 0.8, hwnd=hwnd, isAdb=1)
                        time.sleep(1)
                        matchAndClick("uipictures/max2.png", 0.8, hwnd=hwnd, isAdb=1)
                        matchAndClick("uipictures/ok.png", 0.8, hwnd=hwnd, isAdb=1)
                        matchAndClick("uipictures/xhtls.png", 0.8, hwnd=hwnd, isAdb=1)
                    else:
                        matchAndClick("uipictures/gqrcq.png", 0.8, hwnd=hwnd, isAdb=1)
                        time.sleep(1)
                        matchAndClick("uipictures/max1.png", 0.8, hwnd=hwnd, isAdb=1)
                        time.sleep(1)
                        matchAndClick("uipictures/ok.png", 0.8, hwnd=hwnd, isAdb=1)
                        time.sleep(1)
                        # matchAndClick("uipictures/xhtls.png", 0.8, hwnd=hwnd, isAdb=1)

                        matchAndClick("uipictures/max1.png", 0.8, hwnd=hwnd, isAdb=1)
                        matchAndClick("uipictures/ok.png", 0.8, hwnd=hwnd, isAdb=1)
                        time.sleep(1)
                        matchAndClick("uipictures/max1.png", 0.8, hwnd=hwnd, isAdb=1)
                        matchAndClick("uipictures/ok.png", 0.8, hwnd=hwnd, isAdb=1)

                    if isMatch("uipictures/xmq.png", 0.8, hwnd=hwnd):
                        round += 1
                        break
                pass

        elif round==1 and matchAndClick("uipictures/xmq.png", 0.8, hwnd=hwnd, isAdb=1):
            print(round)
            time.sleep(1)
            txt = readDataTxt()

            if txt == '':
                print("error:文件数据读取失败")
            else:
                print(txt)
                win32_method.dataModeify(data=txt, dataOffset=data_Offset)
                print("完成修改")
            if not  matchAndClick("uipictures/gjzj.png", 0.7, hwnd=hwnd, isAdb=1):
                continue
            else:
                print("run:正在读取文件数据...")
                pass

            time.sleep(1)
            matchAndClick("uipictures/xmq.png", 0.7, hwnd=hwnd, isAdb=1)
            time.sleep(1)
            matchAndClick("uipictures/yg.png", 0.7, hwnd=hwnd, isAdb=1)
            time.sleep(1)
            matchAndClick("uipictures/gjzj.png", 0.7, hwnd=hwnd, isAdb=1)
            time.sleep(1)
            matchAndClick("uipictures/xmq.png", 0.8, hwnd=hwnd, isAdb=1)
            time.sleep(1)
            matchAndClick("uipictures/startAction.png", 0.8, hwnd=hwnd, isAdb=1)
            round+=1

        elif round == 2 and matchAndClick("uipictures/xmq.png", 0.8, hwnd=hwnd, isAdb=1):
            time.sleep(1)
            print(round)
            print('a')
            if not matchAndClick("uipictures/xj.png", 0.7, hwnd=hwnd, isAdb=1):
                continue
            print('a')
            time.sleep(1)
            matchAndClick("uipictures/yg.png", 0.7, hwnd=hwnd, isAdb=1)
            print('a')
            time.sleep(1)
            matchAndClick("uipictures/rxlxgc.png", 0.7, hwnd=hwnd, isAdb=1)
            print('a')
            time.sleep(1)


            matchAndClick("uipictures/startAction.png", 0.8, hwnd=hwnd, isAdb=1)
            round += 1
            time.sleep(1)
        elif round == 3 and matchAndClick("uipictures/yg.png", 0.8, hwnd=hwnd, isAdb=1):
            time.sleep(1)
            print(round)
            if not matchAndClick("uipictures/ym.png", 0.8, hwnd=hwnd, isAdb=1):
                continue
            time.sleep(1)

            matchAndClick("uipictures/xmq.png", 0.8, hwnd=hwnd, isAdb=1)
            time.sleep(1)
            matchAndClick("uipictures/xmq.png", 0.8, hwnd=hwnd, isAdb=1)
            time.sleep(1)

            matchAndClick("uipictures/yyzs.png", 0.8, hwnd=hwnd, isAdb=1)
            time.sleep(1)
            matchAndClick("uipictures/startAction.png", 0.8, hwnd=hwnd, isAdb=1)
            round += 1
            time.sleep(1)
            time.sleep(1)
            round=0
            count+=1
        if count>maxCount:
            return

def readDataTxt(path='__data.txt'):
    txt = ''
    with open(path, encoding='utf8') as file:
        # 逐行(对象)遍历
        lines = file.readlines()
        for line in lines:
            # print(line)
            s = []

            if line[0] != '#':
                s = line.split('=')[0]
                a = line.split('=')[1]
            if '角色数据' in s:
                txt=a
    return txt
def check():
    pass


def skip():
    global myProperty
    myProperty = Property()
    myProperty = eachInit(myProperty)
    while (1):
        if matchAndClick("uipictures/skip.png", 0.7, hwnd=myProperty.hldvbox, isAdb=1):
            print("skip")
            pass
        elif matchAndClick("uipictures/autoOff.png", 0.7, hwnd=myProperty.hldvbox, isAdb=1):
            print("autoOff")
        elif matchAndClick("uipictures/ok.png", 0.7, hwnd=myProperty.hldvbox, isAdb=1):
            print("ok")
        elif isMatch("uipictures/home.png", 0.7, hwnd=myProperty.hldvbox):
            win32_method.adb_click([720, 600])
            print("ho")
        elif matchAndClick("uipictures/startAttack.png", 0.7, hwnd=myProperty.hldvbox, isAdb=1):

            print("sa")
        elif matchAndClick("uipictures/continue.png", 0.7, hwnd=myProperty.hldvbox, isAdb=1):
            print("eb")
        elif isMatch("uipictures/autoOn.png", 0.7, hwnd=myProperty.hldvbox) is False:
            win32_method.adb_click([720, 600])
            time.sleep(1)
        else:
            pass
            # win32_method.adb_click([720, 600])
        # else:
        #     storyPass3()
        #     win32_method.adb_click([1400, 600])
        time.sleep(1)
def playcard():
    global myProperty
    myProperty = Property()
    myProperty = eachInit(myProperty)
    while (1):
        if matchAndClick("uipictures/defeated.png", 0.7, hwnd=myProperty.hldvbox, isAdb=1):
            print("endbattle")
            while(1):
                if matchAndClick("uipictures/31Anormal.png", 0.7, hwnd=myProperty.hldvbox, isAdb=1)is False:
                    win32_method.adb_click([888, 510])
                    time.sleep(2)
                else:
                    break
        elif matchAndClick("uipictures/challenge.png", 0.7, hwnd=myProperty.hldvbox, isAdb=1):
            print("开始")
            time.sleep(20)
        elif matchAndClick("uipictures/31Anormal.png", 0.7, hwnd=myProperty.hldvbox, isAdb=1):
            pass
if __name__ == '__main__':
    os.system('adb start-server')
    os.system('adb version')
    os.system('adb devices')
    # print(get_center_locateonwindow("uipictures\menu.png",hwnd=myProperty.hldvbox))
    h = datetime.datetime.now().hour

    cmd=0

    #start()#任务刷本
    while 1:
        print("***************\n-1:退出\n0:主线\n1:修改战斗数据\n2:鬼屋day3刷图\n3:宝珠迷宫\n4:storySkip\n5:打牌\n6:高能战斗\n****************")
        cmd = int(input("输入数字选项:").strip())
        if  cmd==1:
            print("run:正在读取文件数据...")
            txt=readDataTxt()
            if txt=='':
                print("error:文件数据读取失败")
                pass
            print(txt)
            print("run:修改数据")
            if win32_method.dataModeify(data=txt,dataOffset=15):#0/30/15
                print("completed:修改成功")
            else:
                continue
        elif cmd==2:
            #鬼屋
            storyPass2()
        # elif cmd==3:
        #     #宝珠迷宫
        #     storyPass3()
        elif cmd==-1:
            break
        elif cmd == 3:
            storyPass3(data_Offset=0)
        elif cmd == 4:
            while(1):
                skip()
        elif cmd == 5:
            #打牌
            while(1):
                playcard()
        elif cmd == 0:
            storyPass0()
        elif cmd ==5:
            print("run:正在读取文件数据...")
            txt = readDataTxt()
            if txt == '':
                print("error:文件数据读取失败")
                pass
            print(txt)
            print("run:修改数据")
            if win32_method.dataModeify(data=txt, dataOffset=0):
                print("completed:修改成功")
            else:
                continue
        elif cmd ==6:
            print("高能战斗")
            s=input("zhiling:")

            storyPass6(data_Offset=0,consume=int(s.split('.')[0]),maxCount=int(s.split('.')[1]))

        else:
            print("指令错误")



