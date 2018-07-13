import feedparser
import sqlite3
import time
import jpush
from jpush import common
from threading import Timer
import config

_jpush = jpush.JPush(config.app_key, config.master_secret)
# _jpush.set_logging("DEBUG")


def pushForAlias(id, msg):
    push = _jpush.create_push()
    alias=[id]
    alias1={"alias": alias}
    push.audience = jpush.audience(
        alias1
    )

    ios = jpush.ios(alert=msg, sound="default")
    push.notification = jpush.notification(alert="Hello world with audience!", ios=ios)
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


def connectDB():
    connect = sqlite3.connect('/home/ubuntu/v2erBackend/v2er.db')

    cursor = connect.cursor()

    cursor.execute('select * from user')
    values = cursor.fetchall()

    for value in values:
        id = value[0]
        name = value[1]
        lastMsgTime = value[2]
        feedURL = value[3]

        print("--------", name, "(", id,")", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), "--------")
        print("Feed URL = ", feedURL)

        d = feedparser.parse(feedURL)
       
        # 取出第一条消息
        entrie = d.entries[0]
        title = entrie.title
        content = entrie.content[0].value
        published = time.mktime(entrie.updated_parsed)

        print("最新消息时间戳: ", published)
        print("本地最后一条消息时间戳: ", lastMsgTime)
        print("标题: ", title)
        print("--------", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), "--------")

        if lastMsgTime is not None and published > lastMsgTime:
            pushForAlias(id, title)
        
        cursor.execute("update user set lastMsgTime = ? where id = ?", (published, id))

    cursor.close()

    connect.commit()
    connect.close()

connectDB()
