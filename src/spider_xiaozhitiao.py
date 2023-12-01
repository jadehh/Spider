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
        with open("json/xiaozhitiao.json", "wb") as f:
            f.write(json.dumps(xiaozhitiao_json,ensure_ascii=False,indent=4).encode("utf-8"))
        self.JadeLog.INFO("阿里小纸条JSON文件写入成功", True)


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
        vod_detail.vod_id = ele_list[2].find("a").get("href")
        update_time = ele_list[0].text
        vod_detail.vod_name = ele_list[1].text.split("】")[-1].split(vod_detail.vod_id.split("/")[-1])[0]
        vod_detail.vod_content = ele_list[1].get("tooltip").split("|")[-1]
        vod_detail.type_name = ele_list[1].text.split("【")[-1].split("】")[0]
        vod_detail.vod_pic = self.get_pic(vod_detail.vod_name + vod_detail.type_name)
        if vod_detail.type_name in self.categort_list:
            return vod_detail.to_dict()
        else:
            return None

    def parase_category_element(self, element):
        vod_detail = VodDetail()
        ele_list = element.find_all("td")
        vod_detail.vod_id = ele_list[1].find("a").get("href")
        vod_detail.vod_content = ele_list[0].get("tooltip").split("|")[-1]
        vod_detail.vod_name = ele_list[0].text
        vod_detail.vod_pic = self.get_pic(vod_detail.vod_name)
        return vod_detail.to_dict()


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
                classes_dic[tmp_index]["list"].append(vod_dic)
        self.categort_list = self.categort_list[:12]  ##下个版本优化
        return classes_dic[:12]
