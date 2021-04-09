from db.basedb import BaseDb
from utils.log_utils import logd
from vo.vo import DeviceVo, TaskVo


class DbTask(BaseDb):

    def name(self):
        return self.__class__.__name__
        pass

    def create(self):
        return "CREATE TABLE IF NOT EXISTS " + self.name() + "(" \
                                                             "id INTEGER primary key AUTOINCREMENT" \
                                                             ",device TEXT" \
                                                             ",task_app TEXT" \
                                                             ",task_name TEXT" \
                                                             ",task_time_jiange INTEGER DEFAULT 0" \
                                                             ",task_finish INTEGER DEFAULT 0" \
                                                             ",task_times INTEGER DEFAULT 0" \
                                                             ",task_time_use INTEGER DEFAULT 0" \
                                                             ")"

        pass

    def select_id(self, id):
        self.cursor().execute("select * from " + self.name() + " where id =? ", id)
        result = self.cursor().fetchone()
        logd(result)
        if result is None:
            return
        res = TaskVo()
        res.id = result['id']
        res.device = result['device']
        res.task_app = result['task_app']
        res.task_name = result['task_name']
        res.task_time_jiange = result['task_time_jiange']
        res.task_finish = result['task_finish']
        res.task_times = result['task_times']
        res.task_time_use = result['task_time_use']
        return res
        pass

    def select_task(self, device, task_app, task_name):
        self.cursor().execute("select * from " + self.name() + " where device=? and task_app =? and task_name=?",
                              (device,task_app, task_name))
        result = self.cursor().fetchone()
        logd(result)
        if result is None:
            return
        res = TaskVo()
        res.id = result['id']
        res.device = result['device']
        res.task_app = result['task_app']
        res.task_name = result['task_name']
        res.task_time_jiange = result['task_time_jiange']
        res.task_finish = result['task_finish']
        res.task_times = result['task_times']
        res.task_time_use = result['task_time_use']
        return res
        pass

    def insert(self, vo):
        sql = "INSERT INTO " + self.name() + " (device" \
                                             ",task_app" \
                                             ",task_name" \
                                             ",task_time_jiange" \
                                             ",task_finish" \
                                             ",task_times" \
                                             ",task_time_use" \
                                             ") values(?,?,?,?,?,?,?)"
        args = (
        vo.device, vo.task_app, vo.task_name, vo.task_time_jiange, vo.task_finish, vo.task_times, vo.task_time_use)
        self.doSql(sql, args)
        pass

    def update(self, vo):
        sql = "UPDATE " + self.name() + " SET device=? " \
                                        ",task_app=? " \
                                        ",task_name=? " \
                                        ",task_time_jiange=? " \
                                        ",task_finish=? " \
                                        ",task_times=? " \
                                        ",task_time_use=? " \
                                        "where id =?"
        args = (
        vo.device, vo.task_app, vo.task_name, vo.task_time_jiange, vo.task_finish, vo.task_times, vo.task_time_use,
        vo.id)
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
