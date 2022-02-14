# -*- coding:utf-8 -*-
"""
文件上传接口
素材上传得到media_id，该media_id仅三天内有效
media_id只能是对应上传文件的机器人可以使用
请求方式：POST（HTTPS）
请求地址：https://qyapi.weixin.qq.com/cgi-bin/webhook/upload_media?key=KEY&type=TYPE
使用multipart/form-data POST上传文件， 文件标识名为”media”
"""
"""
参数说明：
1.(必须)key=你的webhook地址  唯一
2.(必须)type=file 固定
"""
import requests
mywx_url_file="https://qyapi.weixin.qq.com/cgi-bin/webhook/upload_media?key=167c4082-8510-4539-87a0-69aecb94f320&type=file" #机器人webhook文件上传接口
headers={
    "Content-Type: multipart/form-data",#headers貌似不影响可有可无
    "Content-Length: 220"
}
file={
    "file":open(r'C:\Users\pzl96\Pictures\smm-01.jpg','rb')#指定本地的文件
}
repond1=requests.post(url=mywx_url_file,files=file) #上传本地文件，获取文件的一串json字符串
json_res1=repond1.json()
media_id=json_res1['media_id']#解析json格式  获取其中的media_id值作为发送消息时的file media_id
my_wx_url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=167c4082-8510-4539-87a0-69aecb94f320"#机器人发消息的接口
data={
    "msgtype":"file",
    "file":{
        "media_id":media_id   #通过上传文件接口获取的media_id
    }
}
repond2=requests.post(url=my_wx_url,json=data)#post请求  机器人将文件发送到群里
print(repond2.json())