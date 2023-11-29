#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File     : spider.py
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
class Spider():
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

    def get_pic(self,name):
        name = self.remove_special_chars(name.split(".")[0])
        url = "https://image.baidu.com/search/index?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&fm=result&fr=&sf=1&fmq=1701236441873_R&pv=&ic=&nc=1&z=&hd=&latest=&copyright=&se=1&showtab=0&fb=0&width=&height=&face=0&istype=2&dyTabStr=MCwxLDMsMiw0LDYsNSw3LDgsOQ%3D%3D&ie=utf-8&sid=&word={}".format(name)
        self.driver.get(url)
        time.sleep(5)
        pic_url = self.parase_baidu_pic_serarch(name,self.driver.page_source)
        return pic_url


    def parase_baidu_pic_serarch(self,name,html):
        try:
            soup = BeautifulSoup(html, "lxml")
            elements = soup.select('.imgitem')
            max_score = 0
            max_score_element = None
            for element in elements:
                sim_score = self.similarity_str(name, element.text)
                if sim_score > max_score:
                    max_score = sim_score
                    max_score_element = element
            url = ""
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
            return url
        except Exception as e:
            with open("html/baidu_pic_{}.html".format(name),"wb") as f:
                f.write(html.encode("utf-8"))
            self.JadeLog.ERROR("百度图片爬虫失败,名称为:{},失败原因为:{}".format(name,e))