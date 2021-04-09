import datetime
import time

from db.basedb import BaseDb
from utils.log_utils import logd


class DbRecord(BaseDb):

    def name(self):
        return self.__class__.__name__
        pass

    def create(self):
        return "CREATE TABLE IF NOT EXISTS " + self.name() + "(" \
                                                             "id INTEGER primary key AUTOINCREMENT" \
                                                             ",device TEXT" \
                                                             ",record_app TEXT" \
                                                             ",record_name TEXT" \
                                                             ",record_finish INTEGER DEFAULT 0" \
                                                             ")"
        pass

    def count(self, device, record_app, record_name):
        now0 = int(time.mktime(datetime.date.today().timetuple()))
        self.cursor().execute("select * from " + self.name() + " where device=? and record_app =? and record_name=? and record_finish>?",
                              (device, record_app, record_name,now0))
        result = self.cursor().fetchall()
        logd(result)
        if result is None:
            return 0

        return len(result)
        pass

    def insert(self, vo):
        sql = "INSERT INTO " + self.name() + " (device" \
                                             ",record_app" \
                                             ",record_name" \
                                             ",record_finish" \
                                             ") values(?,?,?,? )"
        args = (
            vo.device, vo.task_app, vo.task_name, vo.task_finish)
        self.doSql(sql, args)

        pass

    pass
