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
#cookies 带时间码，每获取一次都会变！

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
            print('login success')
            print('Welcome '+reply['data']['name'])
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

# 预约座位


def reserve(arr,cookies):
    url = 'http://ic.zju.edu.cn/ClientWeb//pro/ajax/reserve.aspx'
    seat = arr[0]
    date = arr[1]
    st = arr[2]
    et = arr[3]
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
    print(rep)
    debug = getpass.getpass(
        '\n ...<Response [200]>代表正常  <Response [500]> 代表时间设置有误，具体是否成功请登陆网站查看,Enter to contiune...')
    if debug == 'd':
        print(rep.text)

# 转换座位id


def getSeatId(seat, date):
    print('\n 寻找你的座位id...')
    seatObj = getJson(date)
    for e in seatObj:
        if e['title'] == seat:
            print('校对 '+date+' 座位信息:')
            print(fil_ter(e, 1))
            time.sleep(10)
            return e['devId']
    print('cannot find the seat.\n please try again\n')
    s = input('输入座位：')
    getSeatId(s, date)


# 从config读座位信息
def readSeat(seat):
    conf = configparser.ConfigParser()
    conf.read('./user_data.cfg')
    start_time = conf.get(seat, 'reserve_start_time')
    end_time = conf.get(seat, 'reserve_end_time')
    seat_source = conf.get(seat, 'seat')
    seat = getSeatId(seat_source, str(datetime.date.today()))
    date = str(datetime.date.today() + datetime.timedelta(days=2))
    return [seat, date, start_time, end_time]

# 输入数据


def inputInfo(flag):
    if flag == True:
        uid = input('id:')
        pwd = input('password:')
        time.sleep(0.5)
        os.system('cls')
        return [uid, pwd, True]
    else:
        uid = input('id:')
        pwd = input('password:')
        time.sleep(0.5)
        os.system('cls')
        flag = input('预约日期:(留空今日，tm-明日)')
        if flag == 'tm':
            date = str(datetime.date.today() + datetime.timedelta(days=1))
        else:
            date = str(datetime.date.today())
        start_time = input('开始时间:(例如:8:30写作0830)')
        end_time = input('结束时间:(例如:12:30写作1230)')
        seat_source = input('选择座位:(例如F3-001)')
        seat = getSeatId(seat_source, date)
        return [[uid, pwd, False], [seat, date, start_time, end_time]]

# 对config的总处理


def confDeal():
    conf = configparser.ConfigParser()
    conf.read('./user_data.cfg')
    uid = conf.get('user_set', 'user_id')
    pwd = conf.get('user_set', 'user_password')
    if pwd == '000000':
        pwd = input('输入密码:')
        os.system('cls')
        user = [uid, pwd]
    else:
        user = [uid, pwd]
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
    return [user, arr1, arr2, arr3]



# 定时判断器
def SetTime(set_time):
    print('定时器启动...')
    count = 5
    while True:
        now = time.strftime('%H:%M:%S', time.localtime(time.time()))
        H = int(set_time.split(':')[0]) - int(now.split(':')[0])
        M = int(set_time.split(':')[1]) - int(now.split(':')[1])
        S = int(set_time.split(':')[2]) - int(now.split(':')[2])
        sleepTime = M*60+S+H*3600
        if H > 23:
            sys.stdout.write('\r{0}'.format(str(count) + 's 后启动'))
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
        elif sleepTime > 5:
            sys.stdout.write('\r{0}'.format(
                '设定时间：'+set_time + '  现在时间:'+now+'  待机时间：'+str(sleepTime)))
            time.sleep(1)
            sys.stdout.flush()
        # else:
        #     os.system('cls')
        #     sys.stdout.write('\r{0}'.format(
        #         '设定时间：'+set_time + '  现在时间:'+now+'  待机时间：'+str(count)))
        #     sys.stdout.flush()
        #     time.sleep(1)
        #     count = count - 1
        #     if count < 1:
        #         print('\n now!')
        #         return True

# 关机测试


def shutDown_test():
    flag = input('设置定时关机时间(HH:MM:SS 例如 13:01:23)\n(留空60s后关机):')
    if flag != '':
        if SetTime(flag):
            print('定时时间到！')
    choose = input('你的电脑将在60s后关机，是否继续?\n y/n  ')
    if choose == 'y':
        print('60s 后关机，关闭弹窗无用')
        os.system('shutdown -s -f -t 60')
        time.sleep(50)
        print(' Goodbye in 10s ')
    # 回到test
    else:
        test()


# 预约测试-无定时
def reserve_test(cookies):
    reserveArr = inputInfo(False)
    user = reserveArr[0]
    seat = reserveArr[1]
    if login(user,cookies):
        time.sleep(1)
        os.system('cls')
        login(user,cookies)
        reserve(seat,cookies)
    # 回到test
    time.sleep(5)
    os.system('cls')
    choose = input('是否回到模块? \n y/n  ')
    if choose == 'y':
        test()

# 定时器测试


def Timer_test():
    time_set = input('计时器触发时间：(HH:MM:SS 例如 13:01:23)')
    if SetTime(time_set):
        print('计时器 OK!')
    # 回到test
    time.sleep(5)
    os.system('cls')
    choose = input('是否回到模块? \n y/n  ')
    if choose == 'y':
        test()

# 登陆测试


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
    choose = input('是否回到模块? \n y/n  ')
    if choose == 'y':
        test()

# 测试目录

def judgeLogin(cookies):
    judurl = 'http://ic.zju.edu.cn/ClientWeb/pro/ajax/login.aspx?act=is_login'
    repj = json.loads(requests.get(judurl, cookies=cookies).text)
    if repj['ret'] == 1:
        return True
    else:
        return False

def test():
    cookies = getSid()
    choose = input(
        '测试选项:\n A.登陆信息  \n B.座位预约 \n C.定时关机 \n D.计时器测试 \n E.回到菜单 \n 输入 A/B/C/D/E 选择\n')
    if choose == 'A':
        loginTest(cookies)
    elif choose == 'B':
        reserve_test(cookies)
    elif choose == 'C':
        shutDown_test()
    elif choose == 'D':
        Timer_test()
    elif choose == 'E':
        print('回到菜单')
        time.sleep(2)
        os.system('cls')
    else:
        print('选项不存在，请输入 A/B/C/D')
        test()

# 获取座位信息


def getJson(date):
    url = 'http://ic.zju.edu.cn/ClientWeb/pro/ajax/device.aspx'
    params = {
        'date': date,
        'act': 'get_rsv_sta'
    }
    rep = requests.get(url, params=params)
    content = json.loads(rep.text)
    return content['data']

# 座位信息总处理


def seatLook(cookies):
    flag = input('查询日期:(留空今天，tm-明天)')
    if flag == 'tm':
        date = str(datetime.date.today() + datetime.timedelta(days=1))
    else:
        date = str(datetime.date.today())
    content = getJson(date)
    seat = input('查询座位:(留空查询所有座位信息)')
    if seat != '':
        for e in content:
            if e['title'] == seat:
                print(fil_ter(e, 1))
                scc = getpass.getpass('\npress Enter to continue...')
                if encipher(scc):
                    ret = []
                    for acc in e['ts']:
                        ret.append(userDetail(acc['accno'],cookies))
                    print('个人资料：\n','\n'.join(ret))
                time.sleep(10)
                os.system('cls')
                break
        else:
            print('Cannot find the seat')
            time.sleep(3)
            os.system('cls')
            seatLook(cookies)
    else:
        newContent = []
        filename = 'seat_info'+str(date)+'.txt'
        for e in content:
            if e['labId'] != '173':
                newContent.append(fil_ter(e, 1))
        data = '\n'.join(newContent)
        seat_file = open(filename, 'w')
        seat_file.write(data)
        seat_file.close()
        print('内容写入 '+filename)
        time.sleep(3)

# 验证器
def encipher(ipt):
    if ipt == ' ':
        ipt = input('请输入验证码以继续：')
    hl = hashlib.md5()
    hl.update(ipt.encode(encoding='utf-8'))
    if hl.hexdigest() == 'bcedc450f8481e89b1445069acdc3dd9':
        return True
    elif ipt == '':
        return False
    # else:
        # print('验证码错误,程序退出')
# 筛选json


def fil_ter(obj, n):
    if n == 1:
        retxt = '\n className: ' + str(obj['className'])+'   labName: ' + str(obj['labName'])+'   kindName: ' + str(
            obj['kindName'])+' devName: ' + str(obj['devName'])+'\n open_time: ' + '-'.join(obj['open'])+'   devId: ' + str(obj['devId'])
        count = 0
        if obj['ts'] != []:
            for e in obj['ts']:
                user = '\n user ' + str(count)
                retxt = retxt + user + '\n title: ' + str(e['title']) + ' state: ' + str(
                    e['state'])+'\n start: ' + str(e['start']) + '  end: ' + str(e['end'])
                count = count + 1
        else:
            retxt = retxt + '\n Free'
        return retxt
    if n == 2:
        devtxt = '\n className: ' + str(obj['className'])+'   labName: ' + str(obj['labName'])+'   kindName: ' + str(
            obj['kindName'])+' devName: ' + str(obj['devName'])+'   devId: ' + str(obj['devId'])
        timetxt = '\n open_time: ' + '-'.join(obj['open'])
        retxt = devtxt+timetxt
        count = 0
        if obj['ts'] != []:
            for e in obj['ts']:
                user = str(e['owner'])+'   '+str(e['accno'])
                retxt = retxt + user + '\n title: ' + str(e['title']) + ' state: ' + str(
                    e['state'])+'\n start: ' + str(e['start']) + '  end: ' + str(e['end'])
                count = count + 1
        else:
            retxt = retxt + '\n Free'
        return retxt


def userDetail(accno,cookies):
    if judgeLogin(cookies):
        os.system('cls')
        url = 'http://ic.zju.edu.cn/ClientWeb/pro/ajax/account.aspx'
        params = {
            'accno': accno,
            'act': 'get_acc_accno'
        }
        rep = json.loads(requests.get(url, params=params,cookies = cookies).text)
        data = rep['data']
        retxt = ''
        for obj in data:
            retxt = retxt+'\n id: ' + str(obj['id'])+'\n name: ' + str(obj['name'])+'\n phone: ' + str(obj['phone'])+'\n email: ' + str(obj['email'])+'\n dept: ' + str(obj['dept'])
        return retxt
    else:
        print('还未登陆，无法查看，请登录')
        user = inputInfo(True)
        login(user,cookies)
        return userDetail(accno,cookies)       

# 用户数据获得


def userData(cookies):
    # 确定日期
    flag = input('查询日期:(留空今天，tm-明天)')
    if flag == 'tm':
        date = datetime.date.today() + datetime.timedelta(days=1)
    else:
        date = datetime.date.today()
    # 拿到当天所有座位信息
    content = getJson(str(date))
    # 输入用户
    user = input('search for user:(empty for all users)')
    if user != '':
        prtxt = ''
        accno = []
        for obj in content:
            for e in obj['ts']:
                if e['owner'] == user:
                    restr = '\n owner:' + str(e['owner']) + '\n accno:' + str(e['accno'])+'\n title:' + str(e['title'])+'\n start:' + str(e['start']) + '   end:' + str(e['end']) + '\n className:' + str(
                        obj['className'])+'     labName:' + str(obj['labName']) + '       kindName:' + str(obj['kindName'])+'     devName:' + str(obj['devName'])+'\n state:' + str(e['state'])
                    accno.append(e['accno'])
                    prtxt = prtxt + restr+'\n'
        if prtxt != '':
            print(prtxt)
            scc = getpass.getpass('\npress Enter to continue...')
            if encipher(scc):
                if accno != []:
                    for acc in accno:
                        print(userDetail(acc,cookies))
                        time.sleep(10)
            os.system('cls')
            reserve_sys()
        else:
            print('Cannot find the user')
            time.sleep(3)
            os.system('cls')
            reserve_sys()
    else:
        filename = 'user_info'+str(date)+'.txt'
        txtdata = ''
        for obj in content:
            if obj['ts'] != []:
                for e in obj['ts']:
                    restr = '\n owner:' + str(e['owner'])+'\n accno:' + str(e['accno'])+'\n title:' + str(e['title'])+'\n start:' + str(e['start']) + '   end:' + str(e['end']) + '\n className:' + str(
                        obj['className'])+'     labName:' + str(obj['labName']) + '       kindName:' + str(obj['kindName'])+'     devName:' + str(obj['devName'])+'\n state:' + str(e['state'])
                    txtdata = txtdata+restr+'\n'
        seat_file = open(filename, 'w')
        seat_file.write(txtdata)
        seat_file.close()
        print('内容写入 '+filename)
        time.sleep(3)
        os.system('cls')
        reserve_sys()




# 预约主体：获取sid、登陆、预约
def reserve_main(cookies):
    choose = input('是否使用cfg配置文件?\n y/n   ')
    if choose == 'y':
        reserveArr = confDeal()
        user = reserveArr[0]
        user.append(False)
        seat = reserveArr[1]
        seat1 = reserveArr[2]
        seat2 = reserveArr[3]
        if login(user,cookies):
            print('\n 登陆成功')
            time.sleep(3)
            os.system('cls')
            if SetTime('24:00:15'):
                reserve(seat,cookies)
                if seat1 != False:
                    reserve(seat1,cookies)
                if seat2 != False:
                    reserve(seat2,cookies)
    else:
        reserveArr = inputInfo(False)
        user = reserveArr[0]
        user.append(False)
        seat = reserveArr[1]
        if login(user,cookies):
            print('\n 登陆成功')
            time.sleep(3)
            os.system('cls')
            if SetTime('24:00:05'):
                login(user,cookies)
                reserve(seat,cookies)
# 预约主系统


def reserve_sys():
    os.system('cls')
    cookies = getSid()
    print('预约系统')
    time.sleep(1)
    scc = getpass.getpass('\npress Enter to continue...')
    if encipher(scc):
        userData(cookies)
    choose = input('是否查看座位? y/n   ')
    if choose == 'y':
        seatLook(cookies)
        reserve_sys()
    else:
        input('\npress Enter to continue...')
        os.system('cls')
        print('进入预约系统...')
        reserve_main(cookies)
        print('60s 后关机 \n 你可以关闭程序来阻止\n')
        time.sleep(50)
        print('10s后关机，可能不太能阻止了...')
        os.system('shutdown -s -f -t 10')

# 主函数入口
def main():
    choose = input('\n***************************************\n* 欢迎使用图书馆自动预约-这是完全模式 *\n* 为避免座位的恶性再分配-请勿传播程序 *\n***************************************\n*        -在完成必要步骤后            *\n*      -软件将在00:00进行预约         *\n*       -预约完成自动关机             *\n*        ---键入y进入功能模块         *\n***************************************\n*         Powered by wenz_xv          *\n***************************************\n    是否进入功能模块：y/n ')
    if choose == 'y':
        test()
    # 主进程
    choose = input('\n是否回到模块? y/n   ')
    if choose == 'y':
        os.system('cls')
        main()
    else:
        reserve_sys()


if encipher(' '):
    os.system('cls')
    main()
