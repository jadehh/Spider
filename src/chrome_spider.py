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

    def get_vod_by_douban(self,name):
        url = "https://m.douban.com/search/?query={}".format(key)
        self.logger.info("搜索url地址为:{}".format(url))
        headers = {"Host": "frodo.douban.com",
                  "Connection": "Keep-Alive",
                  "Referer": "https://servicewechat.com/wx2f9b06c1de1ccfca/84/page-frame.html",
                  "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat"
                  }
        headers["Host"] = "m.douban.com"
        rsp = requests.get(url,headers=headers)
        vod_list = self.parase_douban_vod_search(rsp)
        return vod_list[0]

    def parase_douban_vod_search(self,rsp):
        soup = BeautifulSoup(rsp.text,"lxml")
        elements = soup.find_all("li")[1:-2]
        vod_list = []
        for element in elements:
            vod_short = VodShort()
            vod_short.vod_id = element.find("a").attrs["href"]
            vod_short.vod_pic = element.find("img").attrs["src"]
            span_elements = element.find_all("span")
            vod_short.vod_name = span_elements[0].text
            vod_short.vod_remarks = "评分:{}".format(span_elements[-1].text)
            vod_list.append(vod_short.to_dict())
        return vod_list

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
