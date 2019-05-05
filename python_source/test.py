import requests,json

judurl = 'http://ic.zju.edu.cn/ClientWeb/pro/ajax/login.aspx?act=is_login'
repj = json.loads(requests.get(judurl).text)
input(repj)
if repj['ret'] == 0:
    input('ys')