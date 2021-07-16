# 重庆电子工程职业学院校园网认证脚本

## 安装
```shell
git clone https://github.com/starunity/school-network-auth.git
cd school-network-auth
pip3 install -r requirements.txt
```

## 认证脚本使用

```shell
python3 auth.py <需要认证的IP地址> <学号> <密码>
```

## 断线重连脚本使用

运行脚本后主机，会每隔一段时间(默认60秒)检测网络连接状态，检测到掉线会自动重连网络

```shell
python3 reconnection.py <学号> <密码> [检测时间(秒)]
```

