# -*- coding:utf-8 -*-
# 作业效果：可以在微信端跳出领取奖品的信息，然后跳转到搞笑图片或者视频！
import requests
import datetime


corpid = "ww99c341775886c227"
secret = "fAELIbAOKKcEvZRTCmHH1891qd6InM3PpNMGAwrIxEY"
my_app_url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=" + corpid + "&corpsecret=" + secret
get_token = requests.get(url=my_app_url).json()["access_token"]
print(get_token)
wxsend_url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=" + get_token
date_text_card = {
    "touser": "@all",
    "agentid": 1000023,
    "msgtype": "textcard",
    "textcard": {
        "title": "你有新的红包待领取!",
        "description":
            "<div class=\"gray\">" + datetime.datetime.now().strftime(
                '%Y年%m月%d日 %H:%M:%S %p') + "</div> <div class=\"normal\">\n\n请尽快领取,有限期为2天。</div><div class=\"highlight\">请于" + (
                        datetime.datetime.now() + datetime.timedelta(days=2)).strftime('%Y年%m月%d日') + "前领取</div>",
        "url": "https://gimg2.baidu.com/image_search/src=http%3A%2F%2Fwww.keaidian.com%2Fuploads%2Fallimg%2F190429%2F29094302_97.gif&refer=http%3A%2F%2Fwww.keaidian.com&app=2002&size=f9999,10000&q=a80&n=0&g=0n&fmt=jpeg?sec=1640170121&t=1dd49f50c5c418ae96652be9011cf2dc",
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
                "title" : "@你\n您有新消息待查看!",
               "description" : "时间："+(datetime.datetime.now() ).strftime('%Y年%m月%d日'),
               "url" : "192.168.1.7",
               "picurl":"https://gimg2.baidu.com/image_search/src=http%3A%2F%2Fb-ssl.duitang.com%2Fuploads%2Fitem%2F201610%2F09%2F20161009145526_SkzwT.thumb.700_0.png&refer=http%3A%2F%2Fb-ssl.duitang.com&app=2002&size=f9999,10000&q=a80&n=0&g=0n&fmt=jpeg?sec=1646899880&t=e97e8275144d176804240380ca936028"
            }
        ]
    }
}
print(requests.post(url=wxsend_url, json=data_news).json())