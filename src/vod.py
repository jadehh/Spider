#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File     : vod.py
# @Author   : jade
# @Date     : 2023/12/1 11:24
# @Email    : jadehh@1ive.com
# @Software : Samples
# @Desc     :
LocalAddress = "https://gh.con.sh/https://raw.githubusercontent.com/jadehh/TV/py"

class VodShort(object):
    def __init__(self):
        self.vod_id = ""  ## id
        self.vod_name = ""  ## 名称
        self.vod_pic = "{}/jpg/ali.jpg".format(LocalAddress)  ## 图片
        self.vod_remarks = ""  ## 备注

    def to_dict(self):
        dic = {}
        for item in self.__dict__.items():
            dic[item[0]] = item[1]
        return dic

    def load_dic(self, dic):
        for key in list(dic.keys()):
            if key in list(self.to_dict().keys()):
                setattr(self, key, dic[key])

    def copy(self,vod_detail):
        dic = self.to_dict()
        if vod_detail:
            vod_detail_dic = vod_detail.to_dict()
            for key in list(dic.keys()):
                is_need_set = False
                if len(dic[key]) > 0:
                    if key == "vod_id" or key == "vod_name":
                        pass
                    else:
                        is_need_set = True
                else:
                    is_need_set = True
                if is_need_set:
                    setattr(self, key, vod_detail_dic[key])

class VodDetail(VodShort):
    def __init__(self):
        super().__init__()
        self.type_name = ""  ## 类别
        self.vod_year = ""  ## 年份
        self.vod_area = ""  ## 地区
        self.vod_actor = ""  ## 导演
        self.vod_director = ""  ## 演员
        self.vod_content = ""  ## 剧情
        self.vod_play_from = ""  ## 播放格式
        self.vod_play_url = ""  ## 播放连接

    def to_short(self):
        vodShort = VodShort()
        vodShort.load_dic(self.to_dict())
        return vodShort.to_dict()