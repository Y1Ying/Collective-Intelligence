# -*- coding: utf-8 -*-
import urllib2
import xml.dom.minidom

api_key='479NUNJHETN'

def getrandomratings(c):
  # 为getRandomProfile构造URL
  url="http://services.hotornot.com/rest/?app_key=%s" % api_key
  url+="&method=Rate.getRandomProfile&retrieve_num=%d" % c
  url+="&get_rate_info=true&meet_users_only=true"
  
  f1=urllib2.urlopen(url).read()

  doc=xml.dom.minidom.parseString(f1)
  
  emids=doc.getElementsByTagName('emid')
  ratings=doc.getElementsByTagName('rating')

  # 将emids 和 ratings 组合到一个列表中
  result=[]
  for e,r in zip(emids,ratings):
    if r.firstChild!=None:
      result.append((e.firstChild.data,r.firstChild.data))
  return result

stateregions={'New England':['ct','mn','ma','nh','ri','vt'],
              'Mid Atlantic':['de','md','nj','ny','pa'],
              'South':['al','ak','fl','ga','ky','la','ms','mo',
                       'nc','sc','tn','va','wv'],
              'Midwest':['il','in','ia','ks','mi','ne','nd','oh','sd','wi'],
              'West':['ak','ca','co','hi','id','mt','nv','or','ut','wa','wy']}

def getpeopledata(ratings):
  result=[]
  for emid,rating in ratings:
    # 对应于 MeetMe.getProfile 方法调用的URL
    url="http://services.hotornot.com/rest/?app_key=%s" % api_key
    url+="&method=MeetMe.getProfile&emid=%s&get_keywords=true" % emid

    # 得到所有关于此人的详细信息
    try:
      rating=int(float(rating)+0.5)
      doc2=xml.dom.minidom.parseString(urllib2.urlopen(url).read())
      gender=doc2.getElementsByTagName('gender')[0].firstChild.data
      age=doc2.getElementsByTagName('age')[0].firstChild.data
      loc=doc2.getElementsByTagName('location')[0].firstChild.data[0:2]

      # 将洲转换成地区
      for r,s in stateregions.items():
        if loc in s: region=r

      if region!=None:
        result.append((gender,int(age),region,rating))
    except:
      pass
  return result

