from db.basedb import BaseDb
from utils.log_utils import logd
from vo.vo import DeviceVo, TaskVo, ActVo


class DbAct(BaseDb):

    def name(self):
        return self.__class__.__name__
        pass

    def create(self):
        return "CREATE TABLE IF NOT EXISTS " + self.name() + "(" \
                                                             "id INTEGER primary key AUTOINCREMENT" \
                                                             ",act_app TEXT" \
                                                             ",act_act TEXT" \
                                                             ",act_desc TEXT" \
                                                             ")"
        pass

    def select_id(self, id):
        self.cursor().execute("select * from " + self.name() + " where id =? ", id)
        result = self.cursor().fetchone()
        logd(result)
        if result is None:
            return
        res = ActVo()
        res.id = result['id']
        res.act_app = result['act_app']
        res.act_act = result['act_act']
        res.act_desc = result['act_desc']
        return res
        pass

    def select_task(self, act_app, act_act):
        self.cursor().execute("select * from " + self.name() + " where  act_app =? and act_act=?",
                              (act_app, act_act))
        result = self.cursor().fetchone()
        logd(result)
        if result is None:
            return
        res = ActVo()
        res.id = result['id']
        res.act_app = result['act_app']
        res.act_act = result['act_act']
        res.act_desc = result['act_desc']
        return res
        pass

    def insert(self, vo):
        sql = "INSERT INTO " + self.name() + " (act_app" \
                                             ",act_act" \
                                             ",act_desc" \
                                             ") values(?,?,?)"
        args = (vo.act_app, vo.act_act,vo.act_desc)
        self.doSql(sql, args)
        pass

    def update(self, vo):
        sql = "UPDATE " + self.name() + " SET act_app=? " \
                                        ",act_act=? " \
                                        ",act_desc=? " \
                                        "where id =?"
        args = (vo.act_app, vo.act_act,vo.act_desc, vo.id)
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
