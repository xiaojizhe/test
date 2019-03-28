# coding:utf-8

import requests
from selenium import webdriver
from bs4 import BeautifulSoup
import re,time

# firefox浏览器配置文件地址
profile_directory=r"C:\Users\Administrator\AppData\Roaming\Mozilla\Firefox\Profiles\xnmbssgw.default"
# 新建session
s=requests.sessions()
url="https://home.cnblogs.com/u/yoyoketang"

def get_cookies(url):
    '''启动selenium获取登录的cookies'''
    try:
        profile=webdriver.FirefoxProfile(profile_directory) #加载配置文件
        #启动浏览器配置
        driver=webdriver.Firefox(profile)
        driver.get(url+"/followers")
        time.sleep(3)
        cookies=driver.get_cookies() #获取浏览器cookies
        print(cookies)
        driver.quit()
    except Exception as msg:
        print(u"启动浏览器报错了:%s" % str(msg))

def add_cookies(cookies):
    '''往session里面添加cookies'''
    try:
        #添加cookies到CookieJar
        c = requests.cookies.RequestsCookieJar()
        for i in cookies:
            c.set(i["name"], i["value"])
        s.cookies.update(c)  #更新session里面的cookies
    except Exception as msg:
        print(u"添加cookies的时候报错了：%s" % str(msg))

def get_ye_nub(url):
    '''获取粉丝的页面数量'''
    try:
        r1=s.get(url+"/relation/followers")
        soup=BeautifulSoup(r1.content,"html.parser")
        #抓取我的粉丝数
        fensinub=soup.find_all(class_="current_nav")
        print(fensinub[0].string)
        num=re.findall(u"我的粉丝\((.+?)\)",fensinub[0].sstring)
        print("我的粉丝数量：%s" % str(num[0]))

        #计算有多少页，每页45条)
        ye=int(int(num[0])/45)+1
        print(u"总共分页数：%s" % str(ye))
        return ye
    except Exception as msg:
        print(u"获取粉丝页数报错了，默认返回数量1：%s" % str(msg))
        return 1

def sava_name(nub):
    '''抓取页面的粉丝名称'''
    try:
        if nub<=1:    #抓取第一页的数据
            url_page=url+"/relation/followers"
        else:
            url_page=url+"/relation/followers?page=%s" % str(nub)

    print("正在抓取的页面：%s" %url_page)
    r2=s.get(url_page,verify=False)
    soup=BeautifulSoup(r2.content,"html.parser")
    fensi=soup.find_all(class_="avatar_name")
    for i in fensi:
        name=i.string.replace("\n","").replace(" ","")
        print(name)
        with open("name.txt", "a", encoding="utf-8") as f: #追加写入
            f.write(name+"\n")
if __name__=="__main__":
    cookies=get_cookies(url)
    add_cookies(cookies)
    n=get_ye_nub(url)
    for i in list(range(1,n+1)):
        sava_name(i)
















