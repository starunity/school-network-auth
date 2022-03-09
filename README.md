# 重庆电子工程职业学院校园网认证脚本

## 安装
```shell
git clone https://github.com/starunity/school-network-auth.git
cd school-network-auth
pip3 install -r requirements.txt
```

## 认证脚本使用

```shell
python3 auth.py <需要认证的IP地址> <学号>
1. xyw (Teacher only)       # 教师专用
2. telecom                  # 中国电信
3. cmcc                     # 中国移动
4. unicom                   # 中国联通
5. edu                      # 教育网
Please select an ISP [1-5]: <选择运营商>
Password: <输入密码没有回显>
```

## 断线重连脚本使用

运行脚本后主机，会每隔一段时间(默认60秒)检测网络连接状态，检测到掉线会自动重连网络

```shell
python3 reconnection.py <学号> <密码> <运营商英文名> [检测时间(秒)]
```

