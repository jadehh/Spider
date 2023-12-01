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

def test_xiaozhitiao_spider():
    from src.spider_xiaozhitiao import SpiderXiaoZhiTiao
    spider = SpiderXiaoZhiTiao()
    spider.get()

def test_yunpan_share_spider():
    from src.spider_yunpanshare import SpiderYunPanShare
    spider = SpiderYunPanShare()
    spider.homeContent(False)





if __name__ == '__main__':
    test_xiaozhitiao_spider()