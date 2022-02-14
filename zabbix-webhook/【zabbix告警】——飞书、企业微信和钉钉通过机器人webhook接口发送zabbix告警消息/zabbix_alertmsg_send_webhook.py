#!/usr/bin/python3
# -*- coding:utf-8 -*-
import datetime

import requests
import json
from threading import Thread
import sys

"""
用途：用于zabbix告警配置中通过webhook脚本方式发送告警消息。

说明：
1.需要更改4个地方：
-01.url_my_feishu =" "
   .url_my_wx=" "
   .url_my_dingding=" "
-02."href":""
-03.钉钉消息体中的at对象

2.适用于企业微信、钉钉和飞书的群聊机器人webhook,不是自建应用的webhook。
3.消息类型：富文本类
飞书和企业微信的机器人webhook-markdown消息类型不支持@用户
4.python 使用的requests模块，如果未安装请先pip install requests
"""

"""1.全局配置"""
'''
复制你的webhook地址粘贴进url内
'''
# 飞书群聊机器人webhook地址(修改1,如果不需要这种方式请将下面一行注释掉,如果需要请更改为自己的url）
url_my_feishu = "https://open.feishu.cn/open-apis/bot/v2/hook/ebfda356-cc93-4628-ae86-2442008ee3ec"
# 企业微信群聊机器人webhook地址(修改1,如果不需要这种方式请将下面一行注释掉,如果需要请更改为自己的url)
url_my_wx = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=167c4082-8510-4539-87a0-69aecb94f320"
# 钉钉群聊机器人的webhook地址(修改1,如果不需要这种方式请将下面一行注释掉,如果需要请更改为自己的url)
url_my_dingding="https://oapi.dingtalk.com/robot/send?access_token=4d94bb1a87b8f1bb15f8100671bcd5e9e36acc4ad04379aaf7afea8c5a32b99e"

headers = {
    'Content-Type': 'application/json;charset=utf-8'
}

"""2.函数体"""
'''
飞书发送消息的函数
'''
def send_message_feishu(from_zabbix_subject, from_zabbix_message):
    # 消息体
    json_message = {
        "msg_type": "post",
        "content": {
            "post": {
                "zh-CN": {
                    "title": from_zabbix_subject,
                    "content": [
                        [{
                            "tag": "text",
                            "text": from_zabbix_message+"\n"

                        },
                            {"tag": "a",
                             # 飞书聊天界面告警消息跳转的url,比如grafana界面(修改2)
                             "text": "点击查看详情",
                             "href": "192.168.32.136:3000"

                             }
                        ]
                    ]
                }
            }
        }
    }
    # 发送
    try:
        response_feishu = requests.post(url_my_feishu, headers=headers, data=json.dumps(json_message))
        if response_feishu.json()["StatusMessage"] == "success":
            print("飞书机器人告警信息发送成功！")
        else:
            print("飞书机器人发送消息异常"+str(response_feishu.json()))
        return response_feishu
    # 如有异常则抛出异常
    except Exception as e:
        print("飞书机器人发送消息异常\n"+str(e))


'''
企业微信发送消息的函数
'''


def send_message_wx(from_zabbix_subject, from_zabbix_message):
    # 消息体
    json_message = {
        "msgtype": "markdown",
        "markdown": {
            "content": from_zabbix_subject + "\n>" + from_zabbix_message +
                       "\n<font color='#8B0000'>历史数据</font>：[查看详情](192.168.32.136:3000)",
            # 企业微信聊天界面告警消息跳转的url,比如grafana界面(修改2)

        },
    }
    # 发送
    try:
        respond_wx = requests.post(url=url_my_wx, headers=headers,data=json.dumps(json_message))
        if respond_wx.json()["errmsg"] == "ok":
            print("企业微信机器人告警信息发送成功！")
        else:
            print("企业微信机器人发送消息异常\n"+str(respond_wx.json()))
        return respond_wx
    # 如有异常则抛出异常
    except Exception as e:
        print(e)
        print("企业微信机器人发送消息异常\n"+str(e))

'''钉钉发送消息的函数'''
def send_message_dd(from_zabbix_subject, from_zabbix_message):
    #消息体（markdown需要\n\n才能换行）
    json_message={
        "msgtype":"markdown",
        "markdown":{
            "title":from_zabbix_subject,
            "text":"#### "+from_zabbix_subject+"\n"+from_zabbix_message
        },
            "at":{# (修改3)
                # "atMobiles":["18827340310"],#根据注册的手机号@相关的用户
                # "atUserIds":["puzhenglin"],#根据用户id@相关用户
                "isAtAll": True#是否@全员
            }
        }

    #发送
    try:
        respond_dd=requests.post(url=url_my_dingding,headers=headers,data=json.dumps(json_message))
        if respond_dd.json()["errmsg"]=="ok":
            print("钉钉消息发送成功！")
        else:
            print("钉钉机器人发送消息异常\n"+str(respond_dd.json()))
        return respond_dd
    except Exception as e:
        print("钉钉机器人发送消息异常\n"+str(e))

# 使用python的多线程同时执行这两个函数，不会因为第一个函数出错导致第二个函数不执行
def main():
    # 添加第一个函数到线程1，注意添加两个的参数
    t1 = Thread(target=send_message_feishu, args=(from_zabbix_subject, from_zabbix_message,))
    # 添加第二个函数到线程2，注意添加两个需要的参数
    t2 = Thread(target=send_message_wx, args=(from_zabbix_subject, from_zabbix_message,))
    # 添加第三个函数到线程3，注意添加两个需要的参数
    t3 = Thread(target=send_message_dd, args=(from_zabbix_subject, from_zabbix_message,))
    # 开始运行线程1
    try:
        t1.start()
    except Exception as e:
       print("飞书机器人发送消息异常(线程)"+str(e))
    # 开始运行线程2
    try:
        t2.start()
    except Exception as e:
        print("微信机器人发送消息异常(线程)"+str(e))
    #开始运行线程3
    try:
        t3.start()
    except Exception as e:
        print("钉钉机器人发送消息异常(线程)"+str(e))

"""3.主函数"""
if __name__ == '__main__':
    from_zabbix_subject = sys.argv[1]    # 接收zabbix告警的标题
    from_zabbix_message = sys.argv[2]    # 接收zabbix平台的告警信息（告警信息格式在zabbix中定义好，要与此脚本中定义好的文本类型一致）
    main()  # 执行主程序，3个线程同时执行