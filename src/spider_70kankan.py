#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File     : spider_70kankan.py
# @Author   : jade
# @Date     : 2024/1/3 9:49
# @Email    : jadehh@1ive.com
# @Software : Samples
# @Desc     :
import time
import requests
from src.chrome_spider import ChromeSpider,BeautifulSoup
import json

class Spider70Kankan(ChromeSpider):
    def __init__(self):
        self.siteUrl = "http://cqdb6.com"
        self.header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
         , "Referer": self.siteUrl + "/"
        }

        super().__init__()

    def fetch(self, url, header=None):
        try:
            if header:
                rsp = requests.get(url, headers=self.header)
            else:
                rsp = requests.get(url, headers=header)
            rsp.encoding = "utf-8-sig"
            if rsp.status_code == 200:
                return rsp.text
            else:
                self.fetch(url,header)
        except Exception as e:
            self.JadeLog.ERROR("url地址为:{},访问失败,失败原因为:{}".format(url, e))
            return None


    def getExtend(self,type_id):
        url = self.siteUrl + type_id
        text = self.fetch(url)
        extend_list = []
        soup = BeautifulSoup(text, 'lxml')
        elements = soup.select("[class=\"sy scon clearfix\"]")[0].select("dl")
        i = 0
        for element in elements:
            type_name =  element.find("dt").text.replace("按", "").replace("：", "")
            extend_dic = {"key": str(i + 1), "name": type_name,
                          "value": []}
            type_elements = element.find_all("a")

            if type_name == "剧情":
                index = 3
            elif type_name == "年代":
                index = 2
            elif type_name == "地区":
                index = 4

            for type_element in type_elements:
                type_id_list = type_element.attrs["href"].split("/")
                extend_dic["value"].append({"n": type_element.text, "v": type_id_list[index]})
            extend_list.append(extend_dic)
            i = i + 1

        return extend_list

    def get(self):
        category_extend_dic = {}
        text = self.fetch(self.siteUrl,self.header)
        soup = BeautifulSoup(text, 'lxml')
        elements = soup.select("[class=index-list-l]")
        for element in elements:
            type_id = element.select("[class=\"h1 clearfix\"]")[0].find("a").attrs["href"]
            if len(type_id) > 0:
                category_extend_dic[str(type_id)] = self.getExtend(type_id)

        with open("json/70kankan.json", "wb") as f:
            f.write(json.dumps(category_extend_dic, ensure_ascii=False, indent=4).encode("utf-8"))
        self.JadeLog.INFO("70看看JSON文件写入成功", True)
        self.release()
