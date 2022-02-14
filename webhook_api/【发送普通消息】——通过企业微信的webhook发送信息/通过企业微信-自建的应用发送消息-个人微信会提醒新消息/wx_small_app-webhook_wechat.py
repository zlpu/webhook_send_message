# -*- coding:utf-8 -*-
"""
需求：通过这个脚本，我们自建的企业微信应用每天发送两次消息给企业微信成员'@all',每个人通过扫微信关联插件就可以在个人微信上看到企业微信中的信息
1.自建应用的参数：
Secret:fAELIbAOKKcEvZRTCmHH1891qd6InM3PpNMGAwrIxEY
corpid:ww99c341775886c227
AgentId:1000023
获取access_token：https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=ID&corpsecret=SECRET
发送消息api:https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=ACCESS_TOKEN
2.消息体：
new类：
msg={
    "agentid":
    "touser":"@all",
    "msgtype":"news",
    "news":{
        "articles":[
            {
            "title":"@你，您有新的信息待查看!",
            "description":"接收时间"+date_now,
            "url":需要跳转的网页地址,
            "picurl":消息卡片中图片的url
            }
        ]
    }
}
"""
import requests
import datetime






secret = "fAELIbAOKKcEvZRTCmHH1891qd6InM3PpNMGAwrIxEY"
corpid = "ww99c341775886c227"
get_token_url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=" + corpid + "&corpsecret=" + secret
access_token = requests.get(get_token_url).json()['access_token']
send_url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=" + access_token
date_now = datetime.datetime.now().strftime('%Y年%m月%d日 %H:%M:%S %p')
msg = {
    "agentid": 1000023,
    "touser": "@all",
    "msgtype": "news",
    "news": {
        "articles": [
            {
                "title": "@你，您有新的信息待查看!",
                "description": "接收时间:" + date_now,
                "url": "124.71.203.168:8001",
                "picurl": "https://t7.baidu.com/it/u=2294241244,1573074677&fm=193&f=GIF"
            }
        ]
    }
}




def send_msg():
    respond = requests.post(url=send_url, json=msg).json()
    if respond['errmsg'] == 'ok':
       print("消息发送成功！\n消息ID：" + respond['msgid'])
    else:
       print("消息发送失败\n报错信息如下：" + str(respond))
if __name__ == '__main__':
    send_msg()