#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import sys
import uuid
import base64
import getpass
import requests

SUCCESS = 0
ID_FAILED = 1
AUTH_FAILED = 2

ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'


def auth(ip, usercode, password, isp):
    """登录并认证主机

    传入主机IP地址、学号、密码，对主机进行认证

    Args:
        IP: 主机IP地址
        usercode: 学号
        password: 密码
        isp: 运营商

        isp: xyw     教师专用
             telecom 中国电信
             cmcc    中国移动
             unicom  中国联通
             edu     教育网


    Returns:
        SUCCESS: 登录认证成功
        ID_FAILED: 学号认证失败
        AUTH_FAILE: 密码或学号错误
    """
    auth_str = '||{ip}|000000000000|@{isp}|1'.format(ip=ip, isp=isp)

    auth_code = str(base64.b64encode(bytes(auth_str, encoding='utf-8')),
                    encoding='utf-8')

    post_uuid = str(uuid.uuid1()).upper()

    post_data = {'type': '1',
                 'deviceId': post_uuid,
                 'username': usercode,
                 'password': password,
                 'img_code': '',
                 }

    # 访问外网登录服务器
    # redirect_uri之后是登录成功重定向url
    # state之后是base64之后的验证参数
    with requests.Session() as s:
        s.headers.update({'User-Agent': ua})
        url = 'http://sso.cqcet.edu.cn/oauth/authorize'
        params = {
            'client_id': 'rd-legal-web',
            'redirect_uri':
                'http://172.16.255.11:801/eportal/controller/oauth.php',
            'response_type': 'code',
            'state': auth_code,
        }
        params_str = "&".join("%s=%s" % (k, v) for k, v in params.items())
        s.get(url, params=params_str)

        # 对校园学号进行认证
        url = 'http://sso.cqcet.edu.cn/verificationCode'
        params = {'userCode': usercode}
        code_response = s.get(url, params=params)

        # 学号认证失败返回1
        if code_response.text != 'false':
            return ID_FAILED

        # 登录
        url = 'http://sso.cqcet.edu.cn/uaa/login_process'
        login_response = s.post(url, data=post_data)

        # 学号或密码错误返回2
        if 'http://172.16.255.11' not in login_response.url:
            return AUTH_FAILED

        return SUCCESS


def get_auth_status(ip):
    """获取主机是否认证成功

    传入主机IP地址，获取主机是否认证成功

    Args:
       ip: 主机IP地址

    Returns:
        True: 认证成功
        False: 认证失败
    """
    with requests.Session() as s:
        s.headers.update({'User-Agent': ua})
        url = 'http://172.16.255.11:801/eportal/'
        params = {
            'c': 'Portal',
            'a': 'find_mac',
            'wlan_user_ip': ip,
        }
        auth_status = s.get(url, params=params)

        auth_code = re.search(r'\"result\":\"(.)\"', auth_status.text).group(1)
        if auth_code == '1':
            return True
        else:
            return False


if __name__ == '__main__':
    ip, usercode = sys.argv[1:]
    if get_auth_status(ip):
        print('You are already logged in')
    else:
        ipss = ['xyw', 'telecom', 'cmcc', 'unicom', 'edu']
        print(
            '1. xyw (Teacher only)\n' +
            '2. telecom\n'  +
            '3. cmcc\n' +
            '4. unicom\n' +
            '5. edu'
        )
        isp = int(input('Please select an ISP [1-5]:')) - 1
        password = getpass.getpass()
        
        print(auth(ip, usercode, password, ipss[isp]))

        if get_auth_status(ip):
            print('Login successful')
        else:
            print('Login failed')

