#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File     : spider_wanou.py
# @Author   : jade
# @Date     : 2023/12/14 19:36
# @Email    : jadehh@1ive.com
# @Software : Samples
# @Desc     :
from src.chrome_spider import ChromeSpider
from lxml import etree,html
import json
class SpiderWanou(ChromeSpider):
    def __init__(self):
        super().__init__()
        header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"}


    def getExtent(self, tree):
        elements = tree.xpath("//div[@class='scroll-content']")[1:]
        extend_list = []
        for i in range(len(elements)):
            extend_dic = {"key": str(i+1), "name": "", "value": []}
            if i < len(elements) - 1:
                extend_dic["name"] = elements[i].xpath("a/text()")[0]
                for ele in elements[i].xpath("div/a"):
                    extend_dic["value"].append({"n": ele.xpath("text()")[0], "v": ele.xpath("text()")[0]})
                extend_list.append(extend_dic)
            else:
                extend_dic["name"] = elements[i].xpath("div/a")[0].xpath("text()")[0]
                extend_dic["value"] = [{"n": elements[i].xpath("div/a")[1].xpath("text()")[0], "v":"hits"},
                                       {"n": elements[i].xpath("div/a")[2].xpath("text()")[0], "v":"score"}]

                extend_list.append(extend_dic)
        return extend_list

    def fetch(self, url, header=None):
        try:
            if header:
                rsp = self.session.get(url, headers=self.header)
            else:
                rsp = self.session.get(url, headers=header)
            return rsp
        except Exception as e:
            self.logger.error("url地址为:{},访问失败,失败原因为:{}".format(url, e))
            sys.exit()
            return None


    def get(self):
        category_extend_dic = {}
        for i in range(6):
            category_id = i + 1
            url = "https://tvfan.xxooo.cf/index.php/vodshow/{}--------1---.html".format(category_id)
            response = self.fetch(url)
            self.JadeLog.INFO("分类URL为:{}".format(url))
            tree = html.fromstring(response.text)
            category_extend_dic[str(category_id)] = self.getExtent(tree)
        with open("json/wanou.json","wb") as f:
            f.write(json.dumps(category_extend_dic, ensure_ascii=False, indent=4).encode("utf-8"))
        self.release()
