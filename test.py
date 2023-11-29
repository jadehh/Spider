#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File     : test.py
# @Author   : jade
# @Date     : 2023/11/29 9:31
# @Email    : jadehh@1ive.com
# @Software : Samples
# @Desc     :
from src.spider import Spider
from bs4 import BeautifulSoup
from difflib import SequenceMatcher  # 导入库
def similarity_str(a, b):
    return SequenceMatcher(None, a, b).ratio()
def test_xiaozhitiao_spider():
    from src.spider_xiaozhitiao import SpiderXiaoZhiTiao
    spider = SpiderXiaoZhiTiao()
    spider.get()




if __name__ == '__main__':
    test_xiaozhitiao_spider()