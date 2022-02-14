# -*- coding:utf-8 -*-
# 如何使用群机器人,在群里定期自动发送相关的消息
"""
自定义机器人添加完成后，就能向其 webhook 地址发送 POST 请求，
从而在群聊中推送消息了。
支持推送的消息格式有文本、富文本、图片消息和群名片等。
"""
# 你添加的机器人的webhook地址
import requests
import json
import datetime

my_feishu_rul = "https://open.feishu.cn/open-apis/bot/v2/hook/ebfda356-cc93-4628-ae86-2442008ee3ec";
# 定义header
headers = {"Content-Type": "application/json"}
# 定义消息体
'''
1.普通文本类型
'''
data_text = {
    "msg_type": "text",
    "content": {
        "text": "飞书通过机器人的webhook接口发送普通文本" +
                str(datetime.datetime.now().strftime("%Y年%m月%d日 %H时:%M分:%S秒"))
    }
}
'''
2.富文本类型
'''
data_markdown = {
        "msg_type": "post",
        "content": {
            "post": {
                "zh-CN": {
                    "title": 'from_zabbix_subject',
                    "content": [
                        [{
                            "tag": "a",
                            "href": "192.168.32.136:3000",
                            "text": 'from_zabbix_message'
                        },
                        ]
                    ]
                }
            }
        }
    }


# 发起post请求
def post_send(data_msg):
    respond = requests.post(url=my_feishu_rul, headers=headers, data=json.dumps(data_msg))
    print(respond.json())


if __name__ == '__main__':
    post_send(data_markdown)  # 可选data1-8   (4是图,不能直接使用)
