#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File     : vod.py
# @Author   : jade
# @Date     : 2023/12/1 11:24
# @Email    : jadehh@1ive.com
# @Software : Samples
# @Desc     :
class VodShot(object):
    def __init__(self):
        self.vod_id = ""                           ## id
        self.vod_name = ""                         ## 名称
        self.vod_pic = ""                          ## 图片
        self.vod_remarks = "制作人:简得辉"            ## 备注
    def to_dict(self):
        dic = {}
        for item in self.__dict__.items():
            dic[item[0]] = item[1]
        return dic
class VodDetail(VodShot):
    def __init__(self):
        super().__init__()
        self.type_name = ""              ## 类别
        self.vod_year = ""               ## 年份
        self.vod_area = ""               ## 地区
        self.vod_actor = ""              ## 导演
        self.vod_director = ""           ## 演员
        self.vod_content = ""            ## 剧情
        self.vod_play_from = ""          ## 播放格式
        self.vod_play_url = ""           ## 播放连接