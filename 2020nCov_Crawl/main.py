import requests
import json
import datetime

headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'
}
url_token = 'https://api.weixin.qq.com/cgi-bin/token?'
nCov1 = "https://lab.isaaclin.cn/nCoV/api/overall"
nCov2 = "https://lab.isaaclin.cn/nCoV/api/area?latest=1&province="
send_api = 'https://api.weixin.qq.com/cgi-bin/message/template/send?access_token='



def getLatest():
    try:
        r = requests.get(nCov1, headers=headers)
        data = r.json()["results"]
        confirm = data[0]["confirmedCount"]
        suspect = data[0]["suspectedCount"]
        cured = data[0]["curedCount"]
        dead = data[0]["deadCount"]
        res = "已有"+str(confirm)+"人感染,"+ str(suspect) + "人怀疑感染," + "死亡/治愈人数：" + str(dead) + "/" + str(cured)
    except:
        res = "丁香数据接口出现问题..."
    return res

def getProvince(s):
    try:
        r = requests.get(nCov2 + s, headers=headers)
        data = r.json()["results"]
        s = data[0]["cities"]
        res = ""
        if len(s) > 8:
            l = len(s) - 8
            for i in range(l):
                res = res + s[i]["cityName"] + ":" + str(s[i]["confirmedCount"]) + ","
        else:
            res = "数据更新中...."
        print(res)
    except:
        res = "省内数据接口有问题"
        print(res)
    return res

def getWeather(s):
    try:
        url = 'http://t.weather.sojson.com/api/weather/city/' + s
        r = requests.get(url, headers=headers)
        r.encoding = 'utf-8'
        data = r.json()
        city = data["cityInfo"]["city"]
        tmp = data["data"]["forecast"][0]
        weather = tmp["type"]
        high = tmp["high"]
        low = tmp["low"]
        sunrise = tmp["sunrise"]
        sunset = tmp["sunset"]
        notice = tmp["notice"]
        aqi = tmp["aqi"]

        res = city + "今日:" + weather + "," + high + "/" + low
    except:
        res = "天气接口有问题"
    return res


def getdays():
    dict = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    day = datetime.datetime.now().day

    if year%4 == 0 and year%100 != 0 or year%400 == 0:
        total = 366.0
        dict[2] = 29
    else:
        total = 365.0

    cnt = dict[month-1] + day
    per = cnt / total
    len = 40
    bar = '['
    for i in range(len):
        if i < int(len*per): bar += '#'
        else: bar += ' '
    bar += ']'
    bar = bar + " " + str(cnt) + "/" + str(int(total))
    res = str(round(per*100, 2)) + "%"
    return bar, res

def send_template(s1, s2, wuhu, chengdu, bar, h):
    res = requests.get(url=url_token,
                       params={
                         "grant_type": 'client_credential',
                         'appid':'', # appid
                         'secret':'', # secret
                       }, headers=headers).json()
    print(res)
    token = res.get('access_token')

    # 发送消息
    openID= [] # openid
    URL = send_api + str(token)
    for i in range(len(openID)):
        send_data = {
                   "touser":openID[i],
                   "template_id":"",
                   "data":{
                           "s1": {
                               "value": s1,
                               "color":"#000000"
                           },
                       "s2": {
                           "value": s2,
                           "color": "#000000"
                       },
                       "wuhu": {
                           "value": wuhu,
                           "color": "#1E90FF"
                       },
                       "chengdu": {
                           "value": chengdu,
                           "color": "#708090"
                       },
                       "res": {
                           "value": h,
                           "color": "#CD5C5C"
                       },
                       "bar": {
                           "value": bar,
                           "color": "#173177"
                       },
                   }
               }

        send_data = json.dumps(send_data)
        print(send_data)
        res =requests.post(url=URL, data=send_data, headers=headers)
        if res.json()["errcode"] != 0: print("Error in Sending Template")

if __name__ == "__main__":
    s1 = getLatest()
    s2 = getProvince("安徽省")
    # 成都：101270101
    # 芜湖：101220301
    wuhu = getWeather("101220301")
    chengdu = getWeather("101270101")
    bar, res = getdays()
    send_template(s1, s2, wuhu, chengdu, bar, res)






