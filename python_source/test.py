import requests
import json
import time
import datetime
import os
import configparser
import sys
import hashlib
import getpass

# version2.0_测试

# 登陆


def login(arr,cookies):
    if judgeLogin(cookies):
        print('已登录')
        time.sleep(3)
    else:
        url = 'http://ic.zju.edu.cn/ClientWeb/pro/ajax/login.aspx'
        uid = arr[0]
        pwd = arr[1]
        flag = arr[2]
        body = {
            'id': uid,
            'pwd': pwd,
            'act': 'login',
        }
        rep = requests.post(url, cookies=cookies, data=body)
        reply = json.loads(rep.text)
        if reply['msg'] == 'ok':
            print('\n login success')
            print('Welcome '+reply['data']['name']+'\n')
            if flag:
                return reply['data']
            else:
                return True
        else:
            print('login failed,\n please Try again')
            ide = input('id:')
            pwde = input('pwd')
            login([ide, pwde, False],cookies)

# 获取asp.net SessionID


def getSid():
    url = 'http://ic.zju.edu.cn/ClientWeb/xcus/ic2/Default.aspx'
    rep = requests.get(url)
    cookies_rep = rep.cookies
    return cookies_rep


def inputInfo(flag):
    if flag == True:
        uid = input('id:')
        pwd = input('password:')
        return [uid, pwd, True]
    else:
        input('id:')

# 对config的总处理



def loginTest(cookies):
    if judgeLogin(cookies):
        print('已登陆')
        time.sleep(5)
    else:
        user = inputInfo(True)
        print('账户信息：\n', login(user,cookies))
        time.sleep(5)
    # 回到test.sleep(5)
    os.system('cls')
    loginTest(cookies)

# 测试目录

def judgeLogin(cookies):
    judurl = 'http://ic.zju.edu.cn/ClientWeb/pro/ajax/login.aspx?act=is_login'
    repj = json.loads(requests.get(judurl, cookies=cookies).text)
    if repj['ret'] == 1:
        return True
    else:
        return False





cookies = getSid()
loginTest(cookies)