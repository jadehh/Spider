#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File     : spider_xiaozhitiao.py
# @Author   : jade
# @Date     : 2023/11/29 9:32
# @Email    : jadehh@1ive.com
# @Software : Samples
# @Desc     : 阿里小纸条爬虫
import copy
import json
from src.spider import Spider, BeautifulSoup
import time


class SpiderXiaoZhiTiao(Spider):
    def __init__(self):
        self.home_url = "https://o.gitcafe.net"
        self.categort_list = []
        self.vod_dic =  {
            "vod_id": "",
            "vod_name": "",
            "vod_pic": "",
            "type_name": "",
            "vod_year": "",
            "vod_area": "",
            "vod_remarks": "制作人:Jade",
            "vod_actor": "",
            "vod_director": "",
            "vod_content": ""
        }
        super().__init__()

    def get(self):
        self.driver.get(self.home_url)
        time.sleep(2)
        self.JadeLog.INFO("阿里小纸条网页爬虫成功", True)
        self.parase(self.driver.page_source)
        self.release()

    def parase(self, html):
        soup = BeautifulSoup(html, 'lxml')
        elemets = soup.find_all("tbody")  ## 最近,置顶,资源列表三
        classes = self.getCategoryContent(elemets[3])
        self.JadeLog.INFO("阿里纸条分类页解析完成", True)
        vod_list = self.getHomeContent(elemets[1])
        self.JadeLog.INFO("阿里纸条首页解析完成", True)
        xiaozhitiao_json = {
            "class": classes,
            "list": vod_list
        }
        with open("json/xiaozhitiao.json", "wb") as f:
            f.write(json.dumps(xiaozhitiao_json,indent=4).encode("utf-8"))
        self.JadeLog.INFO("阿里小纸条JSON文件写入成功", True)


    def parase_vod_info(self,vod_info,vod_dic):
        if len(vod_info) > 0:
            if "[" and "]" in vod_info:
                vod_dic["vod_content"] = vod_info.split("]")[-1]
                vod_dic["vod_year"] = vod_info.split("]")[0].split("[")[-1]
            else:
                vod_dic["vod_content"] = vod_info
        return vod_dic

    def init_vod_dic(self,vod_id,vod_name,vod_pic,vod_info,vod_remark,type_name,update_time=None):
        vod_dic = copy.copy(self.vod_dic)
        if vod_id:
            vod_dic["vod_id"] = vod_id
        if vod_name:
            vod_dic["vod_name"] = vod_name
            if update_time:
                vod_dic["vod_name"] = vod_name  + " 更新时间为:{}".format(update_time)
        if vod_pic:
            vod_dic["vod_pic"] = vod_pic
        if vod_info:
            vod_dic = self.parase_vod_info(vod_info,vod_dic)
        if vod_remark:
            vod_dic["vod_remark"] = vod_remark
        if type_name:
            vod_dic["type_name"] = type_name
        return vod_dic

    def parase_home_element(self, element):
        ele_list = element.find_all("td")
        vodId = ele_list[2].find("a").get("href")
        update_time = ele_list[0].text
        vodName = ele_list[1].text.split("】")[-1].split(vodId.split("/")[-1])[0]
        vodInfo = ele_list[1].get("tooltip").split("|")[-1]
        typeName = ele_list[1].text.split("【")[-1].split("】")[0]
        vodPic = self.get_pic(vodName + typeName)
        vod_dic = self.init_vod_dic(vodId,vodName,vodPic,vodInfo,None,typeName,update_time)
        if typeName in self.categort_list:
            return vod_dic
        else:
            return None

    def parase_category_element(self, element):
        ele_list = element.find_all("td")
        vodId = ele_list[1].find("a").get("href")
        vodInfo = ele_list[0].get("tooltip").split("|")[-1]
        vodName = ele_list[0].text
        vodPic = self.get_pic(vodName)
        vod_dic = self.init_vod_dic(vodId,vodName,vodPic,vodInfo,None,None)
        return vod_dic

    def getVod(self, elements):
        vod_list = []
        for element in elements:
            vod_dic = self.parase_home_element(element)
            if vod_dic:
                vod_list.append(vod_dic)
        return vod_list

    def get_pic(self, name):
        return ""

    def getHomeContent(self, elements):
        return self.getVod(elements.find_all("tr"))

    def getCategoryContent(self, elements):
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
                vod_dic = self.parase_category_element(element)
                classes_dic[tmp_index]["list"].append(vod_dic)
        self.categort_list = self.categort_list[:12]  ##下个版本优化
        return classes_dic[:12]
