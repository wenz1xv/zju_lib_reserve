
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
        'start': s_t,
        'end': e_t,
        'start_time': st,
        'end_time': et,
        'act': 'set_resv'
    }

    rep = requests.get(url, params=params, cookies=cookies)
    input(rep,'\n ...<Response [200]>代表测试通过  <Response [500]> 代表时间设置有误')

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
        

# 从config读数据
def readSeat(seat):
    conf = configparser.ConfigParser()
    conf.read('./user_data.cfg')
    date = conf.get(seat, 'reserve_date')
    start_time = conf.get(seat, 'reserve_start_time')
    end_time = conf.get(seat, 'reserve_end_time')
    seat_source = conf.get(seat, 'seat')
    seat = getSeatId(seat_source)
    return [seat, date, start_time, end_time]



def confDeal():
    conf = configparser.ConfigParser()
    conf.read('./user_data.cfg')
    uid = conf.get('user_set', 'user_id')
    pwd = conf.get('user_set', 'user_password')    
    if pwd == '000000':
        pwd = input('输入密码:')
        os.system('cls')
        user = [uid,pwd]
    else:
        user = [uid,pwd]
    flag1 = conf.get('seat_set_1', 'flag')
    flag2 = conf.get('seat_set_2', 'flag')
    arr1 = readSeat('seat_set')

    if flag1 == 'true':
        arr2 = readSeat('seat_set_1')
    else:
        arr2 = False

    if flag2 == 'true':
        arr3 = readSeat('seat_set_2')
    else:
        arr3 = False
    return [user,arr1,arr2,arr3]



# 定时判断器

        
def reserve_test():
    main_url = 'http://ic.zju.edu.cn/ClientWeb/xcus/ic2/Default.aspx'
    login_url = 'http://ic.zju.edu.cn/ClientWeb/pro/ajax/login.aspx'
    reserve_url = 'http://ic.zju.edu.cn/ClientWeb/pro/ajax/reserve.aspx'
    cookies = getSid(main_url)
    reserveArr = confDeal()
    user = reserveArr[0]
    seat = reserveArr[1]
    seat1 = reserveArr[2]
    seat2 = reserveArr[3]
    if login(user, cookies, login_url):
        input('\n 登陆成功，Enter继续...')
        os.system('cls')
        reserve(seat, cookies, reserve_url)
        if seat1 != False:
            reserve(seat1,cookies,reserve_url)
        if seat2 != False:
            reserve(seat2,cookies,reserve_url)

reserve_test()