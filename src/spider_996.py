#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File     : spider_996.py
# @Author   : jade
# @Date     : 2024/1/10 20:03
# @Email    : jadehh@1ive.com
# @Software : Samples
# @Desc     :
import copy
import json
from src.chrome_spider import ChromeSpider, BeautifulSoup,requests
import time
from src.vod import VodDetail
import re
import sys

class SpiderJiuJiuLiu(ChromeSpider):
    def __init__(self):
        self.categort_list = []
        super().__init__()


    def getExtent(self, tree):
        elements = tree.select("[class='stui-pannel_hd']")
        extend_list = []
        index = 0
        for i in range(len(elements[0:2])):
            cate_element = elements[i]
            type_elements = cate_element.find_all("ul")
            if i == 0:
                for type_element in type_elements:
                    extend_dic = {"key": str(index + 1), "name": "", "value": []}
                    extend_dic["name"] = type_element.find("li").text
                    if index == 0:
                        for ele in type_element.find_all("li")[1:]:
                            if (len(ele.text)) > 0:
                                extend_dic["value"].append({"n": ele.text, "v": ele.find("a").attrs["href"].split("/")[-1].split(".")[0]})
                    else:

                        for ele in type_element.find_all("li")[1:]:
                            if (len(ele.text)) > 0:
                                extend_dic["value"].append({"n": ele.text, "v": ele.text})
                    extend_list.append(extend_dic)
                    index  = index +1
            else:
                extend_dic = {"key": str(index + 1), "name": "", "value": []}
                extend_dic["name"] = cate_element.find("li").text
                extend_dic["value"].append({"n": "全部", "v": "time"})
                for ele in cate_element.find_all("li")[1:]:
                    if (len(ele.text)) > 0:
                        extend_dic["value"].append({"n": ele.text, "v": ele.find("a").attrs["href"].split("/")[3]})
                extend_list.append(extend_dic)
                index = index + 1
        return extend_list

    def fetch(self, url, header=None):
        try:
            if header:
                rsp = self.session.get(url, headers=self.header)
            else:
                rsp = self.session.get(url, headers=header)
            return rsp
        except Exception as e:
            self.JadeLog.ERROR("url地址为:{},访问失败,失败原因为:{}".format(url, e))
            sys.exit()
            return None

    def get(self):
        category_extend_dic = {}
        for i in range(4):
            category_id = i + 1
            url = "https://www.cs1369.com/show/id/{}.html".format(category_id)
            response = self.fetch(url)
            self.JadeLog.INFO("分类URL为:{}".format(url))
            soup = BeautifulSoup(response.text,"lxml")
            category_extend_dic["/show/id/{}".format(category_id)] = self.getExtent(soup)
        with open("json/996.json", "wb") as f:
            f.write(json.dumps(category_extend_dic, ensure_ascii=False, indent=4).encode("utf-8"))
        self.release()


