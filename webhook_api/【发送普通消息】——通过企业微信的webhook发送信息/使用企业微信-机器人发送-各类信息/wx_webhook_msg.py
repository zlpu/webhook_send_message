# -*- coding:utf-8 -*-
# 如何使用群机器人,在群里定期自动发送相关的消息或者文件
"""1.说明：
在终端某个群组添加机器人之后，创建者可以在机器人详情页看的该机器人特有的webhookurl。开发者可以按以下说明a向这个地址发起HTTP POST 请求，即可实现给该群组发送消息。下面举个简单的例子.
假设webhook是：https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=693a91f6-7xxx-4bc4-97a0-0ec2sifa5aaa
特别特别要注意：一定要保护好机器人的webhook地址，避免泄漏！不要分享到github、博客等可被公开查阅的地方，否则坏人就可以用你的机器人来发垃圾消息了。
以下是用curl工具往群组推送文本消息的示例（注意要将url替换成你的机器人webhook地址，content必须是utf8编码）：


curl 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=693axxx6-7aoc-4bc4-97a0-0ec2sifa5aaa' \
   -H 'Content-Type: application/json' \
   -d '
   {
        "msgtype": "text",
        "text": {
            "content": "hello world"
        }
   }'
当前自定义机器人支持文本（text）、markdown（markdown）、图片（image）、图文（news）四种消息类型+组合型的卡片类型（template_card）中的text_notice和news_notice。
机器人的text/markdown类型消息支持在content中使用<@userid>扩展语法来@群成员
“”“
”“”2.使用方法：
使用python编写的框架结构如下：（具体细节请参考官方文档，官方文档可能会做更改）
import requests
mywx_url="你的机器人webhook地址"
headers = {"Content-Type": "application/json", "charset": "utf-8"}固定
data={
    "此处为消息内容，后期所有改动都在这里，根据不同的消息类型参考API文档进行编写消息"
}
respond=requests.post(url=mywx_url,headers=headers,json=data)调用api，使用requests的post方式发起请求
print(respond)
"""
# 具体的使用案例：
import json
import requests
import datetime


my_wx_url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=167c4082-8510-4539-87a0-69aecb94f320"
headers = {"Content-Type": "application/json", "charset": "utf-8"}
def post_send(data):
    respond = requests.post(url=my_wx_url,  json=data)
    if respond.text.find("errmsg") == 14:
        print("消息发送成功！")
    else:
        print(respond.text)




"""
1.发送简单text
-d '
   {
        "msgtype": "text",
        "text": {
            "content": "hello world"  #消息内容
        }
   }'
"""
data1 = {
    "msgtype": "text",
    "text":
        {
            "content": "北京时间：" + str(datetime.datetime.now().strftime('%Y年%m月%d日 %H:%M:%S %p'))


        }
}


"""
2.发送text消息并且@相关得用户
{
    "msgtype": "text",
    "text": {
        "content": "昆明今日天气：29度，大部分多云，降雨概率：60%",#消息内容
        "mentioned_list":["wangqing","@all"],#消息提醒用户，用户ID匹配用户
        "mentioned_mobile_list":["13800001111","@all"]#消息提醒用户，手机号匹配用户
    }
}
"""
data2 = {
    "msgtype": "text",
    "text": {
        "content": "昆明今日天气：26度，降雨概率：1%",
        "mentioned_list": ["@all"],
        "mentioned_mobile_list": ["18827340310"]
    }
}


"""
3.发送markdown类型得消息
{
    "msgtype": "markdown",
    "markdown": {
        "content": "实时新增用户反馈<font color=\"warning\">132例</font>，请相关同事注意。\n
         >类型:<font color=\"comment\">用户反馈</font>
         >普通用户反馈:<font color=\"comment\">117例</font>
         >VIP用户反馈:<font color=\"comment\">15例</font>"              #markdown格式消息内容
    }
}
"""
data3 = {
    "msgtype": "markdown",
    "markdown": {
        "content":


            str(datetime.datetime.now().strftime('%Y年%m月%d日 %H:%M:%S %p')) + "\n"
                                                                             "# 1.标题\n"
                                                                             "**2.加粗**\n"
                                                                             "[3.超链接文字](https://work.weixin.qq.com/api/doc/90000/90136/91770)\n"
                                                                             "`4.print('代码段')`\n"
                                                                             ">5.引用\n"
                                                                             "<font color='info'>6.字体颜色-绿色</font>\n"
                                                                             "<font color='commit'>灰色</font>\n"
                                                                             "<font color='warning'>橙红色</font>\n"
                                                                             "@all",


    }
}


"""
4.image图片类型#需要用工具获取图片得值
{
    "msgtype": "image",
    "image": {
        "base64": "DATA",#图片得base64编码
        "md5": "MD5"     #图片base64编码前得md5值
    }
}
"""
data4 = {
    "msgtype": "image",
    "image": {
        "base64": "******",
        "md5": "177550b13ade24d8879597a7f524973f"
    }
}
"""
5.new类消息-图文-----articles为list类
{
    "msgtype": "news",                                                  #必须写
    "news": {
       "articles" : [                                                   #必须写
           {
               "title" : "中秋节礼品领取", #必须写                        #必须写
               "description" : "今年中秋节公司有豪礼相送",                #可选
               "url" : "www.qq.com",                                 #必须写
               "picurl" : "http://res.mail.qq.com/node/ww/wwopenmng/images/independent/doc/test_pic_msg1.png" #可选
           }
        ]
    }
}
"""
data5 = {
    "msgtype": "news",
    "news": {
        "articles": [
            {
                "title": "图文类1",
                "description": "描述",
                "url": "https://work.weixin.qq.com/api/doc/90000/90136/91770",
                "picurl": "https://wework.qpic.cn/wwpic/473864_mAbME3l6RcOPd50_1629279699/0"
            },
            {"title": "图文类2",
             "description": "描述",
             "url": "https://work.weixin.qq.com/api/doc/90000/90136/91770",
             "picurl": "https://wework.qpic.cn/wwpic/473864_mAbME3l6RcOPd50_1629279699/0"
             },
            {"title": "图文类3",
             "description": "描述",
             "url": "https://work.weixin.qq.com/api/doc/90000/90136/91770",
             "picurl": "https://wework.qpic.cn/wwpic/473864_mAbME3l6RcOPd50_1629279699/0"
             }
        ]


    }
}
"""
6.发送文件,要使用media_id  所以先要用文件上传接口获取文件的media_id值
文件上传接口使用：
wx_file_url="https://qyapi.weixin.qq.com/cgi-bin/webhook/upload_media?key=167c4082-8510-4539-87a0-69aecb94f320&type=file"
file={
    "file":{"rE:\运维学习PPT编写\Docker.pptx","rb"}
}
media_id=requests.post(url=my_file_url,files=file).json["media_id"]
发送文件接口传参如下：
{
    "msgtype": "file",
    "file": {
         "media_id": media_id#从上面的接口获取的media_id
    }
}
"""
my_wx_url_file="https://qyapi.weixin.qq.com/cgi-bin/webhook/upload_media?key=167c4082-8510-4539-87a0-69aecb94f320&type=file"
file={
    "file":open("E:\运维学习PPT编写\Docker.pptx","rb")


}
media_id=requests.post(url=my_wx_url_file,files=file).json()["media_id"]
data6 = {
    "msgtype": "file",
    "file": {
        "media_id": media_id
    }
}
"""
7.卡片模板----text_notice---不支持card_image 支持关键数字
data={
    "msgtype":"template_card",
    "template_card":{
        "card_type":"text_notice",
        "source":{
            "icon_url":"https://wework.qpic.cn/wwpic/252813_jOfDHtcISzuodLa_1629280209/0",
            "desc":"企业微信"
        },
        "main_title":{
            "title":"欢迎使用企业微信",
            "desc":"您的好友正在邀请您加入企业微信"
        },
        "emphasis_content":{
            "title":"100",
            "desc":"数据含义"
        },
        "sub_title_text":"下载企业微信还能抢红包！",
        "horizontal_content_list":[
            {
                "keyname":"邀请人",
                "value":"张三"
            },
            {
                "keyname":"企微官网",
                "value":"点击访问",
                "type":1,
                "url":"https://work.weixin.qq.com/?from=openApi"
            },
            {
                "keyname":"企微下载",
                "value":"企业微信.apk",
                "type":2,
                "media_id":"MEDIAID"
            }
        ],
        "jump_list":[
            {
                "type":1,
                "url":"https://work.weixin.qq.com/?from=openApi",
                "title":"企业微信官网"
            },
            {
                "type":2,
                "appid":"APPID",
                "pagepath":"PAGEPATH",
                "title":"跳转小程序"
            }
        ],
        "card_action":{
            "type":1,
            "url":"https://work.weixin.qq.com/?from=openApi",
            "appid":"APPID",
            "pagepath":"PAGEPATH"
        }
    }
}
"""
spring = datetime.datetime(2022, 1, 31)
today = datetime.datetime.now()
to_date = (spring - today)
data7 = {
    "msgtype": "template_card",
    "template_card": {
        "card_type": "text_notice",
        # "source": {
        #     "icon_url": "https://img1.baidu.com/it/u=3471583940,297920709&fm=26&fmt=auto",
        #     "desc": "勇士在客场104-89击败骑士，全场比赛勇士后卫斯蒂芬-库里再次发挥出色，全场\n首发出战35分钟的他27投15中，三分球16投9中，罚球1罚1中得到40分4篮板6助攻2抢断。\n本场取胜后，库里自从当地时间2021年1月1日至今已经投进了408记三分球。NBA历史上，在单个自然年度内投进400+三分球共出现过4次，其中库里独占3次。2016年，库里投进了468记三分球；2019年詹姆斯-哈登命中445记三分球；而2015年库里命中过436记三分球。",


        # },
        "main_title": {
            "title": "2021倒计时",
            "desc": "2021年倒计时已开始"
        },


        "emphasis_content": {
            "title": str(to_date.days) + "天" + str(to_date.seconds) + "秒"
            # "desc":"最喜欢的数字"
        },
        "sub_title_text": "每日一读",
        "horizontal_content_list": [
            {
                "type": 1,
                "keyname": "全国热点新闻",
                "value": "阅读新闻",
                "url": "http://www.gov.cn/xinwen/yaowen.htm"
            },
            {
                "type": 1,
                "keyname": "云南热点新闻",
                "value": "阅读新闻",
                "url": "http://www.yn.gov.cn/ywdt/ynyw/"
            }
        ],
        "jump_list": [
            {
                "type": 1,
                "title": "疫情防控",
                "url": "https://user.guancha.cn/app/pneumonia"
                # "appid":"小程序id",


            }
        ],
        "card_action": {
            "type": 1,
            "url": "http://finance.yunnan.cn/video/003/009/022/00300902233_vw00000000000001_32bffe39.mp4",
        }


    }


}
"""
8.卡片模板-new_notice支持crad_image 不支持数字
{
    "msgtype":"template_card",
    "template_card":{
        "card_type":"news_notice",
        "source":{
            "icon_url":"https://wework.qpic.cn/wwpic/252813_jOfDHtcISzuodLa_1629280209/0",
            "desc":"企业微信"
        },
        "main_title":{
            "title":"欢迎使用企业微信",
            "desc":"您的好友正在邀请您加入企业微信"
        },
        "card_image":{
            "url":"https://wework.qpic.cn/wwpic/354393_4zpkKXd7SrGMvfg_1629280616/0",
            "aspect_ratio":2.25
        },
        "vertical_content_list":[
            {
                "title":"惊喜红包等你来拿",
                "desc":"下载企业微信还能抢红包！"
            }
        ],
        "horizontal_content_list":[
            {
                "keyname":"邀请人",
                "value":"张三"
            },
            {
                "keyname":"企微官网",
                "value":"点击访问",
                "type":1,
                "url":"https://work.weixin.qq.com/?from=openApi"
            },
            {
                "keyname":"企微下载",
                "value":"企业微信.apk",
                "type":2,
                "media_id":"MEDIAID"
            }
        ],
        "jump_list":[
            {
                "type":1,
                "url":"https://work.weixin.qq.com/?from=openApi",
                "title":"企业微信官网"
            },
            {
                "type":2,
                "appid":"APPID",
                "pagepath":"PAGEPATH",
                "title":"跳转小程序"
            }
        ],
        "card_action":{
            "type":1,
            "url":"https://work.weixin.qq.com/?from=openApi",
            "appid":"APPID",
            "pagepath":"PAGEPATH"
        }
    }
}
"""
data8 = {
    "msgtype": "template_card",
    "template_card": {
        "card_type": "news_notice",
        "main_title": {
            "title": "NBA勇士新闻汇",
            "desc": "一起关注NBA热点新闻"
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
        "card_action": {
            "type": 1,
            "url": "https://www.bilibili.com/video/BV1644115717?t=3.9",
        }


    }


}
if __name__ == '__main__':
    post_send(data6)  # 可选data1-8   (4是图,不能直接使用)