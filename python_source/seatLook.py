import requests,json,time,sys

def getJson():
    url = 'http://ic.zju.edu.cn/ClientWeb/pro/ajax/device.aspx'
    date = getDate()
    params ={
        'date':date,
        'act':'get_rsv_sta'
    }
    rep = requests.get(url,params = params)
    content = json.loads(rep.text)
    return content['data']

def getDate():
    now = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    return now

def chose():
    content = getJson()
    seat = input('search for seat:')
    if seat != '':
        for e in content:
            if e['title'] == seat:
                return e
    else:
        return content



def main():
    seatData = chose()
    stdout_backup = sys.stdout
    log_file = open('log_file.log','w')
    sys.stdout = log_file
    print(seatData)
    log_file.close()
    sys.stdout = stdout_backup

main()