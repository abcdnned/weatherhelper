#coding: utf-8

from random import randint
import requests
from wxpy import *
from time import strftime
import time
import unicodedata

greeting2mom = False
doatlaunch = True

def wide_chars(s):
    return sum(unicodedata.east_asian_width(x) in ('F', 'W') for x in s)

def f2c(s):
    f = float(s)
    c = (f - 32) / 1.8
    return round(c)
    
daycn = dict({'Wed':'三', 'Thu':'四', 'Fri':'五', 'Sat':'六', 'Sun':'日', 'Mon':'一', 'Tue':'二'})
codecn = dict({'0':"龙卷风", '1':"热带风暴", '2':"飓风", '3':"强烈雷暴天气", '4':"雷暴天气", '5':"雨夹雪", '6':"冻雨", '7':"冰雹夹雪", '8':"冻毛雨", '9':"雾雨", '10':"冻雨", '11':"阵雨", '12':"阵雨", '13':"阵雪", '14':"小阵雪", '15':"高吹雪", '16':"雪", '17':"冰雹", '18':"冻雨", '19':"灰尘天气", '20':"有雾", '21':"薄雾", '22':"烟雾天气", '23':"大风", '24':"有风", '25':"冷", '26':"阴", '27':"多云", '28':"多云", '29':"局部多云", '30':"局部多云", '31':"天晴", '32':"晴朗", '33':"晴朗", '34':"晴朗", '35':"雨夹雹", '36':"热", '37':"局部风暴", '38':"零星风暴", '39':"零星风暴", '40':"局部阵雨", '41':"大雪", '42':"零星阵雪", '43':"大雪", '44':"少云", '45':"雷暴雨", '46':"阵雪", '47':"局部风暴"})
emo = dict({'0':"🌀", '1':"🌀", '2':"🌀", '3':"⚡", '4':"⚡", '5':"☔", '6':"☔", '7':"☔", '8':"☔", '9':"☔", '10':"☔", '11':"☔", '12':"☔", '13':"❄", '14':"❄", '15':"❄", '16':"❄", '17':"☔", '18':"☔", '19':"☁", '20':"☁", '21':"☁", '22':"☁", '23':"☁", '24':"☁", '25':"☁", '26':"☁", '27':"☁", '28':"☁", '29':"☁", '30':"☁", '31':"☀", '32':"☀", '33':"☀", '34':"☀", '35':"☔", '36':"☀", '37':"⚡", '38':"⚡", '39':"⚡", '40':"☔", '41':"❄", '42':"❄", '43':"❄", '44':"☁", '45':"⚡", '46':"❄", '47':"⚡"}) 

greetings = ["老妈，身体好吗？", "妈妈，今天血压怎么样？", "老妈，外婆好伐", "妈妈，今天好吗？"]
names = ['小珣', '我最牛', '彩霞']
location = ['2151849', '2151849', '2151849']
location_name = ['上海', '上海', '上海']
mt = 4
template = '{}号 周{}: {}{} {} ~ {} 摄氏度\n'
proxies = { 'https':'172.16.11.182:9090'}
def get_weather(ln, code):
    report = '{}天气\n'.format(ln)
    msg = requests.get('https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20weather.forecast%20where%20woeid={}&format=json&u=c'.format(code), proxies=proxies)
    j = msg.json()
    forecast = j['query']['results']['channel']['item']['forecast']
    for i in range(len(forecast)):
        data = forecast[i]
        code = data['code']
        date = data['date']
        low = data['low']
        high = data['high']
        text = data['text']
        day = data['day']
        f = template.format(date[:2], daycn[day], emo[code], codecn[code], f2c(low), f2c(high))
        report = report + f
    return report

bot = Bot()
baby = bot.friends().search('小珣')[0]
dady = bot.friends().search('我最牛')[0]
mom = bot.friends().search('彩霞')[0]

if doatlaunch :
    for i, name in enumerate(names):
        report = get_weather(location_name[i], location[i])
        target = bot.friends().search(name)[0]
        print(target.send(report))
    if greeting2mom :
        greeting = greetings[randint(0, len(greetings) - 1)]
        print(mom.send(greeting))

while True :
    h = strftime("%H")
    m = strftime("%M")
    print("hartbeat {}:{}".format(h, m))
    if h == '07':
        for i, name in enumerate(names):
            report = get_weather(location_name[i], location[i])
            target = bot.friends().search(name)[0]
            print(target.send(report))
    if greeting2mom and h == '15':
        greeting = greetings[randint(0, len(greetings) - 1)]
        print(mom.send(greeting))
    time.sleep(3600)
