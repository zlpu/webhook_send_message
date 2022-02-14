#!/usr/bin/python3
# -*- coding:utf-8 -*-
import datetime

import requests
import json
from threading import Thread
import sys

"""
用途：用于zabbix告警配置中通过webhook脚本方式发送告警消息，消息发送给指定用户（非群聊中）
说明：
1.需要更改5个地方：已标注
2.适用于企业微信自建应用发送消息给指定的人。
3.消息类型：text(方便在个人微信中查看告警信息，个人微信暂不支持查看markdown类型消息)
4.python 使用的requests模块，如果未安装请先pip install requests
"""


"""1.企业微信全局配置"""
#01自建应用发送消息请求地址（企业微信统一接口，不需要更改）
url_my_wx_app = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token="
#02.公司id,在企业微信后台可以查看到（需修改，改成自己公司的id）(修改1)
wx_corpid="ww99c341775886c227"
#03.应用的secert,在创建应用以后可以看到（需修改，改成自己创建的应用secert）(修改2)
wx_secret="kbYrcCpP4dpKX9rrQ0yRun3whHsIz3Vgw3QKHg9Ni2U"

headers = {
    'Content-Type': 'application/json;charset=utf-8'
}


"""2.发送部分-函数体"""
def send_message_wx(from_zabbix_subject, from_zabbix_message):
    # 消息体
    json_message = {
        "agentid": 1000013,#应用的ID（修改3）
        "touser": "@all",#消息接收人，@all表示发送给所有人，"p1|z1"表示发送给这个两位用户（修改4）
        "msgtype": "text",
        "text": {
            "content": from_zabbix_subject + "\n\n" + from_zabbix_message,
            # 企业微信聊天界面告警消息跳转的url,比如grafana界面(修改5)
        },
    }
    # 发送
    '''(1)access_token是应用调用api的凭证，由 corpid和corpsecret换取。
        正常情况下AccessToken有效期为7200秒，有效期内重复获取返回相同结果。access_token至少保留512字节的存储空间。
        请求方式：GET（HTTPS）
        请求URL：https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=ID&corpsecret=SECRET
    '''
    try:
        wx_get_token_url="https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid="+wx_corpid+"&corpsecret="+wx_secret
        wx_access_token=requests.get(url=wx_get_token_url).json()["access_token"]
        respond_wx = requests.post(url=url_my_wx_app+wx_access_token, headers=headers, data=json.dumps(json_message))
        if respond_wx.json()["errmsg"] == "ok":
            print("企业微信自建应用告警信息发送成功！")
        else:
            print("企业微信自建应用发送消息异常\n"+str(respond_wx.json()))
        return respond_wx
    # 如有异常则抛出异常
    except Exception as e:
        print("企业微信发送消息异常\n"+str(e))

#调用线程方式运行函数，因为后期可能会增加飞书和钉钉的接口
def main():
    # 添加函数到线程1，注意添加两个需要的参数
    t1 = Thread(target=send_message_wx, args=(from_zabbix_subject, from_zabbix_message,))
    # 开始运行线程1
    try:
        t1.start()
    except Exception as e:
        print("微信机器人发送消息异常(线程)"+str(e))


if __name__ == '__main__':
    from_zabbix_subject = sys.argv[1]  # 接收zabbix告警的标题
    from_zabbix_message = sys.argv[2]  # 接收zabbix平台的告警信息（告警信息格式在zabbix中定义好，要与此脚本中定义好的文本类型一致）
    main()  # 执行主程序，两个线程同时执行
