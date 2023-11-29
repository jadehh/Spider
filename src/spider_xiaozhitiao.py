#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File     : spider_xiaozhitiao.py
# @Author   : jade
# @Date     : 2023/11/29 9:32
# @Email    : jadehh@1ive.com
# @Software : Samples
# @Desc     : 阿里小纸条爬虫
import json
from src.spider import Spider,BeautifulSoup
import time

class SpiderXiaoZhiTiao(Spider):
    def __init__(self):
        self.home_url = "https://ali.gitcafe.ink/"
        self.categort_list = []
        super().__init__()

    def get(self):
        self.driver.get(self.home_url)
        time.sleep(2)
        self.JadeLog.INFO("阿里小纸条爬虫成功:{}".format(self.driver.page_source),True)
        self.parase(self.driver.page_source)
        self.release()

    def parase(self,html):
        soup = BeautifulSoup(html, 'lxml')
        elemets = soup.find_all("tbody") ## 最近,置顶,资源列表三
        self.JadeLog.INFO("阿里小纸条资源解析成功",True)
        classes = self.getCategoryContent(elemets[3])
        self.JadeLog.INFO("阿里纸条分类页解析完成",True)
        vod_list = self.getHomeContent(elemets[1])
        self.JadeLog.INFO("阿里纸条首页解析完成",True)
        xiaozhitiao_json = {
            "class":classes,
            "list":vod_list
        }
        with open("json/xiaozhitiao.json","wb") as f:
            f.write(json.dumps(xiaozhitiao_json).encode("utf-8"))
        self.JadeLog.INFO("阿里小纸条JSON文件写入成功",True)

    def parase_home_element(self,element):
        update_time = (element.text.split("【"))[0].replace(" ", "")
        vod_content = element.text.split("】")[-1].replace(" ", "")
        vodName = vod_content[:-10]
        vodPic = self.get_pic(vodName)
        vodId = vod_content[-10:]
        vodRemarks = element.text.split("【")[-1].split("】")[0]
        if vodRemarks in self.categort_list:
            return update_time, vodId, vodName, vodPic, vodRemarks
        else:
            return None,None,None,None,None
    def parase_category_element(self,element):
        vodId = element.find("a").get("href")
        vodRemarks = element.find("td").get("tooltip").split("|")[-1]
        vodName = element.text.replace("\n","").replace(" ","")[:-19]
        vodPic = self.get_pic(vodName)
        self.JadeLog.INFO("vod pic:{}".format(vodPic))
        return vodId,vodName,vodPic,vodRemarks
    def getVod(self,elements):
        vod_list = []
        for element in elements:
            update_time,vodId,vodName,vodPic,vodRemarks = self.parase_home_element(element)
            if update_time:
                vod_list.append({"vod_id": vodId, "vod_name": vodName + ":更新时间为:{}".format(update_time), "vod_pic": vodPic, "vod_remarks": vodRemarks})
        return vod_list


    def getHomeContent(self,elements):
        return self.getVod(elements.find_all("tr"))


    def getCategoryContent(self,elements):
        classes_dic = []
        cat_elements = elements.select(".cat")
        for element in cat_elements:
            classes_dic.append({"type_name": element.text, "list": []})
            self.categort_list.append(element.text)
        all_elements = (elements.find_all("tr"))
        tmp_index = 0
        for element in all_elements:
            if element.text.strip() in self.categort_list:
                tmp_index = self.categort_list.index(element.text.strip())

            else:
                vodId,vodName,vodPic,vodRemarks = self.parase_category_element(element)
                classes_dic[tmp_index]["list"].append({"vod_id": vodId, "vod_name": vodName, "vod_pic": vodPic,
                 "vod_remarks": vodRemarks})
        self.categort_list = self.categort_list[:19]
        return classes_dic[:19]
