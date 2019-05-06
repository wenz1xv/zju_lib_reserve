import requests
import json
import time
import os
import configparser
import sys
import datetime
import hashlib


#V2.0_测试

# 从config读数据


def readSeat(conf, seat):
    date = str(datetime.date.today() + datetime.timedelta(days=2))
    start_time = conf.get(seat, 'reserve_start_time')
    end_time = conf.get(seat, 'reserve_end_time')
    seat_source = conf.get(seat, 'seat')
    seat = getSeatId(seat_source)
    return [seat, date, start_time, end_time]


# 从conf里读取数据
def confDeal():
    conf = configparser.ConfigParser()
    conf.read('./user_data.cfg')
    # 读取用户数据
    uid = conf.get('user_set', 'user_id')
    pwd = conf.get('user_set', 'user_password')
    if pwd == '000000':
        pwd = input('输入密码:')
        os.system('cls')
    user = [uid,pwd]
    # 读取座位是否启用
    flag1 = conf.get('seat_set_1', 'flag')
    flag2 = conf.get('seat_set_2', 'flag')
    # 读取座位1
    arr1 = readSeat(conf, 'seat_set')
    if flag1 == 'true':
        arr2 = readSeat(conf, 'seat_set_1')
    else:
        arr2 = False
    if flag2 == 'true':
        arr3 = readSeat(conf, 'seat_set_2')
    else:
        arr3 = False
    return [user, arr1, arr2, arr3]


# 登陆
def login(arr, cookies):
    # 先判断是否已经登陆
    judurl = 'http://ic.zju.edu.cn/ClientWeb/pro/ajax/login.aspx?act=is_login'
    repj = json.loads(requests.get(judurl, cookies=cookies).text)
    if repj['ret'] == 1:
        return True
    # 进行登陆
    else:
        url = 'http://ic.zju.edu.cn/ClientWeb/pro/ajax/login.aspx'
        uid = arr[0]
        pwd = arr[1]
        body = {
            'id': uid,
            'pwd': pwd,
            'act': 'login',
        }
        reply = json.loads(requests.post(url, cookies=cookies, data=body).text)
        # 如果登陆成功
        if reply['msg'] == 'ok':
            print('\n login success')
            print('Welcome '+reply['data']['name']+'\n')
            return True
        # 失败重试
        else:
            print('login failed')
            ide = input('id:')
            pwde = input('pwd')
            login([ide,pwde],cookies)


# 预约座位


def reserve(arr, cookies):
    url = 'http://ic.zju.edu.cn/ClientWeb//pro/ajax/reserve.aspx'
    seat = arr[0]
    date = arr[1]
    st = arr[2]
    et = arr[3]
    # 开始时间格式:2019-4-20 09:10
    s_t = date+' '+st[0:2]+':'+st[2:]
    e_t = date+' '+et[0:2]+':'+et[2:]
    params = {
        'dev_id': seat,
        'type': 'dev',
        'test_name': '个人',
        'start': s_t,
        'end': e_t,
        'start_time': st,
        'end_time': et,
        'act': 'set_resv'
    }
    rep = requests.get(url, params=params, cookies=cookies)
    print(rep, '\n', rep.text)

# 转换座位id
def getSeatId(seat):
    print('\n 寻找你的座位...')
    date = str(datetime.date.today())
    url = 'http://ic.zju.edu.cn/ClientWeb/pro/ajax/device.aspx'
    params = {
        'date': date,
        'act': 'get_rsv_sta'
    }
    rep = requests.get(url, params=params)
    content = json.loads(rep.text)
    seatObj = content['data']
    for obj in seatObj:
        if obj['title'] == seat:
            print('\n 校对你的座位信息:')
            retxt = '\n className: ' + str(obj['className'])+'   labName: ' + str(obj['labName'])+'   kindName: ' + str(obj['kindName'])+' devName: ' + str(obj['devName'])+'\n open_time: ' + '-'.join(obj['open'])+'   devId: ' + str(obj['devId'])
            print(retxt)
            time.sleep(3)
            return obj['devId']
    print('cannot find the seat.\n please try again\n')
    s = input('输入座位：')
    getSeatId(s)






# 预约主体：获取sid、登陆、预约
def reserve_main():
    main_url = 'http://ic.zju.edu.cn/ClientWeb/xcus/ic2/Default.aspx'
    # 得到cookies----asp.net session id
    rep = requests.get(main_url)
    Cookies = rep.cookies
    reserveArr = confDeal()
    user = reserveArr[0]
    seat = reserveArr[1]
    seat1 = reserveArr[2]
    seat2 = reserveArr[3]
    if login(user, Cookies):
        print('\n 登陆成功...')
        time.sleep(2)
        os.system('cls')
        if SetTime():
            reserve(seat, Cookies)
            if seat1 != False:
                reserve(seat1, Cookies)
            if seat2 != False:
                reserve(seat2, Cookies)


# 定时判断器
def SetTime():
    set_time = '24:00:03'
    print('定时器启动...')
    count = 3
    while True:
        now = time.strftime('%H:%M:%S', time.localtime(time.time()))
        H = int(set_time.split(':')[0]) - int(now.split(':')[0])
        M = int(set_time.split(':')[1]) - int(now.split(':')[1])
        S = int(set_time.split(':')[2]) - int(now.split(':')[2])
        sleepTime = M*60+S+H*3600
        if H > 23:
            sys.stdout.write('\r{0}'.format('设定时间：'+set_time + '  现在时间:'+now+'  待机时间：'+str(count)))
            time.sleep(1)
            sys.stdout.flush()
            count = count - 1
            if count < 1:
                print('\n now!')
                return True
        elif H > 1:
            sys.stdout.write('\r{0}'.format(
                '剩余：'+str(round(H+M/60, 1)) + '小时,待机中...'))
            time.sleep(360)
            sys.stdout.flush()
        elif sleepTime > 120:
            sys.stdout.write('\r{0}'.format(
                '剩余：'+str(round(H*60+M+S/60, 1)) + '分钟,待机中...'))
            time.sleep(6)
            sys.stdout.flush()
        elif sleepTime > 3:
            sys.stdout.write('\r{0}'.format(
                '设定时间：'+set_time + '  现在时间:'+now+'  待机时间：'+str(sleepTime)))
            time.sleep(1)
            sys.stdout.flush()
        else:
            input('wrong')

# 验证
def encipher():
    ipt = input('验证码：')
    hl = hashlib.md5()
    hl.update(ipt.encode(encoding='utf-8'))
    if hl.hexdigest() == 'bcedc450f8481e89b1445069acdc3dd9':
        return True


# 主函数
def main():
    input('\n***************************************\n* 欢迎使用图书馆自动预约-这是自动模式 *\n***************************************\n* -在完成必要步骤后                   *\n* -软件将在00:15进行预约              *\n* -预约完成自动关机                   *\n* ---请确保：                         *\n*   1、各部分功能能够顺利运行         *\n*   2、电脑电源模式不会自动关机或待机 *\n*   3、完成配置文件                   *\n***************************************\n*         Powered by wenz_xv          *\n***************************************\n    Enter启动... ')

    # 主进程
    reserve_main()
    print('30s 后关机 \n 你可以关闭程序来阻止\n')
    time.sleep(20)
    print('10s后关机，可能不太能阻止了...')
    os.system('shutdown -s -f -t 10')


if encipher():
    os.system('cls')
    main()
