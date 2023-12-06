#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File     : chrome_spider.py
# @Author   : jade
# @Date     : 2023/11/29 9:33
# @Email    : jadehh@1ive.com
# @Software : Samples
# @Desc     :
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from difflib import SequenceMatcher  # 导入库
import re
from jade import getOperationSystem,JadeLogging
from bs4 import BeautifulSoup
import requests
import copy
from src.vod import VodDetail,VodShort
import json
class ChromeSpider():
    def __init__(self):
        if getOperationSystem() == "Windows":
            chrome_path = r"C:\Users\Administrator\AppData\Local\Google\Chrome\Application\chrome.exe"
            driver_path = r"C:\Users\Administrator\Downloads\chromedriver-win64\chromedriver.exe"
        elif getOperationSystem() == "Linux":
            chrome_path = "/usr/bin/google-chrome"
            driver_path = "/usr/bin/chromedriver"
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # 无头
        options.add_argument("--disbale-gpu")  # 无gpu图形化界面
        options.add_argument('--no-sandbox')
        options.binary_location = chrome_path
        options.binary_location = chrome_path
        chrome_driver_service = Service(driver_path)
        self.driver = webdriver.Chrome(options=options,service=chrome_driver_service)
        self.JadeLog = JadeLogging("/tmp/",Level="INFO")
        self.driver.implicitly_wait(10)
        self.douban_home_url = 'https://m.douban.com'
        self.header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"}

    def get(self):

        pass

    def similarity_str(self,a, b):
        return SequenceMatcher(None, a, b).ratio()

    def remove_special_chars(self,text):
        pattern = r'[^\w\s]'  # 定义要删除的特殊字符规则
        result = re.sub(pattern, '', text)  # 使用re.sub函数将特殊字符替换为空格或其他指定内容
        return result


    def release(self):
        self.driver.close()
        self.JadeLog.release()

    def get_pic_by_baidu(self,name):
        name = self.remove_special_chars(name.split(".")[0])
        url = "https://image.baidu.com/search/index?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&fm=result&fr=&sf=1&fmq=1701236441873_R&pv=&ic=&nc=1&z=&hd=&latest=&copyright=&se=1&showtab=0&fb=0&width=&height=&face=0&istype=2&dyTabStr=MCwxLDMsMiw0LDYsNSw3LDgsOQ%3D%3D&ie=utf-8&sid=&word={}".format(name)
        pic_url = "https://gh.con.sh/https://raw.githubusercontent.com/jadehh/TV/py/jpg/ali.jpg"
        try:
            self.driver.get(url)
            time.sleep(2)
            pic_url = self.parase_baidu_pic_serarch(name,self.driver.page_source)
            return pic_url
        except Exception as e:
            self.JadeLog.ERROR("百度图片爬虫失败,{}".format(e))
            return pic_url

    def parase_baidu_pic_serarch(self,name,html):
        try:
            soup = BeautifulSoup(html, "lxml")
            elements = soup.select('.imgitem')
            max_score = 0
            max_score_element = None
            for element in elements:
                sim_score = self.similarity_str(name + "海报", element.text)
                if sim_score > max_score:
                    max_score = sim_score
                    max_score_element = element
            url = "https://gh.con.sh/https://raw.githubusercontent.com/jadehh/TV/py/jpg/ali.jpg"
            try:
                if "data-thumburl" in max_score_element.attrs.keys():
                    url = max_score_element.attrs["data-thumburl"]
                    self.JadeLog.INFO("正在爬虫百度图片,名称为:{},图片地址为:{}".format(name, url))
                else:
                    url = max_score_element.select(".rsbox-imgwarp")[0].find("img").attrs["src"]
                    self.JadeLog.WARNING("正在爬虫百度图片,没有找到原图,名称为:{},图片地址为:{}".format(name, url))
            except Exception as e:
                with open("html/baidu_pic_{}.html".format(name), "wb") as f:
                    f.write(html.encode("utf-8"))
                self.JadeLog.ERROR("百度图片爬虫失败,名称为:{},失败原因为:{}".format(name, e))
        except Exception as e:
            with open("html/baidu_pic_{}.html".format(name),"wb") as f:
                f.write(html.encode("utf-8"))
            self.JadeLog.ERROR("百度图片爬虫失败,名称为:{},失败原因为:{}".format(name,e))
        return url

    def parseVodListFromSoup(self, soup):
        elements = soup.find_all("li",{"class":"search-module"})
        vod_list = []
        other_type_list = ["小组"]
        for element in elements:
            type = element.find("span",{"class":"search-results-modules-name"}).text
            if type not in other_type_list:
                vod_short = VodShort()
                vod_short.vod_id = element.find("a").attrs["href"]
                vod_short.vod_pic = element.find("img").attrs["src"]
                vod_short.vod_name = element.find("span",{"class":"subject-title"}).text
                rating = element.find("p",{"class":"rating"}).text.replace("\n","")
                if "暂无" in rating:
                    pass
                else:
                    vod_short.vod_remarks = "评分:{}".format(rating)
                vod_list.append(vod_short)
        return vod_list



    def get_douban_vod_short_search(self, key):
        url = "{}/search/?query={}".format(self.douban_home_url, key)
        headers = copy.copy(self.header)
        headers["Host"] = "m.douban.com"
        rsp = requests.get(url, headers=headers,allow_redirects=False)
        if rsp.status_code == 200:
            soup = BeautifulSoup(rsp.text, "lxml")
            vod_list = self.parseVodListFromSoup(soup)
            return vod_list
        else:
            #self.JadeLog.ERROR("豆瓣爬虫搜索失败,准备重新爬虫")
            time.sleep(2)
            return self.get_douban_vod_short_search(key)
    def paraseVodDetailFromSoup(self, soup):
        vod_detail = VodDetail()
        info_list = soup.find('div', attrs={'id': "info"}).text.split("\n")
        for item in info_list:
            if "地区" in item:
                vod_detail.vod_area = item.split(":")[-1]
        dic = json.loads(soup.find("script", {'type': 'application/ld+json'}).text.replace("\n", ""))
        vod_detail.vod_id = dic["url"]
        vod_detail.vod_name = dic["name"]
        vod_detail.vod_pic = dic["image"]
        vod_detail.vod_year = dic["datePublished"]
        actor_list = []
        for actor_dic in dic["actor"]:
            actor_list.append(actor_dic["name"].split(" ")[0])
        director_list = []
        for director_dic in dic["director"]:
            director_list.append(director_dic["name"].split(" ")[0])
        vod_detail.type_name = " / ".join(dic["genre"])
        vod_detail.vod_actor = " / ".join(actor_list)
        vod_detail.vod_director = " / ".join(director_list)
        vod_detail.vod_content = dic["description"]
        vod_detail.vod_remarks = "评分:{}".format(dic["aggregateRating"]["ratingValue"])
        return vod_detail

    def get_douban_vod_detail(self, v_id):
        split_list = v_id.split("/")
        type_id = split_list[1]
        tid = "/" + "/".join(split_list[2:])
        home_url_list = self.douban_home_url.split(".")
        home_url_list[0] = "https://{}".format(type_id)
        home_url = ".".join(home_url_list)
        url = home_url + tid
        headers = {}
        headers["Host"] = "movie.douban.com"
        headers[
            "Cookie"] = '_vwo_uuid_v2=DC67E58994652304E348D0E1EB30417A8|79da2360b16aba794ae2f050599037c0; ap_v=0,6.0; __yadk_uid=5OCVRPW39vyo5ubib5dVA4mvIjFLOBzR; __utma=30149280.1972142145.1701828581.1701828603.1701828603.1; __utmb=30149280.0.10.1701828603; __utmc=30149280; __utmz=30149280.1701828603.1.1.utmcsr=m.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; _ga_Y4GN1R87RG=GS1.1.1701828581.1.1.1701828602.0.0.0; __utma=223695111.1972142145.1701828581.1701828603.1701828603.1; __utmb=223695111.0.10.1701828603; __utmc=223695111; __utmz=223695111.1701828603.1.1.utmcsr=m.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; _pk_id.100001.4cf6=eb516fe88d50a169.1701828603.; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1701828603%2C%22https%3A%2F%2Fm.douban.com%2F%22%5D; _pk_ses.100001.4cf6=1; _ck_desktop_mode=1; vmode=pc; _ga=GA1.2.1972142145.1701828581; _gid=GA1.2.1067754563.1701828581; ll="118159"; bid=mAFuUX1zgPI'
        headers[
            "User-Agent"] = "Mozilla/5.0 (iPhone; CPU iPhone OS 16_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/100.0.4896.77 Mobile/15E148 Safari/604.1"
        rsp = requests.get(url, headers=headers,allow_redirects=False)
        if rsp.status_code == 200:
            soup = BeautifulSoup(rsp.text, "lxml")
            vod_detail = self.paraseVodDetailFromSoup(soup)
        else:
            #self.JadeLog.ERROR("豆瓣爬虫详情失败,准备重新爬虫")
            time.sleep(2)
            return self.get_douban_vod_detail(v_id)
        return vod_detail


    def get_douban_vod_detail_by_name(self,name):
        self.JadeLog.INFO("正在进行豆瓣爬虫,名称为:{}".format(name), True)
        try:
            vod_short_list = self.get_douban_vod_short_search(name)
            if len(vod_short_list) > 0:
                vod_detail = self.get_douban_vod_detail(vod_short_list[0].vod_id)
                return vod_detail
            else:
                #self.JadeLog.ERROR("名称为:{},豆瓣爬虫失败".format(name))
                return None
        except Exception as e:
            #self.JadeLog.ERROR("豆瓣爬虫失败,失败原因为:{}".format(e))
            return self.get_douban_vod_detail_by_name(name)