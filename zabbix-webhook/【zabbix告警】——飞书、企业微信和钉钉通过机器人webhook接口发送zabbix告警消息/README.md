<h2 align = "center">通过企业微信、飞书和飞书的webhook机器人发送zabbix告警消息到群聊中</h3>
脚本用途：(**发送zabbix告警消息到群聊中**)

1.需要更改3个地方：
>
><font color="green">01.(需要则修改为自己的url,不需要则注释)</font>
> 
><font color="green">url_my_feishu =" " </font>
>
><font color="green">url_my_wx="" =" " </font>
>
> <font color="green">url_my_dingding="" =" " </font>
> 
><font color="green">02.消息体中的超链接地址 ="" </font>
> 
><font color="green">03.钉钉消息体中的@对象 ="" </font>


2.适用于企业微信、钉钉和飞书的群聊机器人webhook,不是自建应用的webhook。

3.消息类型：

富文本类
飞书和企业微信的机器人webhook-markdown消息类型不支持@用户

4.python 使用的requests模块，如果未安装请先pip install requests

------
<font color="red" size="5">zabbix告警的配置步骤</font>

1.将这个脚本到到zabbix-server的的脚本存放目录中，并修改权限
>
>可以通过：
>
>cat /etc/zabbix/zabbix_server.conf |grep alertscripts
>
>这条命令确定所在的路径
>
>上传到该路径下，给777的权限
>
>chmod 777 zabbix_feishu+wx_bot_webhook.py
![image](https://user-images.githubusercontent.com/46338963/153586352-0586a51a-a432-44eb-b034-0941afc56741.png)


2.在zabbix web界面上操作

2.1 添加告警媒介，定义改告警方式的告警内容模板（告警模板在msg_tmp.txt中）
![image](https://user-images.githubusercontent.com/46338963/153586382-b1eb3df4-d7d1-4ab5-ac05-265673f38eec.png)
![image](https://user-images.githubusercontent.com/46338963/153586404-86ffaded-7670-4de8-a4ef-9460272f664d.png)

2.2 给用户绑定这个告警方式
![image](https://user-images.githubusercontent.com/46338963/153586615-8baf6392-8232-493d-8b57-a3b0946d7406.png)

2.3 创建动作（远程命令自己研究，这里不写）
![image](https://user-images.githubusercontent.com/46338963/153586595-343b2e2f-fc4d-425d-9ed7-a42dfe254511.png)

2.4 测试效果

![image](https://user-images.githubusercontent.com/46338963/153586642-57367e89-65a2-4586-9a6c-5008fdb9809b.png)
![image](https://user-images.githubusercontent.com/46338963/153587162-bec0d4b6-6fe1-4266-b041-26cfb9190100.png)


