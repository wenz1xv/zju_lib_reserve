import requests
import json
import time,datetime
import os
import configparser
import sys

# 登陆
def login(arr, cookies, url):
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
        login([ide,pwde],cookies,url)

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
    print(rep,'\n ...<Response [200]>代表正常  <Response [500]> 代表时间设置有误，具体是否成功请登陆网站查看')

# 转换座位id
def getSeatId(seat):
    print('\n 寻找你的座位id...')
    date =  datetime.date.today()
    seatObj = getJson(date)
    for e in seatObj:
        newe = fil_ter(e)
        if e['title'] == seat:
            print('校对你的座位信息:\n')
            for item in newe:
                print(item,newe[item])
            time.sleep(3)
            return newe['devId']
    print('cannot find the seat.\n please try again\n')
    s = input('输入座位：')
    getSeatId(s)
        

# 从config读座位信息
def readSeat(seat):
    conf = configparser.ConfigParser()
    conf.read('./user_data.cfg')
    date = datetime.date.today() + datetime.timedelta(days=2)
    start_time = conf.get(seat, 'reserve_start_time')
    end_time = conf.get(seat, 'reserve_end_time')
    seat_source = conf.get(seat, 'seat')
    seat = getSeatId(seat_source)
    return [seat, date, start_time, end_time]

# 输入数据
def inputInfo(flag):
    if flag:
        uid = input('id:')
        pwd = input('password:')
        return [uid,pwd,True]        
    else:
        uid = input('id:')
        pwd = input('password:')
        date = input('预约日期:(例如2019-4-30)')
        start_time = input('开始时间:(例如:8:30写作0830)')
        end_time = input('结束时间:(例如:12:30写作1230)')
        seat_source = input('选择座位:(例如F3-001)')
        seat = getSeatId(seat_source)
        return [[uid, pwd,False],[seat, date, start_time, end_time]]

# 对config的总处理
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
        user.append(False)
        seat = reserveArr[1]
        seat1 = reserveArr[2]
        seat2 = reserveArr[3]
        if login(user, cookies, login_url):
           input('\n 登陆成功，Enter继续...')
           os.system('cls')
           if SetTime('24:00:15'):
                reserve(seat, cookies, reserve_url)
                if seat1 != False:
                    reserve(seat1,cookies,reserve_url)
                if seat2 != False:
                    reserve(seat2,cookies,reserve_url)
    else:
        reserveArr = inputInfo(False)
        user = reserveArr[0]
        user.append(False)
        seat = reserveArr[1]
        if login(user, cookies, login_url):
           input('\n 登陆成功，Enter继续...')
           os.system('cls')
           if SetTime('24:00:15'):
                login(user,cookies, login_url)
                reserve(seat, cookies, reserve_url)


# 定时判断器
def SetTime(set_time):
    print('定时器启动...')
    count = 30
    while True:
        now = time.strftime('%H:%M:%S', time.localtime(time.time()))
        H = int(set_time.split(':')[0]) - int(now.split(':')[0])
        M = int(set_time.split(':')[1]) - int(now.split(':')[1])
        S = int(set_time.split(':')[2]) - int(now.split(':')[2])
        sleepTime = M*60+S+H*3600
        if H > 1:
            sys.stdout.write('\r{0}'.format('剩余：'+str(round(H+M/60,1))+ '小时,待机中...'))
            time.sleep(360)
            sys.stdout.flush()
        elif sleepTime > 120:
            sys.stdout.write('\r{0}'.format('剩余：'+str(round(H*60+M+S/60,1))+ '分钟,待机中...'))
            time.sleep(60)
            sys.stdout.flush()
        elif sleepTime > 29:
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

# 关机测试
def shutDown_test():
    choose = input('你的电脑将在60s后关机，是否继续?\n y/n  ')
    if choose == 'y':
        print('60s 后关机，关闭弹窗无用')
        os.system('shutdown -s -f -t 60')
        time.sleep(50)
        print(' Goodbye in 10s ')
    # 回到test
    else :
        test()
        

# 预约测试-无定时
def reserve_test():
    host = 'http://ic.zju.edu.cn/ClientWeb'
    main_url = host+'/xcus/ic2/Default.aspx'
    login_url = host+'/pro/ajax/login.aspx'
    reserve_url = host+'/pro/ajax/reserve.aspx'
    cookies = getSid(main_url)
    choose = input('是否使用cfg配置文件?\n y/n   ')
    if choose == 'y':
        reserveArr = confDeal()
        user = reserveArr[0]
        user.append(False)
        seat = reserveArr[1]
        seat1 = reserveArr[2]
        seat2 = reserveArr[3]
        if login(user, cookies, login_url):
           time.sleep(1)
           os.system('cls')
           reserve(seat, cookies, reserve_url)
           if seat1 != False:
                reserve(seat1,cookies,reserve_url)
           if seat2 != False:
                reserve(seat2,cookies,reserve_url)
    else:
        reserveArr = inputInfo(False)
        user = reserveArr[0]
        seat = reserveArr[1]
        if login(user, cookies, login_url):
            time.sleep(1)
            os.system('cls')
            login(user,cookies, login_url)
            reserve(seat, cookies, reserve_url)
    # 回到test
    time.sleep(5)
    os.system('cls')
    choose = input('是否继续测试? \n y/n  ')
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
    choose = input('是否继续测试? \n y/n  ')
    if choose == 'y':
        test()

# 登陆测试
def loginTest():
    main_url = 'http://ic.zju.edu.cn/ClientWeb/xcus/ic2/Default.aspx'
    login_url = 'http://ic.zju.edu.cn/ClientWeb/pro/ajax/login.aspx'
    cookies = getSid(main_url)
    choose = input('是否使用cfg配置文件?\n y/n   ')
    if choose == 'y':
        reserveArr = confDeal()
        user = reserveArr[0]
        user.append(True)
        print('账户信息：\n',login(user, cookies, login_url))
    else:
        user = inputInfo(True)
        print('账户信息：\n',login(user, cookies, login_url))

    # 回到test
    time.sleep(5)
    os.system('cls')
    choose = input('是否继续测试? \n y/n  ')
    if choose == 'y':
        test()

# 测试目录
def test():
    choose = input('测试选项:\n A.登陆测试  \n B.预约测试 \n C.关机测试 \n D.计时器测试 \n E.回到菜单 \n 输入 A/B/C/D/E 选择\n')
    if choose == 'A':
        loginTest()
    elif choose == 'B':
        reserve_test()
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
    params ={
        'date':date,
        'act':'get_rsv_sta'
    }
    rep = requests.get(url,params = params)
    content = json.loads(rep.text)
    return content['data']

# 座位信息总处理
def chose():
    date = input('查询日期:(例如：2019-05-02)')
    content = getJson(date)
    seat = input('查询座位:(留空查询所有)')
    if seat == 'wow':
        user = input('search for user:')
        newContent = user_fil_ter(content)
        user_lst = []
        for e in newContent:
            if e['owner'] == user:
                user_lst.append(e)
        if user_lst != []:
            for item in range(len(user_lst)):
                print(user_lst[item])
            time.sleep(10)
            os.system('cls')
            chose()
        else:
            print('Cannot find the user')
            time.sleep(3)
            os.system('cls')
            chose() 
    elif seat != '':
        for e in content:
            if e['title'] == seat:
                newe = fil_ter(e)
                for item in newe:
                    print(item,newe[item])
                return ''
        else:
            print('Cannot find the seat')
            time.sleep(3)
            os.system('cls')
            chose()
    else:
        newContent = []
        for e in content:
            if e['labId'] != '173':
                newContent.append(str(fil_ter(e)))
        data = '\n'.join(newContent)
        write(data)
        return '内容写入 seat_info.txt，为避免下次查看影响，查看后请删除文件'
        
# 筛选json
def fil_ter(obj):
    reobj = {
        'className':  obj['className'],
        'labName': obj['labName'],
        'kindName': obj['kindName'],
        'devName': obj['devName'],
        'open_time': '-'.join(obj['open']),
        'devId': obj['devId']
    }
    count = 0
    if obj['ts'] != [] :
        user = {}
        for e in obj['ts']:
            user = 'user '+ str(count)
            reobj[user] = {
                'title': e['title'],
                'state': e['state'],
                'start': e['start'],
                'end': e['end']
            }
            count = count + 1
    else:
        reobj['user'] = 'no user' 
    return reobj

# 筛选json-为用户
def user_fil_ter(lst):
    relst =[]
    for obj in lst:
        if obj['ts'] != [] :
            for e in obj['ts']:
                reobj = {
                    'owner': e['owner'],
                    'accno': e['accno'],
                    'title': e['title'],
                    'start': e['start'],
                    'end': e['end'] ,
                    'className':  obj['className'],
                    'labName': obj['labName'],
                    'kindName': obj['kindName'],
                    'devName': obj['devName'],
                    'state': e['state'],
                }
                relst.append(reobj)
    return relst

# 写入data到seat_info.txt
def write(data):
    seat_file = open('seat_info.txt','w')
    seat_file.write(data)
    seat_file.close()


# 主函数
def main():
    choose = input('\n***************************************\n* 欢迎使用图书馆自动预约-这是完全模式 *\n* 为避免座位的恶性再分配-请勿传播程序 *\n***************************************\n*        -在完成必要步骤后            *\n*      -软件将在00:00进行预约         *\n*       -预约完成自动关机             *\n*        ---键入y进入测试模式         *\n***************************************\n*         Powered by wenz_xv          *\n***************************************\n    是否测试：y/n ')
    if choose == 'y':
        test()
    # 主进程
    choose = input('\n测试完成，是否继续测试? y/n   ')
    if choose == 'y':
        os.system('cls')
        main()
    else:
        choose = input('\n是否查看座位? y/n   ')
        if choose == 'y':
            print(chose())
        input('press Enter to continue...')
        os.system('cls')
        print('进入预约系统...')
        reserve_main()
        print('60s 后关机 \n 你可以关闭程序来阻止\n')
        time.sleep(50)
        print('10s后关机，可能不太能阻止了...')
        os.system('shutdown -s -f -t 10')


main()
