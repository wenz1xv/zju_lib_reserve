import requests
import json
import time
import os
import configparser
import sys
import datetime
import hashlib

#V2.1,独立运行,自动生成配置文件,部分验证

def veridate(sta,edt):

    # 校验日期
    st = int(sta)
    et = int(edt)
    if (et-st)> 400:
        print('超过四小时')
        return False
    elif (et-st) < 60 :
        print('小于一小时')
        return False
    elif (et % 100) > 59:
        print('时间格式不符合')
        return False
    elif (st % 100) > 59:
        print('时间格式不符合')
        return False
    elif et>2230:
        print('太晚了')
        return False
    elif st<830:
        print('太早了')
        return False
    return True
    
    


# 从conf里读取数据
def confDeal():
    os.system('cls')
    # 配置文件存在

    if os.path.exists('data.ini') == True:
        
        conf = configparser.ConfigParser()
        conf.read('data.ini')
        uid = conf.get('user_set', 'user_id')
        pwd = conf.get('user_set', 'user_pwd')
        cookies_w = json.loads(conf.get('user_set','cookies'))
        if pwd == '000000':
            pwd = input('输入密码:')
            if input('是否保存密码(y/n)：') == 'y':
                conf.set("user_set","user_pwd",value=pwd)
            os.system('cls')
        while (login([uid,pwd,cookies_w]) == False):
            uid = input('id:')
            pwd = input('pwd:')
            if input('是否保存密码(y/n)：') == 'y':
                conf.set("user_set","user_pwd",value=pwd)
        user = [uid,pwd,cookies_w]

        # 座位信息

        print('座位1：',conf.items('seat_1'))
        arr1 = seatW(conf,'seat_1',1)
        print('\n座位2：',conf.items('seat_2'))
        if input('是否启用座位2?\n(Enter启用，n不启用):') != 'n':
            arr2 = seatW(conf, 'seat_2',1)
        else:
            arr2 = False

        print('\n座位3：',conf.items('seat_3'))
        if input('是否启用座位3?\n(Enter启用，n不启用):') != 'n':
            arr3 = seatW(conf, 'seat_3',1)
        else:
            arr3 = False

        conf.write(open("data.ini","w"))
        return [user, arr1, arr2, arr3]

    else:
        conf = configparser.ConfigParser()
        path = sys.path[0]+'/data.ini'
        conf.read(path)
        conf.add_section('user_set')
        main_url = 'http://ic.zju.edu.cn/ClientWeb/xcus/ic2/Default.aspx'
        rep = requests.get(main_url)
        cookies_w = {'ASP.NET_SessionId':rep.cookies['ASP.NET_SessionId']}
        conf.set("user_set","cookies",value=json.dumps(cookies_w))
        print('首次使用，请设置账户')
        uid = input('ID:')
        conf.set("user_set","user_id",value=uid)
        pwd = input('password:')
        os.system('cls')
        while (login([uid,pwd,cookies_w]) == False):
            uid = input('id:')
            pwd = input('pwd:')
        if input('是否保存密码(y/n)：') == 'y':
                conf.set("user_set","user_pwd",value=pwd)
        else:
            conf.set("user_set","user_pwd",value='000000')
        
        print('\n 设置座位1\n 建议设置为最常用座位(例如晚上):')
        seatW(conf, 'seat_1',2)
        os.system('cls')
        print('\n 设置座位2\n 第二常用座位:')
        seatW(conf, 'seat_2',2)
        os.system('cls')
        print('\n 设置座位3\n 第三常用座位:')
        seatW(conf, 'seat_3',2)
        os.system('cls')
        conf.write(open("data.ini","w"))
        return confDeal()

        
    

def seatW(conf,seatnum,c):
    if c == 1:
        date = str(datetime.date.today() + datetime.timedelta(days=2))
        start_time = conf.get(seatnum, 'rsv_st')
        end_time = conf.get(seatnum, 'rsv_ed')
        seat = conf.get(seatnum, 'seat_id')
        return [seat, date, start_time, end_time]
    elif c == 2:
        print('\n 首次使用,请进行设置:\n 时间格式：例如8:30写作0830\n 座位格式：例如F3-040\n')
        conf.add_section(seatnum)
        start_time = input('开始时间:')
        end_time = input('结束时间:')
        while veridate(start_time,end_time) == False:
            start_time = input('开始时间:')
            end_time = input('结束时间:')
        seat_source = input('座位:')
        seat_id = getSeatId(seat_source)
        while (seat_id == False):
            seat_source = input('座位:')
            seat_id = getSeatId(seat_source)
        conf.set(seatnum,"rsv_st",value=start_time)
        conf.set(seatnum,"rsv_ed",value=end_time)
        conf.set(seatnum,"seat_id",value=str(seat_id))
        conf.set(seatnum,"seat_name",value=str(seat_source))

# 登陆 1.判断是否登陆是返回T 2.登陆返回T 3.登陆失败返回F
def login(arr):
    # 先判断是否已经登陆
    judurl = 'http://ic.zju.edu.cn/ClientWeb/pro/ajax/login.aspx?act=is_login'
    repj = json.loads(requests.get(judurl, cookies=arr[2]).text)
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
        reply = json.loads(requests.post(url, cookies=arr[2], data=body).text)
        # 如果登陆成功
        if reply['msg'] == 'ok':
            print('\n 登陆成功')
            print('Welcome '+reply['data']['name']+'\n')
            return True
        # 失败重试
        else:
            print('登陆失败，请重试')
            return False


# 预约座位

def reserve(arr,user,num):
    url = 'http://ic.zju.edu.cn/ClientWeb//pro/ajax/reserve.aspx'
    seat = arr[0]
    date = arr[1]
    st = arr[2]
    et = arr[3]
    # url传入开始时间格式:2019-4-20 09:10
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
    if login(user):
        rep = requests.get(url, params=params, cookies=user[2])
        print(json.dumps(params, sort_keys=True, indent=4), '\n', rep.text)
        repj = json.loads(rep.text)
        logdate = time.strftime('%Y-%m-%d/:%H:%M:%S ', time.localtime(time.time()))
        rept = logdate + repj['msg'] + '\r\n'
        seat_file = open('logfile.log', 'a')
        seat_file.write(rept)
        if repj['msg'] == '操作成功！':
            seat_file.close()
        elif (repj['msg']).find('[1]'):
            time.sleep(1.5)
            reserve(arr,user,num)
        else:
            if num < 5:
                time.sleep(num*0.5)
                reserve(arr,user,num+1)
            else:
                print('尝试超过五次，不试了，下一个')



# 转换座位id
def getSeatId(seat):
    print('\n 寻找你的座位...')
    date = str(datetime.date.today())
    url = 'http://ic.zju.edu.cn/ClientWeb/pro/ajax/device.aspx'
    params = {'date': date,'act': 'get_rsv_sta'}
    rep = requests.get(url, params=params)
    content = json.loads(rep.text)
    seatObj = content['data']
    for obj in seatObj:
        if obj['title'] == seat:
            print('\n 校对你的座位信息:')
            retxt = '\n className: ' + str(obj['className'])+'   labName: ' + str(obj['labName'])+'   kindName: ' + str(obj['kindName'])+' devName: ' + str(obj['devName'])+'\n open_time: ' + '-'.join(obj['open'])+'   devId: ' + str(obj['devId'])
            print(retxt)
            if input('\n 是否确定？ y/n ') == 'y':
                return obj['devId']
    print('失败，请重试\n')
    return False


# 预约主体：获取sid、登陆、预约
def reserve_main():
    reserveArr = confDeal()
    user = reserveArr[0]
    seat = reserveArr[1]
    seat1 = reserveArr[2]
    seat2 = reserveArr[3]
    if login(user):
        print('\n  登陆成功...')
        time.sleep(2)
        os.system('cls')
        if SetTime():
            reserve(seat,user,0)
            if seat1 != False:
                reserve(seat1,user,0)
            if seat2 != False:
                reserve(seat2,user,0)


# 定时判断器只能提前一天——还未开放
def SetTime():
    print('定时器启动...')
    while True:
        now = time.strftime('%H:%M:%S', time.localtime(time.time()))
        nowm = time.strftime('%H:%M', time.localtime(time.time()))
        H = 24 - int(now.split(':')[0])
        M = int(now.split(':')[1])
        S = int(now.split(':')[2])
        sleepTime = H*3600-M*60-S
        if nowm == '00:00':
            return True
        elif H > 23:
            print('零点，抢座！')
            return True
        elif H > 1:
            sys.stdout.write('\r{0}'.format('待机时间：'+str(round(H-M/60,1) )+ ' 小时'))
            time.sleep(360)
            sys.stdout.flush()
        elif sleepTime > 99:
            sys.stdout.write('\r{0}'.format('待机时间：'+str(round(H*60-M-S/60,1)) + ' 分钟'))
            time.sleep(6)
            sys.stdout.flush()
        else:
            sys.stdout.write('\r{0}'.format('现在时间:'+now+'  待机时间：'+str(sleepTime)+ ' S'))
            time.sleep(1)
            sys.stdout.flush()

# 测试函数
def test():
    reserveArr = confDeal()
    user = reserveArr[0]
    seat = reserveArr[1]
    seat1 = reserveArr[2]
    seat2 = reserveArr[3]
    input(reserveArr)
    reserve(seat,user,0)
    if seat1 != False:
        reserve(seat1,user,0)
    if seat2 != False:
        reserve(seat2,user,0)

# 主函数
def main():
    input('\n*****************************************\n* 欢迎使用图书馆自动预约-这是自动模式   *\n*        软件可预约完成自动关机         *\n*****************************************\n*****************************************\n* -----提示：                           *\n* 1、确保电脑电源模式不会自动关机或待机 *\n* 2、在首次使用配置完成之后就能一路回车 *\n* 3、可通过删除配置文件重新设置         *\n*****************************************\n*****************************************\n*          Powered by wenz_xv           *\n*****************************************\n    Enter启动... ')
    ch = input('是否自动关机？ y/n ')
    os.system('cls')
    # 主进程
    reserve_main()

    if ch == 'y':
        print('30s 后关机 \n 你可以关闭程序来阻止\n')
        time.sleep(20)
        print('10s后关机，可能不太能阻止了...')
        os.system('shutdown -s -f -t 10')
    else:
        input()

# 验证
def encipher(ipt):
    hl = hashlib.md5()
    hl.update(ipt.encode(encoding='utf-8'))
    if hl.hexdigest() == 'bcedc450f8481e89b1445069acdc3dd9':
        return 1
    elif ipt == 'test':
        return 2

en = input('验证码：')
if encipher(en) == 1:
    os.system('cls')
    main()
elif encipher(en) == 2:
    os.system('cls')
    test()
    
