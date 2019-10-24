# ctpbee_backend
---
> 基于ctpbee界面端的后台服务
```
# 安装依赖
pip install -r requriment.txt
```
### 目录
- [功能支持](#功能支持)
- [API](#API)
  - [/login](#login)
  - [/logout](#logout)
  - [/market](#market)
  - [/order_solve](#order_solve)
  - [/auth_code](#auth_code)
  - [/strategy](#strategy)
  - [/check_code](#check_code)
  - [/run_code](#run_code)
  - [/code](#code)
  - [/close_position](#close_position)
  - [/bar](#bar)
  - [/config](#config)
- [代码概览](#代码概览)
- [快速部署](#deploy)
- [写在最后](#写在最后)



## 功能支持___[[目录]](#目录)
 - [x] 单账户
 - [x] 行情
 - [x] K线图
 - [x] 交易
 - [x] 在线添加策略
 - [ ] 回测
 ---

## API___[[目录]](#目录)
> Response格式规范:  `{'success' : True(bool), 'msg' :  msg(str), 'data' : data(Any)}`
如未明确给出，请以具体的msg，data为准

<span id="login"></span>
### /login___[[目录]](#目录)
key|value|remarks
---|---|---
method|POST
args|
-|authorization | 授权码	默认为:000000
-|userid | 用户名	
-|password | 密码
-| brokerid | 期货公司编号	
-|auth_code  |认证码	
-|appid | 产品名称	
-|interface | 接口
-|td_address | 交易前置	
-|md_address | 行情前置	
response|
success| `{"success":True,"msg":"","data":token}`
fail| `{"success":False,"msg":msg,"data":""}`
     
<span id="logout"></span>
### /logout___[[目录]](#目录)
key|value|remarks
---|---|---
method|POST
args|
-|authorization| 授权码
response|
success| `{"success":True,"msg":msg,"data":""}`
fail| `{"success":False,"msg":msg,"data":""}`

<span id="market"></span>
### /market___[[目录]](#目录)
key|value|remarks
---|---|---
method|POST
args:|
-|symbol |合约名称
response|
success| `{"success":True,"msg":"订阅××成功","data":""}`
fail| `{"success":False,"msg":"订阅××失败","data":""}`
/|/|/
method|PUT
args:|-
response|
success| `{"success":True,"msg":"更新合约列表完成","data":""}`| 最新合约列表通过socket推送 on("contract")
fail| `{"success":False,"msg":"更新合约失败","data":""}`

<span id="order_solve"></span>
### /order_solve___[[目录]](#目录)
key|value|remarks
---|---|---
method|GET
args|-
response|
success|`{"success":True,"msg":"","data":data}`|data->`{"position_list":[],"active_order_list":[],"trade_list":[],"order_list":[],"log_history":[]}`
/|/|/ 
method|POST
args|
-|local_symbol|ctpbee维护的本地合约名称
-|direction|开平
-|offset|long、short
-|type|类型
-|price|价格
-|volume|手数
-|exchange|交易所
response|
success| `{"success":True,"msg":"成功下单","data":""}`
fail| `{"success":False,"msg":msg,"data":""}`

<span id="auth_code"></span>
### /auth_code___[[目录]](#目录)
key|value|remarks
---|---|---
method|POST
args|
-|password|账户密码，仅作校验
-|authorization|授权码
response|
success| `{"success":True,"msg":"修改成功","data":""}`
fail| `{"success":False,"msg":"修改失败","data":""}`

<span id="strategy"></span>
### /strategy___[[目录]](#目录)
key|value|remarks
---|---|---
method|GET
args|-
response|
success| `{"success":True,"msg":"","data":data}`|data->`[{"name": "", "status": "停止"or"运行中"},]`
/|/|/
method|PUT
args|
-|name|策略名称
-|operation|操作：开启，关闭
response|
success| `{"success":True,"msg":msg,"data":""}`
fail| `{"success":False,"msg":msg,"data":""}`
/|/|/
method|DELETE
args|
-|name|策略名称
response|
success| `{"success":True,"msg":"删除××成功","data":""}`
fail| `{"success":False,"msg":"删除××失败","data":""}`

<span id="check_code"></span>
### /check_code___[[目录]](#目录)
key|value|remarks
---|---|---
method|POST
args|
-|text|代码
response|
success| `{"success":True,"msg":"","data":data}`

<span id="run_code"></span>
### /run_code___[[目录]](#目录)
key|value|remarks
---|---|---
method|POST
args|
-|text|代码
response|
success| `{"success":True,"msg":"","data":data}`

<span id="code"></span>
### /code___[[目录]](#目录)
key|value|remarks
---|---|---
method|GET
args|
-|name|策略名称
response|
success| `{"success":True,"msg":"","data":data}`|data->策略代码
fail|`{"success":True,"msg":msg,"data":""}`
/|/|/
method|POST
args|
-|text|策略名称
response|
success| `{"success":True,"msg":"添加成功","data":""}`|同时对策略进行ext变量检测
fail|`{"success":True,"msg":"添加失败","data":""}`

<span id="close_position"></span>
### /close_position___[[目录]](#目录)
key|value|remarks
---|---|---
method|POST
args|
-|local_symbol
-|volume
-|direction
-|exchange
-|symbol
response|
success| `{"success":True,"msg":msg,"data":""}`
fail| `{"success":False,"msg":msg,"data":""}`

<span id="bar"></span>
### /bar___[[目录]](#目录)
key|value|remarks
---|---|---
method|POST
args|
-|local_symbol
response|
success| `{"success":True,"msg":"","data":data}`|data->`[[timestamp,open_price,high_price,low_price,close_price,volume],]`
fail| `{"success":False,"msg":msg,"data":""}`|

<span id="config"></span>
### /config___[[目录]](#目录)
key|value|remarks
---|---|---
method|GET
args|-
response|
success| `{"success":True,"msg":"","data":data}`|data->`{key:value,key:value}`
/|/|/
method|PUT
args|
-|REFRESH_INTERVAL
-|INSTRUMENT_INDEPEND
-|SLIPPAGE_SHORT
-|SLIPPAGE_BUY
-|SLIPPAGE_COVER
-|SLIPPAGE_SELL
-|CLOSE_PATTERN
-|SHARED_FUNC
response|
success|`{"success":True,"修改成功":"","data":""}`

## 代码概览___[[目录]](#目录)
基于ctpbee API支持
- views
- lib
  - pylint_lib: python语法检测的错误代码库
  - stategys:用户策略库，在router中禁止访问
  - strategy_lib:用于策略的一系列CRUD
- model
  - mongodb
- auth 
  - 基于JWT Token认证
  - 在请求header中携带 `JWT(我是一个空格)token`
- default_settings
  - 继承CtpbeeApi 用于数据接口以及数据推送
- global_var
  - 由于配置以及一些参数处理的需要，基于`Flask.config`加了一层封装:` G`
- ext
  - 基于`flask-socketio `数据推送服务
    - 连接验证 ->header中携带"token"用于激活数据推送(使用room区别连接,划分推送区域)

---

<span id="deploy"></span>
## ~~快速部署~~ (现仅支持单账户)python run.py 即可___[[目录]](#目录)

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


## 写在最后

由于ctpbee是轻量化框架,所以各位大佬如果看过ctpbee文档教程,,此backend只暴露接口,一些逻辑代码也加有注释,
欢迎提出疑问或有更好的改进.毕竟本人一直在写Bug.🙈
> [回到顶部](#ctpbee_backend)