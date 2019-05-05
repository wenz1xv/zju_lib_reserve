import requests
import json
import time
import os
import configparser
import sys,datetime,hashlib

# 登陆
def login(arr, cookies, url):
    uid = arr[0]
    pwd = arr[1]
    body = {
        'id': uid,
        'pwd': pwd,
        'act': 'login',
    }
    reply = json.loads(requests.post(url, cookies=cookies, data=body).text)
    if reply['msg'] == 'ok':
        print('\n login success')
        print('Welcome '+reply['data']['name']+'\n')
        return True
    else:
        print('login failed,\n please Try again')
        ide = input('id:')
        pwd = input('pwd')
        login([ide,pwd],cookies,url)

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
        'test_name':'个人',
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
    date =  str(datetime.date.today())
    seatObj = getJson(date)
    for e in seatObj:
        newe = fil_ter(e)
        if e['title'] == seat:
            print('校对你的座位信息:')
            for item in newe:
                print(item,newe[item])
            time.sleep(3)
            return newe['devId']
    print('cannot find the seat.\n please try again\n')
    s = input('输入座位：')
    getSeatId(s)

def getJson(date):
    url = 'http://ic.zju.edu.cn/ClientWeb/pro/ajax/device.aspx'
    params ={
        'date':date,
        'act':'get_rsv_sta'
    }
    rep = requests.get(url,params = params)
    content = json.loads(rep.text)
    return content['data']

def fil_ter(obj):
    reobj = {
        'className':  obj['className'],
        'labName': obj['labName'],
        'kindName': obj['kindName'],
        'devName': obj['devName'],
        'open_time': '-'.join(obj['open']),
        'devId': obj['devId']
    }
    return reobj

# 从config读数据
def readSeat(conf,seat):
    date = str(datetime.date.today() + datetime.timedelta(days=2))
    start_time = conf.get(seat, 'reserve_start_time')
    end_time = conf.get(seat, 'reserve_end_time')
    seat_source = conf.get(seat, 'seat')
    seat = getSeatId(seat_source)
    return [seat, date, start_time, end_time]

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
    flag1 = conf.get('seat_set_1', 'flag')
    flag2 = conf.get('seat_set_2', 'flag')
    arr1 = readSeat(conf,'seat_set')
    if flag1 == 'true':
        arr2 = readSeat(conf,'seat_set_1')
    else:
        arr2 = False

    if flag2 == 'true':
        arr3 = readSeat(conf,'seat_set_2')
    else:
        arr3 = False
    return [user,arr1,arr2,arr3]

def reserve_main():
    host = 'http://ic.zju.edu.cn/ClientWeb'
    main_url = host+'/xcus/ic2/Default.aspx'
    login_url = host+'/pro/ajax/login.aspx'
    reserve_url = host+'/pro/ajax/reserve.aspx'
    cookies = getSid(main_url)
    reserveArr = confDeal()
    user = reserveArr[0]
    seat = reserveArr[1]
    seat1 = reserveArr[2]
    seat2 = reserveArr[3]
    if login(user, cookies, login_url):
        print('\n 登陆成功...')
        time.sleep(2)
        os.system('cls')
        if SetTime():
            reserve(seat, cookies, reserve_url)
            if seat1 != False:
                reserve(seat1,cookies,reserve_url)
            if seat2 != False:
                reserve(seat2,cookies,reserve_url)


# 定时判断器
def SetTime():
    set_time = '24:00:15'
    print('定时器启动...')
    count = 30
    while True:
        now = time.strftime('%H:%M:%S', time.localtime(time.time()))
        H = int(set_time.split(':')[0]) - int(now.split(':')[0])
        M = int(set_time.split(':')[1]) - int(now.split(':')[1])
        S = int(set_time.split(':')[2]) - int(now.split(':')[2])
        sleepTime = M*60+S+H*3600
        if H>23:
            sys.stdout.write('\r{0}'.format(str(count)+ 's 后启动'))
            time.sleep(1)
            sys.stdout.flush()
            count = count - 1
            if count < 1:
                print('now!')
                return True
        elif H > 1 :
            sys.stdout.write('\r{0}'.format('剩余：'+str(round(H+M/60,1))+ '小时,待机中...'))
            time.sleep(360)
            sys.stdout.flush()
        elif sleepTime > 120 :
            sys.stdout.write('\r{0}'.format('剩余：'+str(round(H*60+M+S/60,1))+ '分钟,待机中...'))
            time.sleep(60)
            sys.stdout.flush()
        elif sleepTime > 29 :
            sys.stdout.write('\r{0}'.format('设定时间：'+set_time+ '  现在时间:'+now+'  待机时间：'+str(sleepTime)))
            time.sleep(1)
            sys.stdout.flush()
        else:
            sys.stdout.write('\r{0}'.format(str(count)+ 's 后启动'))
            time.sleep(1)
            sys.stdout.flush()
            count = count - 1
            if count < 1:
                print('now!')
                return True

def encipher(ipt):
    if ipt == '':
        ipt = input('验证码：')
    hl = hashlib.md5()
    hl.update(ipt.encode(encoding='utf-8'))
    if hl.hexdigest() == 'bcedc450f8481e89b1445069acdc3dd9':
        return True


# 主函数
def main():
    input('\n***************************************\n* 欢迎使用图书馆自动预约-这是自动模式 *\n***************************************\n* -在完成必要步骤后                   *\n* -软件将在00:00进行预约              *\n* -预约完成自动关机                   *\n* ---请确保：                         *\n*   1、各部分功能能够顺利运行         *\n*   2、电脑电源模式不会自动关机或待机 *\n*   3、完成配置文件                   *\n***************************************\n*         Powered by wenz_xv          *\n***************************************\n    Enter启动... ')
    
    # 主进程
    reserve_main()
    print('30s 后关机 \n 你可以关闭程序来阻止\n')
    time.sleep(20)
    print('10s后关机，可能不太能阻止了...')
    os.system('shutdown -s -f -t 10')

if encipher(''):
    main()
