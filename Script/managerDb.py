# -*- coding:utf8 -*-
import datetime
import time
import sqlite3
import os

class manager(object):
    def __init__(self,Vaildip):
        super(manager,self).__init__()
        self.Vaildip=Vaildip
        self.index=0
        self.tnow=datetime.datetime.now()
        self.tdelay=self.tnow+datetime.timedelta(minutes=10)

    def connect(self):
        currnetDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        dbPath = currnetDir + '/v2er.db'
        connect = sqlite3.connect(dbPath)
        cursor = connect.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS "proxy_ip" (
        "ip" varchar(15) PRIMARY KEY NOT NULL,
        "port" integer(6),
        "time" integer(11)
        );
        ''')
        return connect

    def insert(self,Database):
        cursor = Database.cursor()
        for self.index in range(len(self.Vaildip)-1):
            print((self.Vaildip[self.index][0], self.Vaildip[self.index][1], time.ctime()))
            sql = "insert or replace into proxy_ip VALUES ('%s','%s','%s')" % (self.Vaildip[self.index][0], self.Vaildip[self.index][1], time.ctime())
            cursor.execute(sql)
            Database.commit()
        Database.close()
        while self.tnow < self.tdelay:
            self.tnow = datetime.datetime.now()
            time.sleep(5)
            if self.tnow > self.tdelay:
                print("数据插入操作完成")

    def delete(self,Database):
        cursor = Database.cursor()
        while self.tnow<self.tdelay:
            self.tnow = datetime.datetime.now()
            time.sleep(5)
            if self.tnow>self.tdelay:
                sql="DELETE FROM `proxy_ip` order by Time limit 2 AND DELETE FROM `proxy_ip` WHERE IP=''"
                cursor.execute(sql)
                Database.commit()
            Database.close()
            print("数据删除操作完成")
