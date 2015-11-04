# check-code
采用python语言，利用PIL包实现的图片验证码。
客户端发起请求，服务器生成一个包含字符串的图片和相应字符串，将图片返回客户端，字符串则在服务器端用于合法性检测。

#文档说明
server.py   服务端程序，采用tornado实现，接受http请求
check_code.py   验证码模块，采用PIL动态在服务器端生成图片验证
templates/index.html   用户发起请求的主界面，可以不断点击验证码从服务器获取新的验证码
