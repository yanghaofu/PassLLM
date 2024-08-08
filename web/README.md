## 概述
app.py:和微调大模型连接的
LLM.py:和KIMI连接

## app.py使用办法
1. 在本机Powershell输入：
~~~ bash
ssh -CNg -L 6006:127.0.0.1:6006 root@connect.yza1.seetacloud.com -p 52671
~~~
2. 输入密码：
~~~bash
cyS9MhAYwFFL
~~~
3. 运行app.py即可与大模型交互。