import requests,json,time,sys

def getJson():
    url = 'http://ic.zju.edu.cn/ClientWeb/pro/ajax/device.aspx'
    date = '2019-05-03'
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
    seat = input('search for seat:(press enter to get all seat)')
    if seat == 'wow':
        user = input('search for user:')
        newContent = user_fil_ter(content)
        user_lst = []
        for e in newContent:
            if e['owner'] == user:
                user_lst.append(e)
        if user_lst != []:
            return user_lst
        else:
            return 'Cannot find the user' 
    elif seat != '':
        for e in content:
            if e['title'] == seat:
                return fil_ter(e)
        else:
            return 'Cannot find the seat'
    else:
        newContent = []
        for e in content:
            if e['labId'] != '173':
                newContent.append(str(fil_ter(e)))
        data = '\n'.join(newContent)
        write(data)
        return 'write in seat.txt'
        

def fil_ter(obj):
    reobj = {
        'className':  obj['className'],
        'labName': obj['labName'],
        'kindName': obj['kindName'],
        'devName': obj['devName'],
        'open_time': '-'.join(obj['open']),
        'labId': obj['labId'],
        'devId': obj['devId'],
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


def write(data):
    seat_file = open('seat_info.txt','w')
    seat_file.write(data)
    seat_file.close()

print(chose())
