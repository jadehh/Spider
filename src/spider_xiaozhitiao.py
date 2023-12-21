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
from src.chrome_spider import ChromeSpider, BeautifulSoup,requests
import time
from src.vod import VodDetail
import re

class SpiderXiaoZhiTiao(ChromeSpider):
    def __init__(self):
        self.home_url = "https://o.gitcafe.net"
        self.categort_list = []
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
        xiaozhitiao_json = self.paraseVodDetailByDouban(xiaozhitiao_json)

        with open("json/xiaozhitiao.json", "wb") as f:
            f.write(json.dumps(xiaozhitiao_json,ensure_ascii=False,indent=4).encode("utf-8"))
        self.JadeLog.INFO("阿里小纸条JSON文件写入成功", True)



    def paraseVodDetailByDouban(self,xiaozhitiao_json):
        classes = xiaozhitiao_json["class"]
        vod_list = xiaozhitiao_json["list"]
        new_vod_list = []
        for vod_detail_dic in vod_list:
            or_vodetail = VodDetail()
            or_vodetail.load_dic(vod_detail_dic)
            vod_detail = self.getDoubanDetail(or_vodetail.vod_name)
            or_vodetail.copy(vod_detail)
            new_vod_list.append(or_vodetail.to_dict())
        xiaozhitiao_json["list"] = new_vod_list
        new_classes = []
        for class_dic in classes:
            type_name = class_dic["type_name"]
            new_vod_list = []
            for vod_detail_dic in class_dic["list"]:
                or_vodetail = VodDetail()
                or_vodetail.load_dic(vod_detail_dic)
                vod_detail = self.getDoubanDetail(or_vodetail.vod_name)
                or_vodetail.copy(vod_detail)
                new_vod_list.append(or_vodetail.to_dict())
            new_classes.append({"type_name":type_name,"list":new_vod_list})
        xiaozhitiao_json["class"] = new_classes
        return xiaozhitiao_json



    def parase_vod_info(self,vod_info,vod_dic):
        if len(vod_info) > 0:
            if "[" and "]" in vod_info:
                vod_dic["vod_content"] = vod_info.split("]")[-1]
                vod_dic["vod_year"] = vod_info.split("]")[0].split("[")[-1]
            else:
                vod_dic["vod_content"] = vod_info
        return vod_dic



    def parase_home_element(self, element):
        vod_detail = VodDetail()
        ele_list = element.find_all("td")
        update_time = ele_list[0].text
        vod_id = ele_list[2].find("a").get("href")
        name = self.format_key(ele_list[1].text.split("】")[-1].split(vod_id)[0])
        if name:
            type_name = ele_list[1].text.split("【")[-1].split("】")[0]
            vod_detail.vod_name = name
            vod_detail.vod_content = ele_list[1].get("tooltip").split("|")[-1]
            vod_detail.type_name = type_name
            vod_detail.vod_remarks = update_time
            vod_detail.vod_id = vod_id
            if type_name in self.categort_list:
                return vod_detail.set_id_to_dic()
            else:
                return None
        else:
            return None

    def is_letter(self,char):
        return char.isalpha()

    def is_letter(self,char):
        pattern = r'[a-zA-Z]'
        matcher = re.match(pattern, char)
        if matcher:
            return True
        else:
            return False

    def format_key(self,key):
        key_list = ["4k", "2023", "4K","完结","惊悚","犯罪","恐怖","悬疑","-₂","韩国","美国","喜剧","动作","高码",
                    "-.","合集","无水印","〖〗","大电影","电影","1080p₂","丨","附系列","","t3460帧率版本","双语","正式版",
                    "国印","持续更新","简日","最新","国漫","1080p","要q","英语","启蒙","中字","熟肉","〖","〗"]
        new_key = key.lower()
        pattern = r'\d+'
        for key_work in key_list:
            if key_work in new_key:
                new_key = new_key.replace(key_work, "")

        if "@" in new_key:
            new_key = new_key.split("@")[0]
        if " " in new_key:
            new_key = new_key.split(" ")[0]
        if "-" in new_key:
            new_key = new_key.split("-")[0]
        if "." in new_key:
            new_key = new_key.split(".")[0]
        if "全" in new_key:
            new_key = new_key.split("全")[0]
        if len(new_key) > 1:
            if self.is_letter(new_key[0]) is True and self.is_letter(new_key[1]) is False:
                new_key = new_key[1:]
        return new_key

    def parase_category_element(self, element):
        vod_detail = VodDetail()
        ele_list = element.find_all("td")
        name = self.format_key(ele_list[0].text)
        if name:
            vod_detail.vod_content = ele_list[0].get("tooltip").split("|")[-1]
            vod_detail.vod_name = name
            vod_detail.vod_id = ele_list[1].find("a").get("href")
            return vod_detail.set_id_to_dic()
        else:
            return None
    def getDoubanDetail(self, key):
        return None

    # def get_pic(self,name):
    #     return ""
    def getVod(self, elements):
        vod_list = []
        for element in elements:
            vod_dic = self.parase_home_element(element)
            if vod_dic:
                vod_list.append(vod_dic)
        return vod_list


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
                if vod_dic:
                    classes_dic[tmp_index]["list"].append(vod_dic)
        self.categort_list = self.categort_list[:13]  ##下个版本优化
        return classes_dic[:13]
