# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import uiautomator2 as u2
from adbui import Device, Util
import time
import sqlite3
from uiautomator2 import Direction
import os
import my_ocr

import datetime

device_name = None
friend_talk_names = ('张俊华',)  # 要聊天的名字


# home_index_listView_items = None

con = None  # 数据库连接
cur = None  # 游标

my_name = ''  # 朋友圈中顶部我的名字

def openWx():
    d.app_start("com.tencent.mm")  # 打开程序
    pass


def wxaddFriend():
    # d.xpath(
    #     '//*[@resource-id="com.tencent.mm:id/e8y"]/android.widget.LinearLayout[1]/android.widget.RelativeLayout[2]/android.widget.LinearLayout[1]/android.widget.RelativeLayout[1]/android.widget.ImageView[1]').click()
    # d(resourceId="com.tencent.mm:id/d6z").info['text']
    #
    # d(text="接受")
    #
    # d(resourceId="com.tencent.mm:id/d6").click()

    pass


def wxsearchName(str):
    d(resourceId="com.tencent.mm:id/he6").click()
    d.xpath(
        '//*[@resource-id="com.tencent.mm:id/fdi"]/android.widget.LinearLayout[1]/android.widget.LinearLayout[1]/android.widget.RelativeLayout[1]').set_text(
        str)
    d.xpath('//*[@resource-id="com.tencent.mm:id/hf1"]/android.widget.RelativeLayout[2]').click()

    pass


def wxsendText(str):
    d.xpath('//android.widget.EditText').set_text(str)
    d(resourceId="com.tencent.mm:id/ay5").click()
    pass


def wxgoFaxian():
    d.xpath(
        '//*[@resource-id="com.tencent.mm:id/e8y"]/android.widget.LinearLayout[1]/android.widget.RelativeLayout[3]/android.widget.LinearLayout[1]/android.widget.RelativeLayout[1]/android.widget.ImageView[1]').click()
    pass


def wxgoPenyouquan():
    d(resourceId="android:id/title", text="朋友圈").click()
    pass


def wxsendPengyouquan(str):
    # 点击朋友圈发送
    d.xpath('//android.support.v7.widget.LinearLayoutCompat').click()
    d(resourceId="com.tencent.mm:id/ipm", text="从相册选择").click()

    # 点击选择图片分组
    d(resourceId="com.tencent.mm:id/j5").click()
    d(resourceId="com.tencent.mm:id/d7p", text="jianzhiku").click()
    # 选择图片
    d(resourceId="com.tencent.mm:id/h9a").click()
    # 确定图片
    d(resourceId="com.tencent.mm:id/d6").click()
    # 添加文字
    d(resourceId="com.tencent.mm:id/hxn").set_text()
    # 发送
    d(resourceId="com.tencent.mm:id/d6").click()
    pass


def wxswipe2PyqTop():
    while 1:
        head = d(resourceId="com.tencent.mm:id/hy6")
        if head.exists:
            global my_name
            d.swipe_ext(Direction.DOWN)
            my_name = d(resourceId="com.tencent.mm:id/hy6").child(resourceId="com.tencent.mm:id/fzg").info['text']
            print(my_name)
            return
            pass
        else:
            d.swipe_ext(Direction.DOWN)
            pass
        pass
    pass


def wxPengyouquanJietu(name, content):
    i = -1

    while 1:
        try:

            items = d(resourceId="com.tencent.mm:id/hyd")
            i += 1
            item = items[i]

            item_name = item.child(resourceId="com.tencent.mm:id/fzg")
            item_content = item.child(resourceId="com.tencent.mm:id/bmy", text=content)
            item_time = item.child(resourceId="com.tencent.mm:id/km")
            if item_content.exists:
                pass
            else:
                continue
                pass

            if item_name.exists:
                if item_name.info['text'] != name:
                    continue
                    pass
                pass
            else:
                i = -1
                d.swipe_ext(Direction.DOWN, scale=0.2)
                continue
                pass

            if item_time.exists:
                pass
            else:
                i = -1
                d.swipe_ext(Direction.UP, scale=0.2)
                continue
                pass

            # image = d.screenshot()
            os.system('adb -s ' + device_name + ' shell screencap -p /sdcard/screenshot.png')
            print("succ-------------------")
            return
        except BaseException:
            i = -1
            d.swipe_ext(Direction.UP)
            time.sleep(1)
    pass


def wxiter_names():
    i = -1
    end_name = ""

    while 1:
        try:
            global home_index_listView_items
            if home_index_listView_items is None:
                home_index_listView_items = d(resourceId="com.tencent.mm:id/fzg")
            i += 1
            temp_name = home_index_listView_items[i].info['text']
            is_need_to_talk = friend_talk_names.__contains__(temp_name)
            print("boolean:", str(is_need_to_talk), temp_name)
            if i == 0:
                if end_name == temp_name:
                    print("end")
                    return
            else:
                end_name = temp_name
        except BaseException:
            home_index_listView_items = None
            i = -1
            d.swipe_ext(Direction.UP)

            time.sleep(2)
    pass


def back2Home():
    d.press("back")
    d.press("back")
    d.press("back")
    d.press("back")
    d.press("back")
    d.press("back")
    d.press("back")
    d.press("back")
    d.press("home")
    pass



def openZrb():
    d.app_start("com.jianzhiku.zhongrenbang")  # 打开程序
    pass


def goXuanshangdating():
    d(resourceId="com.jianzhiku.zhongrenbang:id/hall_tab").click()
    pass


def goZhuanfa():
    d(resourceId="com.jianzhiku.zhongrenbang:id/r9").click()
    pass


def clickZhuanfaTaskItem():
    i = -1
    canLoadMore = ""

    while 1:
        try:

            items = d(resourceId="com.jianzhiku.zhongrenbang:id/v")
            i += 1
            item = items[i]
            if i == 2:
                # //通过连续三个item内容来判断是否滑动到底部
                temp = items[0]
                item0Str1 = temp.child(resourceId="com.jianzhiku.zhongrenbang:id/item_title").info['text']
                item0Str2 = temp.child(resourceId="com.jianzhiku.zhongrenbang: id / item_gongzi").info['text']

                temp = items[1]
                item1Str1 = temp.child(resourceId="com.jianzhiku.zhongrenbang:id/item_title").info['text']
                item1Str2 = temp.child(resourceId="com.jianzhiku.zhongrenbang: id / item_gongzi").info['text']
                temp = items[2]
                item2Str1 = temp.child(resourceId="com.jianzhiku.zhongrenbang:id/item_title").info['text']
                item2Str2 = temp.child(resourceId="com.jianzhiku.zhongrenbang: id / item_gongzi").info['text']
                canLoadMore_temp = item0Str1 + item0Str2 + item1Str1 + item1Str2 + item2Str1 + item2Str2

                if canLoadMore == canLoadMore_temp:
                    canLoadMore = "load_end"
                    return
                    pass
                else:
                    canLoadMore = canLoadMore_temp
                    pass
                pass

            item.click()
            doPyqZhuanfaTask()
            return
        except BaseException:
            i = -1
            if canLoadMore == "load_end":
                return
                pass
            d.swipe_ext(Direction.UP)
    pass


def doPyqZhuanfaTask():
    # 底部按钮
    btn = d(resourceId="com.jianzhiku.zhongrenbang:id/btn_add")
    if "立即报名" not in btn.info["text"]:
        d.press("back")
        return
        pass

    # 判断 条件1中是否含有朋友圈字样 有 就是朋友圈任务 那么就做
    tiaojian1 = d(resourceId="com.jianzhiku.zhongrenbang:id/step_detail_nocap")
    if "朋友圈" not in tiaojian1.info['text']:
        d.press("back")
        return
        pass

    # //接取任务
    btn.click()
    mission_title = d(resourceId="com.jianzhiku.zhongrenbang:id/mission_title").info["text"]
    owner_name = d(resourceId="com.jianzhiku.zhongrenbang:id/owner").info["text"]
    mission_money = d(resourceId="com.jianzhiku.zhongrenbang:id/mission_money").info["text"]

    # 滑动到复制文字按钮 这样能保证 复制文字控件全面展示
    while 1:
        btn_copytext = d(resourceId="com.jianzhiku.zhongrenbang:id/copy")
        if btn_copytext is None:
            d.swipe_ext(Direction.UP, scale=0.2)
            pass
        else:
            break
            pass
        pass
    # 复制文字
    copy_content = d(resourceId="com.jianzhiku.zhongrenbang:id/zfcontent").info["text"]

    # 滑动到下载图片按钮并点击
    while 1:
        btn_copyimg = d(resourceId="com.jianzhiku.zhongrenbang:id/qrdownload_btn")
        if btn_copytext is None:
            d.swipe_ext(Direction.UP, scale=0.2)
            pass
        else:
            btn_copyimg.click()
            break
            pass
        pass

    # 将接取的任务 存入数据库
    insertPyqZf(device_name, owner_name, copy_content)

    # 去微信
    back2Home()
    openWx()
    wxgoFaxian()
    wxgoPenyouquan()
    wxsendPengyouquan(copy_content)
    updatePyqZfzftime(device_name, owner_name, copy_content)

    back2Home()
    openZrb()
    goXuanshangdating()
    goZhuanfa()

    pass


def getDb():
    global con
    if con is None:
        con = sqlite3.connect("DEMO.db")
        pass

    global cur
    if cur is None:
        cur = con.cursor()
        pass
    pass


def createDataTables():
    getDb()
    sql = "CREATE TABLE IF NOT EXISTS test(id INTEGER primary key AUTOINCREMENT,name TEXT,age INTEGER)"
    cur.execute(sql)
    sql = "CREATE TABLE IF NOT EXISTS zrb_wx_pyq_zf(" \
          "id INTEGER primary key AUTOINCREMENT" \
          ",device TEXT not null" \
          ",owner_name TEXT not null" \
          ",mission_title TEXT not null" \
          ",mission_money TEXT not null" \
          ",copy_content TEXT not null" \
          ",jiequ_time INTEGER DEFAULT 0" \
          ",zhuanfa_time INTEGER DEFAULT 0" \
          ",wancheng_time INTEGER DEFAULT 0" \
          ")"
    cur.execute(sql)
    con.commit()
    pass


def delete():
    getDb()
    cur.execute("DELETE FROM test WHERE id=?", (1,))
    pass


def insertPyqZf(device, owner_name, mission_title, mission_money, copy_content):
    getDb()
    # ②：添加单条数据
    cur.execute("INSERT INTO zrb_wx_pyq_zf (device,owner_name,mission_title ,mission_money,copy_content,jiequ_time) "
                "values(?,?,?,?,?,?)",
                (device, owner_name, mission_title, mission_money, copy_content, int(time.time())))
    con.commit()
    pass


def updatePyqZfzftime(device, owner_name, mission_title, mission_money, copy_content):
    getDb()
    cur.execute("UPDATE zrb_wx_pyq_zf "
                "SET zhuanfa_time=? "
                "WHERE device=? and "
                "owner_name =? and "
                "mission_title =? and "
                "mission_money =? and "
                "copy_content=?",
                (int(time.time()), device, owner_name, mission_title, mission_money, copy_content))
    pass


def updatePyqZfwctime(device, owner_name, mission_title, mission_money, copy_content):
    getDb()
    cur.execute("UPDATE zrb_wx_pyq_zf "
                "SET wancheng_time=? "
                "WHERE device=? and "
                "owner_name =? and "
                "mission_title =? and "
                "mission_money =? and "
                "copy_content=?",
                (int(time.time()), device, owner_name, mission_title, mission_money, copy_content))
    pass


# def selectPyqZfTask():
#     getDb()
#     cur.execute("select * from zrb_wx_pyq_zf where zhuanfa_time !=0 and wancheng_time=0")
#     return cur.fetchone()
#     pass


if __name__ == '__main__':
    device_name = 'BQ6PWKPBGQHIWKAI'
    d = u2.connect(device_name)
    createDataTables()

    # 搜索人发送消息聊天
    # back2Home()
    # openWx()
    # searchName()
    # sendText()

    # 发送朋友圈
    # back2Home()
    # openWx()
    # goFaxian()
    # goPenyouquan()
    # sendPengyouquan("sss")

    # swipe2PyqTop()
    # jietu("陈春旭 乐乐", "跟北京协和王京岚教授团队免费学血气分析，强烈推荐👍")

    pass
