
from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random
import http.client, urllib
import re

today = datetime.now()
start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]

def get_weekday(today):
  week_list = ["星期一","星期二","星期三","星期四","星期五","星期六","星期日"]
  weeekday = week_list[today.weekday()]
  return weeekday

def get_weather():
  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
  res = requests.get(url).json()
  weather = res['data']['list'][0]
  return weather['weather'],math.floor(weather['low']),math.floor(weather['high'])

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_words():
  conn = http.client.HTTPSConnection('api.tianapi.com')  #接口域名
  params = urllib.parse.urlencode({'key':'301692a6922f4900e61059a683cdaf81'})
  headers = {'Content-type':'application/x-www-form-urlencoded'}
  conn.request('POST','http://api.tianapi.com/one/index',params,headers)
  res = conn.getresponse()
  data = res.read()
  a = data.decode('utf-8')
  req = re.findall(r'"word":"(.*?)","wordfrom"',a)[0]
  return req

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
day = str(today.year)+'年'+str(today.month)+'月'+str(today.day)+'日'+'  '+ get_weekday(today)
wea, low, high = get_weather()

data = {"date":{"value":day},
        "city":{"value":city},
        "weather":{"value":wea},
        "low":{"value":low},
        "high":{"value":high},
        "love_days":{"value":get_count()},
        #"birthday_left":{"value":get_birthday()},
        "words":{"value": get_words(), "color":get_random_color()}
        }
res = wm.send_template(user_id, template_id, data)
print(res)
