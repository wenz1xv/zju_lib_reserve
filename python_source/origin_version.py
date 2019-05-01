import requests
import json
import time
import os

# 登陆


def login(arr, cookies, url):
    uid = arr[4]
    pwd = arr[5]
    body = {
        'id': uid,
        'pwd': pwd,
        'act': 'login',
    }
    rep = requests.post(url, cookies=cookies, data=body)
    reply = json.loads(rep.text)
    if reply['msg'] == 'ok':
        print('login success')
        return reply
    elif reply['msg'] != '':
        print(reply['msg'])
        reserve_main()
    else:
        print('login failed,\n please Try again')
        reserve_main()

# 获取asp.net SessionID
def getSid(url):
    rep = requests.get(url)
    cookies_rep = rep.cookies
    return cookies_rep

# 预约座位
def reserve(arr, cookies, url):
    seat = arr[0]
    date = arr[1]
    st = arr[2]
    et = arr[3]
    s_t = date+' '+st[0:2]+':'+st[2:]
    e_t = date+' '+et[0:2]+':'+et[2:]
    params = {
        'dev_id': seat,
        'type': 'dev',
        'start': s_t,
        'end': e_t,
        'start_time': st,
        'end_time': et,
        'act': 'set_resv'
    }
    try:
        rep = requests.get(url, params=params, cookies=cookies)
        reply = json.loads(rep.text)
        print(reply['msg'])
        return reply['msg']
    except:
        print('Some Error happend,please Try again')


# 输入数据
def inputInfo():
    uid = input('id:')
    pwd = input('password:')
    seat = input('the seat you want to reserve:')
    date = input('reserve date:(should be inputed as 2019-4-30)')
    start_time = input('start time:(8:30 should be inputed as 0830)')
    end_time = input('end time:(8:30 should be inputed as 0830)')
    return [seat, date, start_time, end_time, uid, pwd]

# 预约主体：获取sid、登陆、预约
def reserve_main():
    main_url = 'http://ic.zju.edu.cn/ClientWeb/xcus/ic2/Default.aspx'
    login_url = 'http://ic.zju.edu.cn/ClientWeb/pro/ajax/login.aspx'
    reserve_url = 'http://ic.zju.edu.cn/ClientWeb/pro/ajax/reserve.aspx'
    cookies = getSid(main_url)
    reserveArr = inputInfo()
    user = login(reserveArr, cookies, login_url)
    print('Welcome '+user['data']['name'])
    if SetTime():
        reserve(reserveArr, cookies, reserve_url)


# 定时判断器
def SetTime():
    set_time = input(
        'input your reserve time:(you can also press enter to use default time:00:00)')
    if set_time == '':
        set_time = '00:00'
    print('Timer is on, please wait...')
    while True:
        now = time.strftime('%H:%M', time.localtime(time.time()))
        if set_time == now:
            return True

# 关机测试
def shutDown_test():
    choose = input(
        'Your computer will shutdown in 10s, are you sure to continue?\n y/n  ')
    if choose == 'y':
        print('30s later shutdown')
        time.sleep(20)
        print('shutDown in 10s')
        os.system('shutdown -s -f -t 10')
    choose = input('Do you want to continue? \n y/n  ')
    if choose == 'y':
        test()

# 预约测试-无定时
def reserve_test():
    main_url = 'http://ic.zju.edu.cn/ClientWeb/xcus/ic2/Default.aspx'
    login_url = 'http://ic.zju.edu.cn/ClientWeb/pro/ajax/login.aspx'
    reserve_url = 'http://ic.zju.edu.cn/ClientWeb/pro/ajax/reserve.aspx'
    cookies = getSid(main_url)
    reserveArr = inputInfo()
    user = login(reserveArr, cookies, login_url)
    print('Welcome '+user['data']['name'])
    reserve(reserveArr, cookies, reserve_url)
    
    choose = input('Do you want to continue? \n y/n  ')
    if choose == 'y':
        test()

# 定时器测试
def Timer_test():
    if SetTime():
        print('timer test OK!')
    choose = input('Do you want to continue? \n y/n  ')
    if choose == 'y':
        test()

# 测试目录
def test():
    choose = input('which do you want to test? \n A.test reserve \n B.test auto-shutdown \n C.test Timer \n D.back to main \n Enter A/B/C/D or JUST rnter to continue \n')
    if choose == 'A':
        reserve_test()
    elif choose == 'B':
        shutDown_test()
    elif choose == 'C':
        Timer_test()
    elif choose == 'D':
        print('Start')
    else:
        print('Wrong choose,please enter A/B/C/D')
        test()


# 主函数
def main():
    choose = input(
        'welcome to the zju lib reserve tool,press enter to continue\n Do you want to test it ? \n y/n   ')
    if choose == 'y':
        test()
# 主进程
    reserve_main()
    print('30s later shut down\n you can stop it by close')
    time.sleep(20)
    print('there are still 10s')
    os.system('shutdown -s -f -t 10')


main()