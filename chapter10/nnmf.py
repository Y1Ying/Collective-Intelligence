# -*- coding: utf-8 -*-
from numpy import *

def difcost(a,b):
  dif=0
  # 遍历矩阵中的每一行和每一列
  for i in range(shape(a)[0]):
    for j in range(shape(a)[1]):
      # 将差值相加
      dif+=pow(a[i,j]-b[i,j],2)
  return dif

def factorize(v,pc=10,iter=50):
  ic=shape(v)[0]
  fc=shape(v)[1]

  # 以随机值初始化权重矩阵和特征矩阵
  w=matrix([[random.random() for j in range(pc)] for i in range(ic)])
  h=matrix([[random.random() for i in range(fc)] for i in range(pc)])

  # 最多执行Iter次操作
  for i in range(iter):
    wh=w*h
    
    # 计算当前差值
    cost=difcost(v,wh)
    
    if i%10==0: print cost
    
    # 如果矩阵已分解彻底，则立即终止
    if cost==0: break
    
    # 更新特征矩阵
    hn=(transpose(w)*v)
    hd=(transpose(w)*w*h)
  
    h=matrix(array(h)*array(hn)/array(hd))

    # 更新权重矩阵
    wn=(v*transpose(h))
    wd=(w*h*transpose(h))

    w=matrix(array(w)*array(wn)/array(wd))  
    
  return w,h

