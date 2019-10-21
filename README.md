# ctpbee_client
  
---
> 基于ctpbee界面端的后台服务
```
# 安装依赖
pip install -r requriment.txt
```

## ~~快速部署~~ (现仅支持单账户)python run.py 即可

--- 
根据实际部署情况修改 uwsig.ini
```
# supervisor
sudo apt install supervisor
cd /etc/supervisor/conf.d/ && sudo vim supervisor.conf
```
supervisor.conf
```
[program:ctpbee_client]
# 启动命令入口
command=/home/faith/GIT/ctpbee_client/venv/bin/uwsgi /home/faith/GIT/ctpbee_client/backend/uwsgi.ini

# 命令程序所在目录
directory=/home/faith/GIT/ctpbee_client/backend/
#运行命令的用户名
user=faith
        
autostart=true
autorestart=true
#日志地址
stdout_logfile=/home/faith/GIT/ctpbee_client/backend/uwsgi_supervisor.log    
```
```
# nginx
sudo apt install nginx
cd /etc/nginx && sudo vim nginx.conf
```
根据实际部署情况修改 nginx.conf
```
## nginx.conf
http
{   ##
	# Basic Settings
	##
# 写入
server {
  listen  80;
  server_name 10.40.25.15; #公网地址

  location / {
    include      uwsgi_params;
    uwsgi_pass   127.0.0.1:8001;  # 指向uwsgi 所应用的内部地址,所有请求将转发给uwsgi 处理
    uwsgi_param UWSGI_PYHOME /home/faith/GIT/ctpbee_client/venv; # 指向虚拟环境目录
    uwsgi_param UWSGI_CHDIR  /home/faith/GIT/ctpbee_client/backend; # 指向网站根目录
    uwsgi_param UWSGI_SCRIPT run:app; # 指定启动程序
  }
}
## 写入
}
```
启动
```
sudo service supervisor start
sudo service nginx restart
```
如果表达的不清楚->[传送门](https://www.cnblogs.com/Ray-liang/p/4173923.html)

---

## 功能支持

 - [x] 单账户
 - [x] 行情
 - [x] K线图
 - [x] 交易
 - [x] 在线添加策略
 - [ ] 回测
 ---
 
## 代码部分     
基于ctpbee API支持
- 视图部分 views
  - bar：K线api
  - login：账户登录api
  - config：配置api
  - market：行情api 
    - 订阅
  - order：交易api
    - 下单
    - 撤单
  - position：持仓api
    - 平仓
  - strategy：策略api
    - 管理策略
    - 添加
    - 删除
    - 更新
> Response规范格式
> {'success': True(bool), 'msg': msg(str), 'data': data(Any)}
        
Api|Methods|Args|Response/Success|Response/Fail
:---|:---|:---|:---|:---
login|post|*login_args|msg=''|msg=''
bar |post|local_symbol(str)| data=bars(list)|msg=''
config|get,post|post->[*config_args]|msg=''|msg=''
market|post,put|post->[symbol]|msg=''|msg=''
order|get,post,delete|post->[local_symbol,direction,offset,type,price,volume,exchange],delete->[local_symbol,order_id,exchange]|msg=''|msg=''
position|post|local_symbol,volume,direction,exchange,symbol|msg=''|msg=''
strategy|get,put,delete|put->[name,operation],delete->[name]|msg=''|msg=''
strategy_code|get,post|get->[name],post->[text]|get->data=text,post->msg=''|msg=''


- 认证机制
  - 基于JWT Token认证
  - 基于flask-socketio 数据推送服务
    - 连接验证 ->Token,使用room区别连接,划分推送区域
- global_var.py
  - 由于配置以及一些参数处理的需要,基于Flask.config加了一层封装
    - G
---

## 凑凑字数

由于ctpbee是轻量化框架,所以各位大佬如果看过ctpbee文档教程,对client的Views部分应该不陌生,此client只暴露接口,一些逻辑代码也加有注释,
欢迎提出疑问或有更好的改进.毕竟本人一直在写Bug.🙈
