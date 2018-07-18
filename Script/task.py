import feedparser
import sqlite3
import time
import jpush
from jpush import common
from threading import Timer
import config
import io
import sys
import os
import urllib
import random

class PushService(object):
    def __init__(self):
        super(PushService,self).__init__()

        self._jpush = jpush.JPush(config.app_key, config.master_secret)
    #_jpush.set_logging("DEBUG")
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    def pushForAlias(self, id, msg, link):
        push = self._jpush.create_push()
        alias=[id]
        alias1={"alias": alias}
        push.audience = jpush.audience(
            alias1
        )

        ios = jpush.ios(alert=msg, sound="default", extras={'link': link})
        push.notification = jpush.notification(alert="", ios=ios)
        push.options = {"time_to_live":86400, "sendno":12345,"apns_production": config.is_release}
        push.platform = "ios"
        print(push.payload)
        # push.send()
        try:
            response=push.send()
        except common.Unauthorized:
            raise common.Unauthorized("Unauthorized")
        except common.APIConnectionException:
            raise common.APIConnectionException("conn")
        except common.JPushFailure:
            print("JPushFailure")
        except:
            print("Exception")

    def connect(self):
        # 上级目录
        currnetDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        dbPath = currnetDir + '/v2er.db'
        connect = sqlite3.connect(dbPath)
        return connect  

    def main(self, Database):
        cursor = Database.cursor()

        cursor.execute('select * from User where isOnline = 1')
        values = cursor.fetchall()

        # proxys = cursor.execute('select * from proxy_ip').fetchall()

        print("\n**************** START ****************")
        for value in values:
            name = value[1]
            lastMsgTime = value[2]
            feedURL = value[3]

            # proxyObj = random.choice(proxys)
            userAgent = random.choice(config.usr_agent)

            print("--------", name, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), "--------")
            print("Feed URL = ", feedURL)    
            # proxy = urllib.request.ProxyHandler( {'http': 'http://{}:{}'.format(proxyObj[0], proxyObj[1])} )
            d = feedparser.parse(feedURL, agent = userAgent)#, handlers = [proxy])

            if len(d.entries) == 0:
                continue

            # 取出第一条消息
            entrie = d.entries[0]
            title = entrie.title
            content = entrie.content[0].value
            published = time.mktime(entrie.updated_parsed)

            link = entrie.link
            print(link)
            print("最新消息时间戳: ", published)
            print("本地最后一条消息时间戳: ", lastMsgTime)
            print("标题: ", title)

            if lastMsgTime is not None and published > lastMsgTime:
                print("\033[1;31;40m正在发送通知\033[0m")
                self.pushForAlias(name, title, link)
            
            cursor.execute("update user set lastMsgTime = ? where name = ?", (published, name))
            print("--------", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), "--------")

        cursor.close()

        Database.commit()
        Database.close()
        print("**************** END ****************\n")

if __name__=='__main__':
    service=PushService()
    db = service.connect()
    service.main(db)
