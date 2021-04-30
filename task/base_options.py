import datetime
import os
import shutil

from db.db_act import DbAct
from db.db_point import DbPoint
from db.db_record import DbRecord
from db.db_task import DbTask
from utils.log_utils import logd, loge
from vo.vo import DeviceVo, ScreenVo, PointVo, ActVo
import xml.etree.cElementTree as et
import time
import re
import os
import os.path
from PIL import Image

from aip import AipOcr
from tkinter import messagebox


""" 你的 APPID AK SK """
APP_ID = '23759270'
API_KEY = 'idqcG6y0kLxE09rGKuzLhDGp'
SECRET_KEY = 'BtXG8R6cQ78l3SGSXG9GRSCiRKDTEgK1'
client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

dbPoint: DbPoint = DbPoint()
dbTask: DbTask = DbTask()
dbAct: DbAct = DbAct()
dbRecord: DbRecord = DbRecord()


class BaseOptions:
    deviceVo: DeviceVo = None
    screenVo: ScreenVo = ScreenVo()
    speed_fast = "200"
    speed_slow = "1200"
    g_swipe_times = 0

    def __init__(self, deviceVo_: DeviceVo):
        self.deviceVo = deviceVo_
        self.screen_info()
        pass

    def sleep(self, t):
        time.sleep(t)  # 休眠1秒
        pass

    def getTime(self):
        return time.time()
        pass

    def package(self):
        pass

    def launcher(self):
        pass

    def home(self):
        # popen返回文件对象，跟open操作一样
        cmd = r'adb -s {} shell input keyevent 3'.format(self.deviceVo.device_w)
        with os.popen(cmd, 'r') as f:
            text = f.read()
        logd(text)
        pass

    def colse(self):
        for i in range(6):
            self.back()
            pass
        self.home()
        pass

    def open(self):
        self.colse()

        # popen返回文件对象，跟open操作一样
        cmd = r'adb -s {} shell am start -n {}/{}'.format(self.deviceVo.device_w, self.package(), self.launcher())
        with os.popen(cmd, 'r') as f:
            text = f.read()
        logd(text)  # 打印cmd输出结果
        # gdl 需要判断是否成功
        self.openWait()
        pass

    def forceClose(self):

        # popen返回文件对象，跟open操作一样
        cmd = r'adb -s {} shell am force-stop {}'.format(self.deviceVo.device_w, self.package())
        with os.popen(cmd, 'r') as f:
            text = f.read()
        logd(text)  # 打印cmd输出结果
        # gdl 需要判断是否成功
        self.openWait()
        pass

    def openWait(self):
        pass

    def back(self):
        # popen返回文件对象，跟open操作一样
        cmd = r'adb -s {} shell input keyevent 4'.format(self.deviceVo.device_w)
        with os.popen(cmd, 'r') as f:
            text = f.read()
        logd(text)
        pass

    def pause(self, info="none"):
        messagebox.showinfo(self.deviceVo.device_w,info)

        # # popen返回文件对象，跟open操作一样
        # cmd = r'echo "pause {}:{} 暂停" >log.txt'.format(self.deviceVo.device_w, info)
        # with os.popen(cmd, 'r') as f:
        #     text = f.read()
        # # logd(text)
        #
        # cmd = r'start log.txt'
        # with os.popen(cmd, 'r') as f:
        #     text = f.read()
        # # logd(text)

        cmd = r'pause'
        with os.popen(cmd, 'r') as f:
            text = f.read()
        # logd(text)
        loge("继续运行")
        pass

    def currentAppActivity(self):
        self.sleep(5)
        # popen返回文件对象，跟open操作一样
        cmd = r'adb -s {} shell dumpsys activity'.format(self.deviceVo.device_w)
        with os.popen(cmd, 'r') as f:
            text = f.read()
        # logd(text)  # 打印cmd输出结果
        start_pos = text.index("mFocusedActivity")
        text = text[start_pos:]
        start_pos = text.index("{") + 1
        end_pos = text.index("}\n")
        text = text[start_pos:end_pos]

        temps = text.split(" ")

        for t in temps:
            if t.__contains__("/"):
                text = t
                continue
                pass
            pass
        temps = text.split("/")
        logd(temps)
        # gdl 需要判断是否成功
        return temps[0], temps[1]
        pass

    def checkActivity(self, desc):

        pkg, act = self.currentAppActivity()

        while True:
            vo = dbAct.select_task(pkg, act)
            if vo is None:
                self.saveCurrentActivity(desc)
                pass
            else:
                break
                pass
            pass

        return vo.act_desc == desc

        pass

    def dump(self):

        cmd = r'adb -s {} shell uiautomator dump'.format(self.deviceVo.device_w)
        with os.popen(cmd, 'r') as f:
            text = f.read()
        logd(text)  # 打印cmd输出结果
        # gdl 需要判断是否成功
        temps = text.split(":")
        res = "D:\\xml\\"

        self.pull(temps[1], res)
        pass

    def pull(self, src, res):
        src = src.replace("\n", "")
        if not os.path.exists(res):
            os.makedirs(res)
            pass

        cmd = r'adb -s {} pull {} {}'.format(self.deviceVo.device_w, src, res)

        with os.popen(cmd, 'r') as f:
            text = f.read()
        logd(text)  # 打印cmd输出结果
        pass

    def screen_info(self):
        # popen返回文件对象，跟open操作一样
        with os.popen(r'adb -s ' + self.deviceVo.device_w + r' shell wm size', 'r') as f:
            text = f.read()
        logd(text)  # 打印cmd输出结果

        # 输出结果字符串处理
        start_pos = text.index(':') + 1

        temps = text[start_pos:].strip().split("x")
        self.screenVo.set_wh(temps)

        # popen返回文件对象，跟open操作一样
        with os.popen(r'adb -s ' + self.deviceVo.device_w + r' shell wm density', 'r') as f:
            text = f.read()
        logd(text)  # 打印cmd输出结果
        # 输出结果字符串处理
        start_pos = text.index(':') + 1

        self.screenVo.density = float(text[start_pos:].strip()) / float(160)
        pass

    def tap_coord_by_name_id(self, attrib_name, text_name):
        source = et.parse("D:\\xml\\window_dump.xml")
        root = source.getroot()

        for node in root.iter("node"):
            if node.attrib[attrib_name] != text_name:
                continue
                pass

            bounds = node.attrib["bounds"]
            pattern = re.compile(r"\d+")
            coord = pattern.findall(bounds)

            int0 = int(coord[0])
            int1 = int(coord[1])
            int2 = int(coord[2])
            int3 = int(coord[3])
            if int2 == 0 and int3 == 0:
                return None, None
                pass

            x = (int2 - int0) / 2.0 + int0
            y = (int3 - int1) / 2.0 + int1
            return x, y
            pass
        return None, None
        pass

    def screenshot(self):
        cmd = r'adb -s {} exec-out screencap -p /sdcard/temp.jpg'.format(self.deviceVo.device_w)

        with os.popen(cmd, 'r') as f:
            text = f.read()
        logd(text)  # 打印cmd输出结果

        res = "D:\\xml\\"

        self.pull("/sdcard/temp.jpg", res)
        # self. resizeImage()
        pass

    def resizeImage(self):
        img = Image.open("D:\\xml\\temp.jpg")
        out = img.resize((self.screenVo.sw, self.screenVo.sh), Image.ANTIALIAS)
        # resize image with high-quality
        out.save("D:\\xml\\temp1.jpg", "png")
        pass

    def return_cordinate(self):
        """ 读取图片 """
        with open("D:\\xml\\temp.jpg", 'rb') as fp:
            """识别到信息以字典形式返回"""
            return client.general(fp.read())

    def click(self, x_, y_):
        x = str(x_)
        y = str(y_)
        cmd = r'adb -s {} shell input tap {} {}'.format(self.deviceVo.device_w, x, y)
        with os.popen(cmd, 'r') as f:
            text = f.read()
        logd(text)  # 打印cmd输出结果
        # gdl 需要判断是否成功
        pass

    def swipeVPrePage(self):
        x = str(self.screenVo.border_right)
        fromy = str(self.screenVo.h2)
        toy = str(self.screenVo.h9)

        cmd = r'adb -s {} shell input swipe {} {} {} {} {}'.format(self.deviceVo.device_w, x, fromy, x, toy,
                                                                   self.speed_fast)
        with os.popen(cmd, 'r') as f:
            text = f.read()
        logd(text)  # 打印cmd输出结果
        # gdl 需要判断是否成功
        pass

    def swipeVNxtPage(self):
        x = str(self.screenVo.border_right)
        fromy = str(self.screenVo.h7)
        toy = str(0)
        cmd = r'adb -s {} shell input swipe {} {} {} {} {}'.format(self.deviceVo.device_w, x, fromy, x, toy,
                                                                   self.speed_fast)
        with os.popen(cmd, 'r') as f:
            text = f.read()
        logd(text)  # 打印cmd输出结果
        # gdl 需要判断是否成功
        pass

    def swipeHPrePage(self):
        fromx = str(self.screenVo.border_left)
        y = str(self.screenVo.h5)
        tox = str(self.screenVo.border_right)
        cmd = r'adb -s {} shell input swipe {} {} {} {} {}'.format(self.deviceVo.device_w, fromx, y, tox, y,
                                                                   self.speed_fast)
        with os.popen(cmd, 'r') as f:
            text = f.read()
        logd(text)  # 打印cmd输出结果
        # gdl 需要判断是否成功
        pass

    def swipeHNxtPage(self):
        fromx = str(self.screenVo.border_right)
        y = str(self.screenVo.h5)
        tox = str(self.screenVo.border_left)
        cmd = r'adb -s {} shell input swipe {} {} {} {} {}'.format(self.deviceVo.device_w, fromx, y, tox, y,
                                                                   self.speed_fast)
        with os.popen(cmd, 'r') as f:
            text = f.read()
        logd(text)  # 打印cmd输出结果
        # gdl 需要判断是否成功
        pass

    def swipeVPre5_1(self):
        x = str(self.screenVo.border_right)
        fromy = str(self.screenVo.h3)
        toy = str(self.screenVo.h6)
        cmd = r'adb -s {} shell input swipe {} {} {} {} {}'.format(self.deviceVo.device_w, x, fromy, x, toy,
                                                                   self.speed_slow)
        with os.popen(cmd, 'r') as f:
            text = f.read()
        logd(text)  # 打印cmd输出结果
        # gdl 需要判断是否成功
        pass

    def swipeVNxt5_1(self):
        x = str(self.screenVo.border_right)
        fromy = str(self.screenVo.h6)
        toy = str(self.screenVo.h3)
        cmd = r'adb -s {} shell input swipe {} {} {} {} {}'.format(self.deviceVo.device_w, x, fromy, x, toy,
                                                                   self.speed_slow)
        with os.popen(cmd, 'r') as f:
            text = f.read()
        logd(text)  # 打印cmd输出结果
        # gdl 需要判断是否成功
        pass

    def swipe2Top(self):
        self.swipeVPrePage()
        self.swipeVPrePage()
        self.swipeVPrePage()
        pass

    def swipe_v_times(self, ptime=5, ltime=120):
        loge("竖向滑动")
        start_time = self.getTime()

        while True:
            self.sleep(ptime)
            self.swipeVNxtPage()
            loge("下一页")

            end_time = self.getTime()
            # 判断是否已经运行三分钟
            if end_time - start_time >= ltime:
                loge("退出")
                return
                pass
            pass
        pass

    def swipe_h_times(self, ptime=1, times=50):
        loge("横向滑动")
        for i in range(times):
            self.sleep(ptime)
            self.swipeHNxtPage()
            loge("下一页" + str(i))
            pass
        pass

    def getTaskDb(self):
        return dbTask
        pass

    def getRecordDb(self):
        return dbRecord
        pass

    def get_point(self, len=5):
        cmd = r'adb -s {} shell getevent -l -c {}'.format(self.deviceVo.device_w, len)
        with os.popen(cmd, 'r') as f:
            text = f.read()
        # logd(text)  # 打印cmd输出结果
        temps = text.split("\n")
        x1 = 0
        y1 = 0
        x2 = 0
        y2 = 0
        for t in temps:
            if not t.__contains__("/dev/input/event"):
                continue
                pass
            if not t.__contains__("EV_ABS"):
                continue
                pass
            values = t.strip().split(" ")
            if t.__contains__("ABS_MT_POSITION_X"):
                x2 = int(values[-1], 16)
                if x1 == 0:
                    x1 = x2
                    pass
                continue
                pass
            if t.__contains__("ABS_MT_POSITION_Y"):
                y2 = int(values[-1], 16)
                if y1 == 0:
                    y1 = y2
                    pass
                continue
                pass
            pass
        logd(x1 + " " + y1 + " " + x2 + " " + y2)
        return x1, y1, x2, y2
        pass

    pass

    def get_pointInfo(self, point_app, point_name):
        return dbPoint.select_point(point_app, point_name)
        pass

    def save_pointInfo(self, point_app, point_name, must=False, re_scale=False):
        vo: PointVo = self.get_pointInfo(point_app, point_name)
        if vo is None:
            vo = PointVo()
            vo.device = self.deviceVo.device_u
            vo.point_app = point_app
            vo.point_name = point_name
            pass

        now0 = int(time.mktime(datetime.date.today().timetuple()))

        if now0 < vo.point_time or not must:
            return
            pass

        x, y, swipe_times = self.swipe_2_getpoint1(re_scale)

        vo.point_x = x
        vo.point_y = y
        vo.point_swipe_times = swipe_times
        vo.point_time = int(time.time())

        dbPoint.save(vo)

        pass

    def swipe_2_getpoint1(self, re_scale=False):
        if re_scale:
            self.g_swipe_times = 0
            self.swipe2Top()
            pass

        x = 0
        y = 0
        while True:
            loge("当前滑动次数：{}".format(self.g_swipe_times))
            input_data = self.get_input_num("请输入操作(1下页 2定点 3重置 0退出):", [0, 1, 2, 3])

            if input_data == 1:
                self.swipeVNxt5_1()
                self.g_swipe_times += 1
                continue
                pass

            if input_data == 2:
                x, y = self.get_point()
                continue
                pass

            if input_data == 3:
                self.swipe2Top()
                self.g_swipe_times = 0
                continue
                pass
            break
            pass
        return x, y, self.g_swipe_times
        pass

    def get_input_num(self, hint, wannas):

        while True:
            pos = input(hint)

            if not pos.isdigit():
                continue

            pos = int(pos)

            if not wannas.__contains__(pos):
                continue
                pass

            return pos
            pass

        pass

    def swipe_click(self, point_app, point_name):
        vo = self.get_pointInfo(point_app, point_name)
        if vo is None:
            messagebox.showinfo(self.deviceVo.device_w, "请确定点击按钮{} {}".format(point_app, point_name))
            self.save_pointInfo(point_app, point_name, re_scale=False)
            pass

        for i in range(vo.point_swipe_times):
            self.swipeVNxt5_1()
            pass
        self.sleep(0.5)
        self.click(vo.point_x, vo.point_y)
        pass

    def saveCurrentActivity(self, desc=None):
        pkg, act = self.currentAppActivity()
        vo = dbAct.select_task(pkg, act)

        if vo is None:
            vo = ActVo()
            vo.act_app = pkg
            vo.act_act = act

            pass
        if desc is None:
            vo.act_desc = input("输入描述:")
            pass
        else:
            vo.act_desc = desc
            pass
        dbAct.save()
        pass


if __name__ == '__main__':
    d = DeviceVo()
    d.device_w = "192.168.16.209:5555"
    a = BaseOptions(d)
    a.pause()
    # a.screenshot()
    # print(a.get_point())
    # a.dump()
    # x,y=a.tap_coord_by_name_id('text',"来赚钱")
    # logd(x)
    # logd(y)
    # a.click(x,y)
    # print(return_cordinate("可领取金币", "D:\\xml\\temp.jpg"))

    pass
