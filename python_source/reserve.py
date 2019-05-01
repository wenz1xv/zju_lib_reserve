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
    print(rep,'\n ...<Response [200]>代表测试通过  <Response [500]> 代表时间设置有误')

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

# 输入数据
def inputInfo():
    uid = input('id:')
    pwd = input('password:')
    date = input('预约日期:(例如2019-4-30)')
    start_time = input('开始时间:(例如:8:30写作0830)')
    end_time = input('结束时间:(例如:8:30写作0830)')
    seat_source = input('选择座位:(例如F3-131)')
    seat = getSeatId(seat_source)
    return [seat, date, start_time, end_time, uid, pwd]


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

# 预约主体：获取sid、登陆、预约
def reserve_main():
    host = 'http://ic.zju.edu.cn/ClientWeb'
    main_url = host+'/xcus/ic2/Default.aspx'
    login_url = host+'/pro/ajax/login.aspx'
    reserve_url = host+'/pro/ajax/reserve.aspx'
    cookies = getSid(main_url)
    choose = input('是否使用cfg配置文件?\n y/n   ')
    if choose == 'y':
        reserveArr = confDeal()
        user = reserveArr[0]
        seat = reserveArr[1]
        seat1 = reserveArr[2]
        seat2 = reserveArr[3]
        if login(user, cookies, login_url):
           input('\n 登陆成功，Enter继续...')
           os.system('cls')
           if SetTime('24:00:00'):
                reserve(seat, cookies, reserve_url)
                if seat1 != False:
                    reserve(seat1,cookies,reserve_url)
                if seat2 != False:
                    reserve(seat2,cookies,reserve_url)
    else:
        reserveArr = inputInfo()
        if login(reserveArr, cookies, login_url):
           input('\n 登陆成功，Enter继续...')
           os.system('cls')
           if SetTime('24:00:00'):
                login(reserveArr, cookies, login_url)
                reserve(reserveArr, cookies, reserve_url)


# 定时判断器
def SetTime(timei):
    set_time = timei
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
            print('设定时间：', set_time, '现在时间:', now, '待机时间：', sleepTime,'s')
            time.sleep(sleepTime)
        else:
            print(now)
            return True

# 关机测试
def shutDown_test():
    choose = input(
        '你的电脑将在60s后关机，是否继续?\n y/n  ')
    if choose == 'y':
        print('60s 后关机')
        os.system('shutdown -s -f -t 60')
        time.sleep(55)
        print(' Goodbye in 5s ')
    # 回到test
    else :
        test()
        

# 预约测试-无定时
def reserve_test():
    main_url = 'http://ic.zju.edu.cn/ClientWeb/xcus/ic2/Default.aspx'
    login_url = 'http://ic.zju.edu.cn/ClientWeb/pro/ajax/login.aspx'
    reserve_url = 'http://ic.zju.edu.cn/ClientWeb/pro/ajax/reserve.aspx'
    cookies = getSid(main_url)
    choose = input('是否使用cfg配置文件?\n y/n   ')
    if choose == 'y':
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
    else:
        reserveArr = inputInfo()
        if login(reserveArr, cookies, login_url):
           input('\n 登陆成功，Enter继续...')
           os.system('cls')
           login(reserveArr, cookies, login_url)
           reserve(reserveArr, cookies, reserve_url)
    # 回到test
    choose = input('是否继续测试? \n y/n  ')
    if choose == 'y':
        test()

# 定时器测试
def Timer_test():
    time = input('计时器触发时间：(HH:MM:SS)')
    if SetTime(time):
        print('计时器 OK!')
    choose = input('是否继续测试? \n y/n  ')
    # 回到test
    if choose == 'y':
        test()

# 测试目录
def test():
    choose = input('测试选项: \n A.预约测试 \n B.自动关机测试 \n C.计时器测试 \n D.回到菜单 \n 输入 A/B/C/D 选择\n')
    if choose == 'A':
        reserve_test()
    elif choose == 'B':
        shutDown_test()
    elif choose == 'C':
        Timer_test()
    elif choose == 'D':
        print('回到菜单')
        os.system('cls')
    else:
        print('选项不存在，请输入 A/B/C/D')
        test()


# 主函数
def main():
    choose = input('\n***************************************\n* 欢迎使用图书馆自动预约-这是完全模式 *\n***************************************\n*        -在完成必要步骤后            *\n*      -软件将在00:00进行预约         *\n*       -预约完成自动关机             *\n*        ---键入y进入测试模式         *\n***************************************\n*         Powered by wenz_xv          *\n***************************************\n    是否测试：y/n ')
    if choose == 'y':
        test()
    # 主进程
    choose = input(
        '\n测试完成，是否继续测试? y/n   ')
    if choose == 'y':
        os.system('cls')
        main()
    else:
        print('进入预约系统...')
        time.sleep(5)
        os.system('cls')
        reserve_main()
        print('60s 后关机 \n 你可以关闭程序来阻止\n')
        time.sleep(50)
        print('10s后关机，可能不太能阻止了...')
        os.system('shutdown -s -f -t 10')


main()
