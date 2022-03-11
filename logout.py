#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import auth
import json
import requests

def logout(ip):
    """通过IP地址注销

    Args:
        ip: 需要注销主机的IP地址

    Returns:
        True: 注销成功
        False: 注销失败

    """
    with requests.Session() as s:
        s.headers.update({'User-Agent': auth.ua})
        url = 'http://172.16.255.11:801/eportal/'
        params = {
            'c': 'Portal',
            'a': 'unbind_mac',
            'wlan_user_ip': ip
        }
        
        logout_info = s.get(url, params=params)
        logout_info = json.loads(logout_info.text[7:-1])
        
    if logout_info['result'] == '1':
        return True
    else:
        return False

if __name__ == '__main__':
    ip = sys.argv[1:]

    if not auth.get_auth_status(ip):
        print('Not logged in, no need to log out')
        exit()

    if logout(ip):
        print('Logout succeeded')
    else:
        print('logout failed')

