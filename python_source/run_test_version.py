import requests
import json
import time
import os
import configparser
import json

# 登陆
def login(arr, cookies, url):
    uid = arr[0]
    pwd = arr[1]
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
        return True
    elif reply['msg'] != '':
        print('Error', reply['msg'])
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

    rep = requests.get(url, params=params, cookies=cookies)
    print(rep,'\n',rep.text)
        
# 转换座位id
def getSeatId(seat):
    print('\n 寻找你的座位id...')
    with open('./seat_data.json', 'r') as load_f:
        json_file = json.load(load_f)
        seatObj = json_file['data']
    for e in seatObj:
        if e['title'] == seat:
            print('校对你的座位信息:')
            print(e)
            time.sleep(3)
            return e['devID']
    print('cannot find the seat.\n please try again\n')
    s = input('输入座位：')
    getSeatId(s)


# 预约主体：获取sid、登陆、预约
def readUser(conf):
    uid = conf.get('user_set', 'user_id')
    pwd = conf.get('user_set', 'user_password')    
    if pwd == '000000':
        pwd = input('输入密码:')
        os.system('cls')
        return [uid,pwd]
    else:
        return [uid,pwd]

def confDeal():
    conf = configparser.ConfigParser()
    conf.read('./user_data.cfg')
    user = readUser(conf)
	date = conf.get(seat, 'reserve_date')
    start_time = conf.get(seat, 'reserve_start_time')
    end_time = conf.get(seat, 'reserve_end_time')
    seat_source = conf.get(seat, 'seat')
    seat = getSeatId(seat_source)
    arr = [seat, date, start_time, end_time]
    return [user,arr]

def reserve_main():
    host = 'http://ic.zju.edu.cn/ClientWeb'
    main_url = host+'/xcus/ic2/Default.aspx'
    login_url = host+'/pro/ajax/login.aspx'
    reserve_url = host+'/pro/ajax/reserve.aspx'
    cookies = getSid(main_url)
    reserveArr = confDeal()
    user = reserveArr[0]
    seat = reserveArr[1]
    if login(user, cookies, login_url):
        input('\n 登陆成功，Enter继续...')
        os.system('cls')
        if SetTime():
            reserve(seat, cookies, reserve_url)


# 定时判断器
def SetTime():
    set_time = '24:00:00'
    print('定时器启动...')
    while True:
        now = time.strftime('%H:%M:%S', time.localtime(time.time()))
        H = int(set_time.split(':')[0]) - int(now.split(':')[0])
        M = int(set_time.split(':')[1]) - int(now.split(':')[1])
        S = int(set_time.split(':')[2]) - int(now.split(':')[2])
        sleepTime = M*60+S+H*3600
        if H > 1:
            print('剩余：',round(H+M/60,1), '小时', '待机中...')
            time.sleep(3600)
        elif sleepTime > 1:
            print('设定时间：', set_time, '现在时间:', now, '待机时间：', sleepTime)
            time.sleep(sleepTime)
        else:
            print('now!')
            return True


# 主函数
def main():
    input('\n***************************************\n* 欢迎使用图书馆自动预约-这是自动模式 *\n***************************************\n* -在完成必要步骤后                   *\n* -软件将在00:00进行预约              *\n* -预约完成自动关机                   *\n* ---请确保：                         *\n*   1、各部分功能能够顺利运行         *\n*   2、电脑电源模式不会自动关机或待机 *\n*   3、完成配置文件                   *\n***************************************\n*         Powered by wenz_xv          *\n***************************************\n    Enter启动... ')
    
    # 主进程
    reserve_main()
    print('60s 后关机 \n 你可以关闭程序来阻止\n')
    time.sleep(50)
    print('10s后关机，可能不太能阻止了...')
    os.system('shutdown -s -f -t 10')


main()
