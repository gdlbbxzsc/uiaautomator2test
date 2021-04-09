import sqlite3

from utils.log_utils import logd

conn = None  # 数据库连接
cursor = None  # 游标


def _init_db():
    global conn
    if conn is None:
        conn = sqlite3.connect("DEMO.db")
        pass

    global cursor
    if cursor is None:
        cursor = conn.cursor()
        pass

    pass


class BaseDb:

    def __init__(self) -> object:
        _init_db()
        sql = self.create()
        logd(sql)
        self.doSql(sql)
        pass

    @staticmethod
    def db():
        return conn
        pass

    @staticmethod
    def cursor():
        return cursor
        pass

    def name(self):
        pass

    def create(self):
        pass

    def doSql(self, sql, args=None):
        if args is None:
            self.cursor().execute(sql )
        else:
            self.cursor().execute(sql, args)
        self.db().commit()
        pass
