# -*- coding:utf-8 -*-
"""
我的自建应用：
Secret:fAELIbAOKKcEvZRTCmHH1891qd6InM3PpNMGAwrIxEY
corpid:ww99c341775886c227
AgentId:1000023
"""
'''
1.获取access_token
access_token的有效期通过返回的expires_in来传达，正常情况下为7200秒（2小时），有效期内重复获取返回相同结果，过期后获取会返回新的access_token。
参考开始开发，access_token是应用调用api的凭证，由 corpid和corpsecret换取。
请求方式：GET（HTTPS）
请求URL：https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=ID&corpsecret=SECRET
'''
import requests
import datetime


corpid = "ww99c341775886c227"
secret = "fAELIbAOKKcEvZRTCmHH1891qd6InM3PpNMGAwrIxEY"
my_app_url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=" + corpid + "&corpsecret=" + secret
# 第一步.获取access_token
get_access_token = requests.get(url=my_app_url).json()["access_token"]
print(get_access_token)


'''
第二步：发送消息
应用支持推送文本、图片、视频、文件、图文等类型。
请求方式：POST（HTTPS）
请求地址： https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=ACCESS_TOKEN
参数说明：access_token
各个消息类型的具体POST格式请阅后续“消息类型”部分。
1.如果有在管理端对应用设置“在微工作台中始终进入主页”，应用在微信端只能接收到文本消息，并且文本消息的长度限制为20字节，超过20字节会被截断。同时其他消息类型也会转换为文本消息，提示用户到企业微信查看。
2.支持id转译，将userid/部门id转成对应的用户名/部门名，目前仅文本/文本卡片/图文/图文（mpnews）/任务卡片/小程序通知/模版消息/模板卡片消息这八种消息类型的部分字段支持。仅第三方应用需要用到，企业自建应用可以忽略。具体支持的范围和语法，请查看附录id转译说明。
3.支持重复消息检查，当指定 "enable_duplicate_check": 1开启: 表示在一定时间间隔内，同样内容（请求json）的消息，不会重复收到；时间间隔可通过duplicate_check_interval指定，默认1800秒。
4.从2021年2月4日开始，企业关联添加的「小程序」应用，也可以发送文本、图片、视频、文件、图文等各种类型的消息了。
5.调用建议：大部分企业应用在每小时的0分或30分触发推送消息，容易造成资源挤占，从而投递不够及时，建议尽量避开这两个时间点进行调用。
发送请求示例：


返回示例：
{
   "errcode" : 0,
   "errmsg" : "ok",
   "invaliduser" : "userid1|userid2",
   "invalidparty" : "partyid1|partyid2",
   "invalidtag": "tagid1|tagid2",
   "msgid": "xxxx",
   "response_code": "xyzxyz"
}
如果部分接收人无权限或不存在，发送仍然执行，但会返回无效的部分（即invaliduser或invalidparty或invalidtag），常见的原因是接收人不在应用的可见范围内。
如果全部接收人无权限或不存在，则本次调用返回失败，errcode为81013。
返回包中的userid，不区分大小写，统一转为小写
'''
# 1.简单文本的消息可以在微信上直接查看
date_now = datetime.datetime.now().strftime('%Y年%m月%d日 %H:%M:%S %p')
data_text = {
    "touser": "@all",
    "msgtype": "text",
    "agentid": 1000023,
    "text": {
        "content": date_now
    }
}
# 2.卡片类型的消息无法直接在微信上查看
data_temp_card = {
    "touser": "pzl",
    "agentid": 1000023,
    "msgtype": "template_card",
    "template_card": {
        "card_type": "news_notice",
        "main_title": {
            "title": "准点NBA-新闻推送",
            "desc": "每天准时推送最新勇士队新闻"
        },
        "card_image": {
            "url": "https://gimg2.baidu.com/image_search/src=http%3A%2F%2Finews.gtimg.com%2Fnewsapp_match%2F0%2F11566271830%2F0.jpg&refer=http%3A%2F%2Finews.gtimg.com&app=2002&size=f9999,10000&q=a80&n=0&g=0n&fmt=jpeg?sec=1639889007&t=ff5f487bbde84d90d36764cca8871340",
            "aspect_ratio": 2.25
        },


        "horizontal_content_list": [
            {
                "type": 1,
                "keyname": "今日比赛回顾",
                "value": "点击观看比赛回放",
                "url": "https://v.qq.com/x/cover/mzc00200qhithzs/h0041cgb9f9.html"
            },
            {
                "type": 1,
                "keyname": "更多NBA赛事",
                "value": "点击观看直播",
                "url": "30.tv"
            }
        ],
        "jump_list": [
            {
                "type": 1,
                "title": "IT资讯",
                "url": "http://www.cnit5.com/"
                # "appid":"小程序id",


            }],
        "card_action": {
            "type": 1,
            "url": "https://www.bilibili.com/video/BV1644115717?t=3.9",
        }


    }


}
# 3.文件类型
# 先通过文件上传接口获取media_id




data_file = {
    "touser": "@all",
    "msgtype": "file",
    "agentid": 1000023,
    "file": {
        "media_id": "1Yv-zXfHjSjU-7LH-GwtYqDGS-zz6w22KmWAT5COgP7o"
        # 可以调用上传临时素材接口获取 media_id
    }
}


data_text_card = {
    "touser": "@all",
    "agentid": 1000023,
    "msgtype": "textcard",
    "textcard": {
        "title": "你有新的红包，请尽快领取！",
        "description": "<a href=\"http://www.w3school.com.cn\">W3School</a>",
        "url": "www.baidu.com",
        "btntxt": "详情"
    }
}
data_news = {
    "touser": "@all",
    "agentid": 1000023,
    "msgtype": "news",
    "news": {
        "articles": [
            {
                "title": "中秋节礼品领取",
                "description": "今年中秋节公司有豪礼相送",
                "url": "www.baidu.com",
                "picurl": "http://res.mail.qq.com/node/ww/wwopenmng/images/independent/doc/test_pic_msg1.png",


            }
        ]
    }
}
data_temp = {
    "touser": "@all",
    "agentid": 1000023,
    "msgtype": "template_card",
    "template_card": {
        "card_type": "news_notice",
        "main_title": {
            "title": "准点NBA-新闻推送",
            "desc": "每天准时推送最新勇士队新闻"
        },
        "card_image": {
            "url": "https://gimg2.baidu.com/image_search/src=http%3A%2F%2Finews.gtimg.com%2Fnewsapp_match%2F0%2F11566271830%2F0.jpg&refer=http%3A%2F%2Finews.gtimg.com&app=2002&size=f9999,10000&q=a80&n=0&g=0n&fmt=jpeg?sec=1639889007&t=ff5f487bbde84d90d36764cca8871340",
            "aspect_ratio": 2.25
        },


        "horizontal_content_list": [
            {
                "type": 1,
                "keyname": "今日比赛回顾",
                "value": "点击观看比赛回放",
                "url": "https://v.qq.com/x/cover/mzc00200qhithzs/h0041cgb9f9.html"
            },
            {
                "type": 1,
                "keyname": "更多NBA赛事",
                "value": "点击观看直播",
                "url": "30.tv"
            }
        ],
        "jump_list": [
            {
                "type": 1,
                "title": "IT资讯",
                "url": "http://www.cnit5.com/"
                # "appid":"小程序id",


            }],
        "card_action": {
            "type": 1,
            "url": "https://www.bilibili.com/video/BV1644115717?t=3.9",
        }


    }


}
data_markdown = {
    "touser": "@all",
    "agentid": 1000023,
    "msgtype": "markdown",
    "markdown": {
         "content":
             "您的会议室已经预定，稍后会同步到`邮箱`\n"
                    ">**事项详情 **\n"
                    "> 事　项： < font color =\"info\">开会</font>\n"
                    "> 组织者：@miglioguan\n"
                    "> 参与者：@miglioguan\n"
                    "> 会议室： < font color =\"info\">广州TIT 1楼 301</font>\n"
                    "> 日　期： < font color =\"warning\">2018年5月18日</font>\n"
                    "> 时　间： < font color =\"comment\">上午9:00-11:00</font>\n"
                    "> 请准时参加会议。\n"
                    "> 如需修改会议信息，请点击：[修改会议信息](https://work.weixin.qq.com)"
},
}


wxmsg_url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=" + get_access_token
respond = requests.post(url=wxmsg_url, json=data_text_card)
print(respond.json())