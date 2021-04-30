import datetime
import time

from task.base_options import BaseOptions
from utils.log_utils import loge
from vo.vo import TaskVo

g_app_name = "douyin"

g_point_name_tap_baoxiang_task = "tap_baoxiang_task"

g_point_name_tap_kanguanggao_task = "tap_kanguanggao_task"
g_point_name_tap_liulanshangpin_task = "tap_liulanshangpin_task"

g_point_name_tap_kanxiaoshuo_task = "tap_kanxiaoshuo_task"
g_point_name_tap_kanxiaoshuo_task_book = "tap_kanxiaoshuo_task_book"
g_point_name_tap_kanxiaoshuo_task_book_ad = "tap_kanxiaoshuo_task_book_ad"


class ProDouYinJiSuBan(BaseOptions):

    def package(self):
        return None
        pass

    def launcher(self):
        return None
        pass

    def openWait(self):
        loge("开启抖音极速版等待")
        self.sleep(10)
        self.back()
        for i in range(5):
            self.sleep(5)
            self.back()
            self.swipeVNxtPage()
            loge("视频下一页")
            pass
        pass

    def goTaskCenter(self):
        loge("去任务中心")
        self.click(self.screenVo.center_x, self.screenVo.bottomDp(26))
        self.sleep(8)

        self.swipeVPrePage()
        self.swipeVPrePage()
        self.swipeVPrePage()

        pass

    def kanshipin(self):
        self.swipe_v_times()
        pass

    def kanxiaoshuo(self):
        vo = self.getTaskDb().select_task(g_app_name, "kanxiaoshuo")

        if vo is None:
            vo = TaskVo()
            vo.device = self.deviceVo.device_u
            vo.task_app = g_app_name
            vo.task_name = "kanxiaoshuo"
            pass

        now0 = int(time.mktime(datetime.date.today().timetuple()))

        if now0 < vo.task_finish:
            return
            pass

        self.goTaskCenter()

        loge("滑动到看小说-点击")
        self.swipe_click(g_app_name, g_point_name_tap_kanxiaoshuo_task)

        self.sleep(5)

        loge("点击看小说书名")
        self.swipe_click(g_app_name, g_point_name_tap_kanxiaoshuo_task_book)

        loge("看小说")
        # 翻页一百次
        for i in range(4):
            # 活去看小说权限 看一次广告
            self.sleep(4)
            # 点击看小说中广告
            self.swipe_click(g_app_name, g_point_name_tap_kanxiaoshuo_task_book_ad)
            loge("小说广告")
            self.toAd(36)

            self.swipe_h_times()
            pass

        loge("推出小说")
        self.back()

        loge("退出书架")
        self.back()

        loge("退出去赚钱页面")
        self.back()

        vo.task_finish = int(time.time())
        self.getTaskDb().save(vo)

        pass

    def quguanggao(self):
        vo = self.getTaskDb().select_task(g_app_name, "quguanggao")

        if vo is None:
            vo = TaskVo()
            vo.device = self.deviceVo.device_u
            vo.task_app = g_app_name
            vo.task_name = "quguanggao"
            vo.task_time_jiange = 1205
            pass

        if int(time.time()) < vo.task_finish + vo.task_time_jiange:
            return
            pass

        self.goTaskCenter()

        loge("滑动到看广告-点击")
        self.swipe_click(g_app_name, g_point_name_tap_kanguanggao_task)
        loge("看广告任务")
        self.toAd(36)

        loge("退出去赚钱页面")
        self.back()

        vo.task_finish = int(time.time())
        self.getTaskDb().save(vo)

        pass

    def baoxiang(self):
        vo = self.getTaskDb().select_task(g_app_name, "baoxiang")

        if vo is None:
            vo = TaskVo()
            vo.device = self.deviceVo.device_u
            vo.task_app = g_app_name
            vo.task_name = "baoxiang"
            vo.task_time_jiange = 1205
            pass

        if int(time.time()) < vo.task_finish + vo.task_time_jiange:
            return
            pass

        self.goTaskCenter()

        loge("滑动到宝箱-点击")
        self.swipe_click(g_app_name, g_point_name_tap_baoxiang_task)
        loge("看广告任务")
        self.toAd(36)

        loge("退出去赚钱页面")
        self.back()

        vo.task_finish = int(time.time())
        self.getTaskDb().save(vo)

        pass

    def liulanshangpin(self):
        vo = self.getTaskDb().select_task(g_app_name, "liulanshangpin")

        if vo is None:
            vo = TaskVo()
            vo.device = self.deviceVo.device_u
            vo.task_app = g_app_name
            vo.task_name = "liulanshangpin"
            vo.task_time_jiange = 600
            vo.task_times = 3
            vo.task_time_use = 35
            pass

        allcount = self.getRecordDb().count(vo.device, vo.task_app, vo.task_name)
        if allcount >= vo.task_times:
            return
            pass

        if int(time.time()) < vo.task_finish + vo.task_time_jiange:
            return
            pass

        self.goTaskCenter()

        loge("滑动到浏览商品-点击")
        self.swipe_click(g_app_name, g_point_name_tap_liulanshangpin_task)
        loge("浏览商品")
        self.swipe_v_times(ptime=3, ltime=vo.task_time_use)

        loge("退出去赚钱页面")
        self.back()

        vo.task_finish = int(time.time())

        self.getTaskDb().save(vo)
        self.getRecordDb().insert(vo)
        pass


    def toAd(self, lookTime):
        loge("看广告")
        b = self.checkActivity("抖音广告")
        if not b:
            return
            pass

        while True:
            ffff
            pass

        loge(lookTime + "秒")

        self.sleep(lookTime)

        self.back()
        self.back()
        self.sleep(2.5)
        pass

    pass
