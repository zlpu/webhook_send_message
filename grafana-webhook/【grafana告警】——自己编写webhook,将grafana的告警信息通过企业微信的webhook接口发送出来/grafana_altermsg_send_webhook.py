# -*- coding:utf-8 -*-
# coding:utf-8
'''
项目介绍：
Grafana支持prometheus等部分开源系统的告警功能，使用的webhook的方式，但是因为企业微信、飞书等第三方wenhook接口需要先定义消息体，
grafana不支持自定义消息体，所以无法直接使用第三方webhook接口直接发送，所以，我们要先自己编写一个webhook接口，
接收grafana发送过来的初始的json文件，经过数据的解析筛选出我们需要的数据再封装成消息体，通过第三方应用的webhook接口发送出去
步骤：
1.编写webhook接口，第三方应用请求改app地址发起post请求,改app接收json字符串


2.转换json文件，获取自己相要的数据


3.将数据通过markdown或者text的方式发送到企业微信或者飞书等第三方webhook接口中
'''


import json, requests
from flask import Flask,request
from gevent.pywsgi import WSGIServer
import datetime


#定义常量
corpid = "ww99c341775886c227"
secret = "fAELIbAOKKcEvZRTCmHH1891qd6InM3PpNMGAwrIxEY"
my_app_url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=" + corpid + "&corpsecret=" + secret
#获取access_token
get_access_token = requests.get(url=my_app_url).json()["access_token"]
#真实的消息发送api
wxmsg_url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=" + get_access_token
now_time=datetime.datetime.now().strftime('%Y年%m月%d日 %H:%M:%S %p')






# 1.编写自己的webhook接口
app = Flask(__name__)
@app.route('/webhook',methods=['POST'])
def webhook():
    grafana_msg = json.loads(request.data)
    print(json.dumps(grafana_msg, ensure_ascii=False, sort_keys=True, indent=2))
#2.从json文件中获取可用值，因为告警和恢复得到的json文件不一样，所以需要单独做判断,获取以后组合成新的消息体通过第三方wenhook发送出去
    if grafana_msg["state"] == "alerting":
        msgtype = "告警信息"
        # 告警主机
        alert_host = grafana_msg["evalMatches"][0]["tags"]["instance"].split(':')[0]
        # 当前值：
        now_status = grafana_msg["evalMatches"][0]["metric"] + "=" + str(
            float('%.2f' %grafana_msg["evalMatches"][0]["value"]))
        # 告警信息
        alert_name = grafana_msg["ruleName"]
        # 历史趋势图url:
        image_url = grafana_msg["ruleUrl"]
        #3.发送消息


        message_alert = {
            "agentid":1000023,
            "touser":'@all',
            # "msgtype":"news",
            # "news":{
            #     "articles":[{
            #         "title":"新的告警信息",
            #         "description":alert_host+alert_name,
            #         "url": "www.baidu.com",
            #         "picurl":"http://192.168.32.128:3000/d/9CWBzd1f0bik001666699889/prometheushui-zong?tab=alert&viewPanel=7&orgId=1"
            #     }]
            # }
            "msgtype": "text",
            "text": {
                "content": msgtype +"\n告警时间："+now_time +"\n告警主机：" + alert_host + "\n告警内容：" + alert_name + "\n当前状态：" + now_status
            }
        }
        print(requests.post(url=wxmsg_url,json=message_alert).json())


    else:
        msgtype = "恢复信息"
        # 告警信息
        alert_name = grafana_msg["ruleName"]
        # 历史趋势图url:
        image_url = grafana_msg["ruleUrl"]
        message_recover = {
            "agentid":1000023,
            "touser":'@all',
            # "msgtype":"news",
            # "news":{
            #     "articles":[{
            #         "title":"恢复信息",
            #         "description":alert_name+"已恢复",
            #         "url": "www.baidu.com",
            #         "picurl":"http://192.168.32.128:3000/d/9CWBzd1f0bik001666699889/prometheushui-zong?tab=alert&viewPanel=7&orgId=1"
            #     }]
            # }
           "msgtype": "text",
            "text": {
                "content": msgtype + "\n恢复时间："+now_time+"\n恢复的告警：" + alert_name
            }
        }
        print(requests.post(url=wxmsg_url,json=message_recover).json())
    return "pzl"


if __name__ == '__main__':
    WSGIServer(('0.0.0.0', 5000), app).serve_forever()