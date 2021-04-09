from db.basedb import BaseDb
from utils.log_utils import logd
from vo.vo import DeviceVo, PointVo


class DbPoint(BaseDb):

    def name(self):
        return self.__class__.__name__
        pass

    def create(self):
        return "CREATE TABLE IF NOT EXISTS " + self.name() + "(" \
                                                             "id INTEGER primary key AUTOINCREMENT" \
                                                             ",device TEXT" \
                                                             ",point_app TEXT" \
                                                             ",point_name TEXT" \
                                                             ",point_x INTEGER DEFAULT 0" \
                                                             ",point_y INTEGER DEFAULT 0" \
                                                             ",point_swipe_times INTEGER DEFAULT 0" \
                                                             ",point_time INTEGER DEFAULT 0" \
                                                             ")"
        pass

    def select_id(self, id):
        self.cursor().execute("select * from " + self.name() + " where id =? ", id)
        result = self.cursor().fetchone()
        logd(result)
        if result is None:
            return
        res = PointVo()
        res.id = result['id']
        res.device = result['device']
        res.point_app = result['point_app']
        res.point_name = result['point_name']
        res.point_x = result['point_x']
        res.point_y = result['point_y']
        res.point_swipe_times = result['point_swipe_times']
        res.point_time = result['point_time']
        return res
        pass

    def select_point(self, device, point_app, point_name):
        self.cursor().execute("select * from " + self.name() + " where device=? and point_app=? and point_name=?",
                              (device,point_app, point_name))
        result = self.cursor().fetchone()
        logd(result)
        if result is None:
            return
        res = PointVo()
        res.id = result['id']
        res.device = result['device']
        res.point_app = result['point_app']
        res.point_name = result['point_name']
        res.point_x = result['point_x']
        res.point_y = result['point_y']
        res.point_swipe_times = result['point_swipe_times']
        res.point_time = result['point_time']
        return res
        pass

    def insert(self, vo):
        sql = "INSERT INTO " + self.name() + " (device" \
                                             ",point_app" \
                                             ",point_name" \
                                             ",point_x" \
                                             ",point_y" \
                                             ",point_swipe_times" \
                                             ",point_time" \
                                             ") values(?,?,?,?,?,?,?)"
        args = (vo.device, vo.point_app, vo.point_name, vo.point_x, vo.point_y, vo.point_swipe_times, vo.point_time)
        self.doSql(sql, args)
        pass

    def update(self, vo):
        sql = "UPDATE " + self.name() + " SET device=? " \
                                        ",point_app=? " \
                                        ",point_name=? " \
                                        ",point_x=? " \
                                        ",point_y=? " \
                                        ",point_swipe_times=? " \
                                        ",point_time=? " \
                                        "where id =?"
        args = (
        vo.device, vo.point_app, vo.point_name, vo.point_x, vo.point_y, vo.point_swipe_times, vo.point_time, vo.id)
        self.doSql(sql, args)
        pass

    def save(self, vo):
        if vo.id is None:
            self.insert(vo)
            pass

        temp = self.select_id(vo.id)
        if temp is None:
            self.insert(vo)
            pass
        else:
            self.update(vo)
            pass
        pass

    pass
