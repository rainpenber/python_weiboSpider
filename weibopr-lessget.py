# -*- coding: utf-8 -*-
import re
# import string
import sys
import os
import random
# import urllib
# import urllib2
# from bs4 import BeautifulSoup
import requests
from lxml import etree
import traceback
import time
import codecs
import importlib


class weibo:
    # cookie需替换成本人的！
    #角川烈的 已经过期
    cookie = {
         'Cookie': '_T_WM=b8058f6f221a847c4b0a1376761bf16f; ALF=1555087138; SCF=AmVBQxD_b1_B2ZTqO58annp7rxHqFFQxmEG29OeC2KPU5VQpwsH2Hv0N85fxkAKlEChLA4t8cfrrkVLHkVxfBVM.; SUB=_2A25xjtBJDeRhGeNM61IT-SzFwzyIHXVTcPABrDV6PUJbktAKLVLNkW1NTloX7DGpdIMepxbBg-I0HReg5_TCrPQB; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhbdKyAGyMu6e4e70S9xa5y5JpX5K-hUgL.Fo-Eeh5E1Kz41h52dJLoI0YLxK-LBKeLB-zLxK-LBKBL1-2LxK-L1K-LBKBLxKqLBKzLBKnLxKqLB.eL1hzLxKqLBo-LB--LxKML1heL1hnt; SUHB=09PNIxB2GhSk50; SSOLoginState=1552588825'}
    #我的
    # cookie = {
    #      'Cookie': '_T_WM=4803db0e20cc23aca76d6d82e67f4ede; ALF=1555147565; SCF=AkGB_lGNNOAZX3THtsXCl3N54q8Bmc9eh3Rx68vELq_GBaFESkC3idcTfuVB01Nx4MliyYM9GWQczKnmrBdiq5Y.; SUB=_2A25xjm59DeRhGeFO6VIX8ynOyz-IHXVTcXI1rDV8PUJbkNANLXnzkW1NQZayLnjyL6ykgonmzp5UW1xmmx0g8Dv6; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFIsaeww1mzHBwMKqfl7CxH5JpX5oz75NHD95QNehz7SoeNeo50Ws4Dqcjkxs84MEH8SE-4BC-RSFH8SCHFeF-RxbH81C-4BbHW15tt; SUHB=0sqx68mRmLnFHb; SSOLoginState=1552543448'}
    # cookie = {
    #     'Cookie': '_T_WM=895f154bb45c806a94eeaf7b018b4305; ALF=1548851546; SCF=Ag5kkvZQykmazulxfh5RQhCKT0OYudxQqfK_EMxj0krZcONynSlpX1Fc5U3pDir1haP5X2n-_yvBB1PkQVTz8Ns.; SUB=_2A25xLnwMDeRhGeVP7lAY8y3EzTyIHXVS0QRErDV6PUNbktAKLWjYkW1NTOasSwijAzTFFUA4X0Np_uCdLbS25H5X; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WF3nTRVeAZF9Ln3yKMkVU1N5JpX5KMhUgL.FoepSKz4e0eRSo52dJLoIEXLxK-L12-L1-qLxK-LB-BL1K5LxKBLBonL12-LxKqL1KnL1-qLxKMLBoeLB.zt; SUHB=09P9CNvMah6QYo; SSOLoginState=1546259548'}


    # weibo类初始化
    def __init__(self, user_id, filter=0):
        self.user_id = user_id
        self.filter = filter  # 取值范围为0、1，程序默认值为0，代表要爬取用户的全部微博，1代表只爬取用户的原创微博
        self.weiboNum = 0  # 用户全部微博数
        self.weiboNum2 = 0  # 爬取到的微博数
        self.following = 0  # 用户关注数
        self.followers = 0  # 用户粉丝数
        self.weibos = []  # 微博内容
        self.num_zan = []  # 微博对应的点赞数
        self.num_forwarding = []  # 微博对应的转发数
        self.num_comment = []  # 微博对应的评论数
        self.pr = 0  # 用户的pagerank值

    # 获取微博数、关注数、粉丝数
    def getUserInfo(self):
        try:
            url = 'http://weibo.cn/u/%d?filter=%d&page=1' % (self.user_id, self.filter)
            html = requests.get(url, cookies=weibo.cookie).content
            selector = etree.HTML(html)
            pattern = r"\d+\.?\d*"  # 一堆数字，有或者没有的.，一个[0,9]数字

            # 微博数
            str_wb = selector.xpath("//div[@class='tip2']/span[@class='tc']/text()")[0]
            guid = re.findall(pattern, str_wb, re.S | re.M)
            for value in guid:
                num_wb = int(value)
                break
            self.weiboNum = num_wb
            print('微博数: ' + str(self.weiboNum))

            # 关注数
            str_gz = selector.xpath("//div[@class='tip2']/a/text()")[0]
            guid = re.findall(pattern, str_gz, re.M)
            self.following = int(guid[0])
            print('关注数: ' + str(self.following))

            # 粉丝数
            str_fs = selector.xpath("//div[@class='tip2']/a/text()")[1]
            guid = re.findall(pattern, str_fs, re.M)
            self.followers = int(guid[0])
            print('粉丝数: ' + str(self.followers))
        except Exception as e:
            print("Error: ", e)
            traceback.print_exc()


    def getPR(self):
        sum_zan = sum(self.num_zan)
        sum_forwarding = sum(self.num_forwarding)
        sum_comment = sum(self.num_comment)
        self.pr = self.followers * 0.01 + (sum_zan + sum_forwarding * 100 + sum_comment * 30) * 1.0 / (
                    self.weiboNum2 + 1)

        # 主程序

    def start(self):
        try:
            weibo.getUserInfo(self)
            # weibo.getWeiboInfo(self)
            weibo.getPR(self)
            print('信息抓取完毕')
            print('==================================')
        except Exception as e:
            print("Error: ", e)

        # 将爬取的信息写入文件

    def writeTxt(self):
        try:

            result = str(self.user_id) + ' ' + str(self.weiboNum) + ' ' + str(self.following) + ' ' + str(
                self.followers) + ' '
            with open('result/result.txt', 'a+') as f:
                f.write(result + '\n')
                f.close()
        except Exception as e:
            print("Error: ", e)
            traceback.print_exc()


# 使用
if os.path.isdir('result') == False:
    os.mkdir('result')
head_text = 'UID 微博数 关注数 粉丝数 '

print(head_text + 'is written')

with open("hkl_fans_List_part2.txt", "r") as read_f:
    try:
        for current_id in read_f.readlines():
            if current_id == '':
                break
            try:
                user_id = int(current_id)  # 另一个是：5984336074 2766134004
                # user_pr = {}  # 存储用户的pr值，用来判断用户的影响力，pr值越大代表影响力越高
                filter = 0

                wb = weibo(user_id, filter)
                wb.start()  # 爬取微博信息
                # user_pr[i] = wb.pr
                wb.writeTxt()
                print('id为' + current_id + '的用户的pr值为：' + str(wb.pr))
                t = random.randint(1, 3)
                print("休眠时间为:{}s".format(t))
                time.sleep(t)
            except Exception as e:
                print(e)
                traceback.print_exc()
    except Exception as e:
        print(e)

file_path = os.getcwd() + "/result/result.txt"
print('微博写入文件完毕，保存路径%s' % (file_path))
