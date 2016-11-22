# -*- coding: utf-8 -*-
import time
import urllib2
import xml.dom.minidom

# 开发者密钥:https://www.cn.kayak.com/labs/api/search
kayakkey='YOUR KEY HERE'

def getkayaksession():
  # 构造一个URL以开启一个对话
  url='http://www.kayak.com/k/ident/apisession?token=%s&version=1' % kayakkey
  
  # 解析返回的XML
  doc=xml.dom.minidom.parseString(urllib2.urlopen(url).read())
  
  # 找到 <sid>xxxxxxxx</sid>标签
  sid=doc.getElementsByTagName('sid')[0].firstChild.data
  return sid

def flightsearch(sid,origin,destination,depart_date):
  
  # 构造搜索用的URL
  url='http://www.kayak.com/s/apisearch?basicmode=true&oneway=y&origin=%s' % origin
  url+='&destination=%s&depart_date=%s' % (destination,depart_date)
  url+='&return_date=none&depart_time=a&return_time=a'
  url+='&travelers=1&cabin=e&action=doFlights&apimode=1'
  url+='&_sid_=%s&version=1' % (sid)

  # 得到XML
  doc=xml.dom.minidom.parseString(urllib2.urlopen(url).read())

  # 提取搜索用的ID
  searchid=doc.getElementsByTagName('searchid')[0].firstChild.data

  return searchid

def flightsearchresults(sid,searchid):
  # 删除开头的$和逗号，并把数字转化成浮点类型
  def parseprice(p): 
    return float(p[1:].replace(',',''))

  # 遍历检测
  while 1:
    time.sleep(2)

    # 构造检测用的URL
    url='http://www.kayak.com/s/basic/flight?'
    url+='searchid=%s&c=5&apimode=1&_sid_=%s&version=1' % (searchid,sid)
    doc=xml.dom.minidom.parseString(urllib2.urlopen(url).read())

    # 寻找 morepending 标签，并等待其不再为true
    morepending=doc.getElementsByTagName('morepending')[0].firstChild
    if morepending==None or morepending.data=='false': break

  # 下载完整列表
  url='http://www.kayak.com/s/basic/flight?'
  url+='searchid=%s&c=999&apimode=1&_sid_=%s&version=1' % (searchid,sid)
  doc=xml.dom.minidom.parseString(urllib2.urlopen(url).read())

  # 得到不同元素组成的列表
  prices=doc.getElementsByTagName('price')
  departures=doc.getElementsByTagName('depart')
  arrivals=doc.getElementsByTagName('arrive')  

  # 用zip连接到一起
  return zip([p.firstChild.data.split(' ')[1] for p in departures],
             [p.firstChild.data.split(' ')[1] for p in arrivals],
             [parseprice(p.firstChild.data) for p in prices])


def createschedule(people,dest,dep,ret):
  # 得到搜索用的会话id
  sid=getkayaksession()
  flights={}
  
  for p in people:
    name,origin=p
    # 去程航班
    searchid=flightsearch(sid,origin,dest,dep)
    flights[(origin,dest)]=flightsearchresults(sid,searchid)
    
    # 返程航班
    searchid=flightsearch(sid,dest,origin,ret)
    flights[(dest,origin)]=flightsearchresults(sid,searchid)
    
  return flights
