#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
fab -f s1.py go
    -f 表示文件名不为fabfile.py的时候需要指定
    go 指定要执行的方法名称

fab hello:name=age,value=20 或者 fab hello:age,20 带参数的使用方法

examples: http://wklken.me/posts/2013/03/25/python-tool-fabric.html
'''
__author__ = 'JustFantasy'

from fabric.api import *
from fabric.colors import *
from fabric.context_managers import *
from fabric.contrib.console import confirm
import config, os, os.path

# 配置连接服务器的参数
env.user = 'root'
env.hosts = ['10.0.8.88']
env.password = 'vue@test_0000'

# 代码上传
def code_upload(path):
    print yellow(u'正在上传代码到服务器...')
    with settings(warn_only=True):

        # 格式转化
        pathParams = path.replace('\\', '/').split('/')

        # 获取本地绝对路径
        try:
            localAbsPath = config.local_path_map[pathParams[0]] + path
        except KeyError:
            localAbsPath = config.local_basepath + path

        # 获取远程绝对路径
        try:
            remoteAbsPath = config.target_path_map[pathParams[0]] + path
        except KeyError:
            remoteAbsPath = config.target_path_map + path


        # 判断是否是文件，如果是目录，则遍历出所有的文件
        if os.path.isfile(localAbsPath):
            upload(localAbsPath, remoteAbsPath)
        else:
            #三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
            for parent, dirnames, filenames in os.walk(localAbsPath):
                for filename in filenames:
                    tmpAbsPath = os.path.join(parent, filename).replace('\\', '/')
                    targetPath = tmpAbsPath.replace(localAbsPath, remoteAbsPath)
                    upload(tmpAbsPath, targetPath)

# 文件上传操作
def upload(source, targetPath):

    # 首先判断目录是否存在，不存在则创建
    targetDir = os.path.dirname(targetPath)

    if not os.path.exists(targetDir):
        run('mkdir -p ' + targetDir)

    #上传操作
    result = put(source, targetPath)
    if result.failed and not confirm('put file failed, Continue?'):
        abort('Aborting file put task!')


@task
def go():
    with open('source.txt') as f:
        for line in f.readlines():
            code_upload(line.strip())







