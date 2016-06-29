#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'JustFantasy'

# 基础路径
local_basepath = u'F:/code/'     # 本地基础路径
target_basepath = '/data/tmp/'       # 远程基础路径
target_bak_basepath = '/data/bak/'     # 远程备份路径

# 没有项目名称源地址
exclude_path = (
    'at.vue.cn'
)

# 本地项目对应的绝对路径
local_path_map = {
    'www.vue.com': local_basepath + u'测试/',
}

# 远程项目对应的绝对路径
target_path_map = {
    'www.vue.com': target_basepath,
}


