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
from datetime import datetime
from urllib import parse
import base64
import hmac
import hashlib
from urllib3.exceptions import InsecureRequestWarning
import urllib3
urllib3.disable_warnings(InsecureRequestWarning)
from random import choice

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
        self.session = requests.session()
        self.index = 1
        self._user_agents = [
        "api-client/1 com.douban.frodo/7.22.0.beta9(231) Android/23 product/Mate 40 vendor/HUAWEI model/Mate 40 brand/HUAWEI  rom/android  network/wifi  platform/AndroidPad"
        "api-client/1 com.douban.frodo/7.18.0(230) Android/22 product/MI 9 vendor/Xiaomi model/MI 9 brand/Android  rom/miui6  network/wifi  platform/mobile nd/1",
        "api-client/1 com.douban.frodo/7.1.0(205) Android/29 product/perseus vendor/Xiaomi model/Mi MIX 3  rom/miui6  network/wifi  platform/mobile nd/1",
        "api-client/1 com.douban.frodo/7.3.0(207) Android/22 product/MI 9 vendor/Xiaomi model/MI 9 brand/Android  rom/miui6  network/wifi platform/mobile nd/1"]

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

    def paraseVodDetailFromJson(self, dic):
        vodDetail = VodDetail()
        vodDetail.vod_name = dic["title"]
        vodDetail.vod_year = dic["year"]
        vodDetail.vod_pic = dic["pic"]["large"]
        vodDetail.vod_remarks = "评分:{}".format(dic["rating"]["value"])
        vodDetail.vod_content = dic["intro"]
        vodDetail.vod_area = " / ".join(dic["countries"])
        director_list = []
        for director_dic in dic["directors"]:
            director_list.append(director_dic["name"])
        actor_list = []
        for actor_dic in dic["actors"]:
            actor_list.append(actor_dic["name"])
        vodDetail.vod_director = " / ".join(director_list)
        vodDetail.vod_actor = " / ".join(actor_list)
        vodDetail.type_name = " / ".join(dic["genres"])
        return vodDetail

    def paraseVodShortFromJson(self,key,dic):
        items = dic["items"]
        if len(items) > 0:
            vod_short = VodShort()
            target = items[0]["target"]
            vod_short.vod_name = target["title"]
            vod_short.vod_id = "/" + "/".join(target["uri"].split("/")[-2:])
            vod_short.vod_pic = target["cover_url"]
            vod_short.vod_remarks = "评分:{}".format(target["rating"]["value"])
            return vod_short
        else:
            self.JadeLog.ERROR("豆瓣搜索失败,名称为:{},失败原因为:{}".format(key, "没有搜索到该名称"))
            return None


    def sign(self, url: str, ts: int, method='GET') -> str:
        """
        签名
        """
        _api_secret_key = "bf7dddc7c9cfe6f7"
        url_path = parse.urlparse(url).path
        raw_sign = '&'.join([method.upper(), parse.quote(url_path, safe=''), str(ts)])
        return base64.b64encode(
            hmac.new(
                _api_secret_key.encode(),
                raw_sign.encode(),
                hashlib.sha1
            ).digest()
        ).decode()



    def getDoubanShort(self,key):
        self.JadeLog.INFO("开始豆瓣搜索爬虫,搜索名称为:{},次数为:{}".format(key, self.index), True)
        api_url = "https://frodo.douban.com/api/v2"
        _api_key = "0dad551ec0f84ed02907ff5c42e8ec70"
        url = api_url + "/search/movie"
        ts = datetime.strftime(datetime.now(), '%Y%m%d')
        params = {'_sig': self.sign(url, ts), '_ts': ts, 'apiKey': _api_key,
                  'count': 1, 'os_rom': 'android', 'q': key, 'start': 0}
        headers = {
            'User-Agent': choice(self._user_agents),
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 'Accept': None, 'referer': None}
        try:
            search_rsp = self.session.get(url, params=params, headers=headers, verify=False, timeout=20,
                                          allow_redirects=True, stream=False)
            if search_rsp.status_code == 200:
                self.index = self.index + 1
                search_json = search_rsp.json()
                vod_short = self.paraseVodShortFromJson(key,search_json)
                return vod_short
            else:
                if "search_access_rate_limit" in search_rsp.text:
                    self.JadeLog.ERROR("豆瓣搜索爬虫失败,名称为:{},失败原因为:{}".format(key, "访问频率太快"))
                    time.sleep(60) ## 10分钟后重试
                    return self.getDoubanShort(key)
                else:
                    self.JadeLog.ERROR("豆瓣搜索爬虫失败,名称为:{},失败原因为:{}".format(key, search_rsp.text))
        except Exception as e:
            self.JadeLog.ERROR("豆瓣搜索爬虫失败,名称为:{},失败原因为:{}".format(key, e))

    def getDoubanDetail(self, key):
        api_url = "https://frodo.douban.com/api/v2"
        _api_key = "0dad551ec0f84ed02907ff5c42e8ec70"
        vod_short = self.getDoubanShort(key)
        if vod_short:
            search_url = api_url + vod_short.vod_id
            ts = datetime.strftime(datetime.now(), '%Y%m%d')
            params = {'_sig': self.sign(search_url, ts), '_ts': ts, 'apiKey': _api_key, 'os_rom': 'android'}
            headers = {
                'User-Agent': choice(self._user_agents),
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 'Accept': None,
                'referer': None}
            try:
                detail_rsp = self.session.get(search_url, params=params, headers=headers, verify=False,
                                              timeout=20,
                                              allow_redirects=True, stream=False)
                if detail_rsp.status_code == 200:
                    detail_json = detail_rsp.json()
                    vodDetail = self.paraseVodDetailFromJson(detail_json)
                    self.JadeLog.INFO("豆瓣详情爬虫成功,名称为:{}".format(key), True)
                    return vodDetail
                else:
                    self.JadeLog.ERROR("豆瓣详情爬虫失败,名称为:{}".format(key, detail_rsp.text))
            except Exception as e:
                self.JadeLog.ERROR("豆瓣详情爬虫失败,名称为:{},失败原因为:{}".format(key, e))

