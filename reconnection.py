#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import sys
import auth
import time
import socket
import requests

SCHOOL_SERV = '172.16.255.11'


def get_host_ip():
    """查询本机ip地址
    Returns:
        ip: 本机在校园网内网IP
    """
    ip = ''

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((SCHOOL_SERV, 80))
        ip = s.getsockname()[0]
    except OSError as e:
        print('ERRO: ' + str(e)[12:])
    finally:
        s.close()

    return ip


def is_ip(s):
    """判断传入字符串是否为IP地址

    Args:
        s: 需要进行判断的字符串

    Returns:
        True: 是一个正确的IP地址
        False: 不是一个正确的IP地址
    """
    p = re.compile(
        r'^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')
    if p.match(s):
        return True
    else:
        return False


def online_test():
    """检测主机是否连接互联网

    通过访问dhcp.cn获取主机公网IP地址，
    识别网站返回是否为IP地址，
    判断是否接入互联网

    Returns:
        True: 已经接入互联网
        False: 未接入互联网
    """
    try:
        r = requests.get('http://dhcp.cn', allow_redirects=False)
        return is_ip(r.text)
    except (requests.exceptions.ConnectionError, requests.exceptions.SSLError):
        return False


def reconnect(usercode, password, sleep_seconds=60):
    """断线自动重连

    传入主机学号、密码，脚本会一直检测网络连接
    当网络连接中断时，重新登录校园网


    Args:
        usercode: 学号
        password: 密码
        sleep_seconds: 每一次检查网络连接延迟的时间
    """

    ip = get_host_ip()

    # 发生错误通过errors_count记录错误次数
    errors_count = 0

    while errors_count <= 2:
        time.sleep(sleep_seconds)

        if not ip:
            ip = get_host_ip()
            errors_count += 1
            continue

        if online_test():
            continue

        # 检测到网络连接断开
        print('Warn: Network disconnection detected')

        if not auth.get_auth_status(ip):
            login_result = auth.auth(ip, usercode, password)
            if auth.SUCCESS == login_result:
                # 已重新登录网络
                print('Info: Have relogined to the network')
            else:
                if auth.ID_FAILED == login_result:
                    # 学号认证失败
                    print('ERRO: Student ID verification failed')
                elif auth.AUTH_FAILED == login_result:
                    # 学号或密码错误
                    print('ERRO: Incorrect student ID or password')
                else:
                    # 未知错误
                    print('ERRO: Unknown mistake')
                errors_count += 1
        else:
            # 帐号已登录但网络断开
            print('ERRO: The account is logged in \
but the network is disconnected')

        if online_test():
            # 网络连接已恢复
            print('Info: Network connection restored')
        else:
            # 网络连接未恢复
            print('Warn: Network connection is not restored')


if __name__ == '__main__':
    usercode, password = sys.argv[1:]
    reconnect(usercode, password)

