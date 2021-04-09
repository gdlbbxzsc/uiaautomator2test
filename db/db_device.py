from db.basedb import BaseDb
from utils.log_utils import logd
from vo.vo import DeviceVo


class DbDevice(BaseDb):

    def name(self):
        return self.__class__.__name__
        pass

    def create(self):
        return "CREATE TABLE IF NOT EXISTS " + self.name() + "(" \
                                                             "id INTEGER primary key AUTOINCREMENT" \
                                                             ",device_u TEXT" \
                                                             ",device_w TEXT" \
                                                             ")"

        pass

    def select_id(self, id):
        self.cursor().execute("select * from " + self.name() + " where id =? ", id)
        result = self.cursor().fetchone()
        logd(result)
        if result is None:
            return
        res = DeviceVo()
        res.id = result['id']
        res.device_u = result['device_u']
        res.device_w = result['device_w']
        return res
        pass

    def select_device_u(self, device_u):
        self.cursor().execute("select * from " + self.name() + " where device_u =? ",
                              (device_u,))
        result = self.cursor().fetchone()
        logd(result)
        if result is None:
            return
        res = DeviceVo()
        res.id = result['id']
        res.device_u = result['device_u']
        res.device_w = result['device_w']
        return res
        pass

    def select_device_w(self, device_w):
        self.cursor().execute("select * from " + self.name() + " where device_w =? ",
                              (device_w,))
        result = self.cursor().fetchone()
        logd(result)
        if result is None:
            return
        res = DeviceVo()
        res.id = result['id']
        res.device_u = result['device_u']
        res.device_w = result['device_w']
        return res
        pass

    def count_device(self, device_u, device_w):
        self.cursor().execute("select * from " + self.name() + " where device_u =? or device_w =?",
                              (device_u, device_w))
        result = self.cursor().fetchall()
        logd(result)
        if result is None:
            return 0

        return len(result)
        pass

    def deleteAll(self):
        sql = "DELETE FROM " + self.name()
        self.doSql(sql)
        pass

    def insert(self, vo):
        sql = "INSERT INTO " + self.name() + " (device_u,device_w) values(?,?)"
        args = (vo.device_u, vo.device_w)
        self.doSql(sql, args)
        pass

    def update(self, vo):
        sql = "UPDATE " + self.name() + " SET device_u=? ,device_w=? where id =?"
        args = (vo.device_u, vo.device_w, vo.id)
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
