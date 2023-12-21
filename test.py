#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File     : test.py
# @Author   : jade
# @Date     : 2023/11/29 9:31
# @Email    : jadehh@1ive.com
# @Software : Samples
# @Desc     :
from bs4 import BeautifulSoup
from difflib import SequenceMatcher  # 导入库
import re
def test_xiaozhitiao_spider():
    from src.spider_xiaozhitiao import SpiderXiaoZhiTiao
    spider = SpiderXiaoZhiTiao()
    spider.get()

def test_yunpan_share_spider():
    from src.spider_yunpanshare import SpiderYunPanShare
    spider = SpiderYunPanShare()
    spider.homeContent(False)

def test_wanou_spider():
    from src.spider_wanou import SpiderWanou
    spider = SpiderWanou()
    spider.get()




if __name__ == '__main__':
    test_wanou_spider()
    test_xiaozhitiao_spider()
