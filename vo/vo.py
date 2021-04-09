class DeviceVo:
    id = None
    device_u = None
    device_w = None
    pass


class TaskVo:
    id = None
    device = None
    task_app = None
    task_name = None
    task_time_jiange = 0  # 任务间隔
    task_times = 0  # 任务次数
    task_time_use = 0  # 任务用时
    task_finish = 0  # 任务完成时间
    pass


class ActVo:
    id = None
    act_app = None
    act_act = None
    act_desc = None
    pass


class PointVo:
    id = None
    device = None
    point_app = None
    point_name = None
    point_x = 0
    point_y = 0
    point_swipe_times = 0
    point_time = 0
    pass


class ScreenVo:
    density: float = None

    sw = None
    sh = None

    w1 = None
    w2 = None
    w3 = None
    w4 = None
    w5 = None
    w6 = None
    w7 = None
    w8 = None
    w9 = None

    h1 = None
    h2 = None
    h3 = None
    h4 = None
    h5 = None
    h6 = None
    h7 = None
    h8 = None
    h9 = None

    border_top = 10
    border_left = 10
    border_right = None
    border_bottom = None

    center_x = None
    center_y = None

    def __init__(self):
        pass

    def set_wh(self, temps):
        self.sw = int(temps[0])
        self.sh = int(temps[1])
        self.center_x = self.sw / 2
        self.center_y = self.sh / 2

        self.w1 = self.sw / 10
        self.h1 = self.sh / 10

        self.w2 = self.w1 * 2
        self.h2 = self.h1 * 2

        self.w3 = self.w1 * 3
        self.h3 = self.h1 * 3

        self.w4 = self.w1 * 4
        self.h4 = self.h1 * 4

        self.w5 = self.w1 * 5
        self.h5 = self.h1 * 5

        self.w6 = self.w1 * 6
        self.h6 = self.h1 * 6

        self.w7 = self.w1 * 7
        self.h7 = self.h1 * 7

        self.w8 = self.w1 * 8
        self.h8 = self.h1 * 8

        self.w9 = self.w1 * 9
        self.h9 = self.h1 * 9

        self.border_right = self.sw - 10
        self.border_bottom = self.sh - 10

        pass

    def bottomDp(self, dpv):
        return self.sh - self.dp2px(dpv)
        pass

    def dp2px(self, dpv):
        return int(dpv * self.density + 0.5)
        pass

    def px2dp(self, pxv):
        return int(pxv / self.density + 0.5)
        pass

    pass
