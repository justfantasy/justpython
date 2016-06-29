#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
fab -f s1.py go
    -f 表示文件名不为fabfile.py的时候需要指定
    go 指定要执行的方法名称

fab hello:name=age,value=20 或者 fab hello:age,20 带参数的使用方法

examples: http://wklken.me/posts/2013/03/25/python-tool-fabric.html

todo:   解决没有目录的情况
        增加备份和回滚

'''
__author__ = 'JustFantasy'

from fabric.api import *
from fabric.colors import *
from fabric.context_managers import *
from fabric.contrib.console import confirm
from fabric.contrib import files
#from fabric.contrib import project
import config, os, os.path
from datetime import *

# 配置连接服务器的参数
env.user = config.user
env.hosts = config.hosts
env.password = config.password

# 代码上传
def code_upload(path, remoteBakName):
    with settings(warn_only=True):

        # 格式转化
        pathParams = path.replace('\\', '/').split('/')

        # 获取本地绝对路径
        try:
            localAbsPath = config.local_path_map[pathParams[0]] + path
        except KeyError:
            localAbsPath = config.local_basepath + path

        # 如果路径中没有项目名称，则去掉项目名称
        if pathParams[0] in config.exclude_path:
            localAbsPath = localAbsPath.replace(pathParams[0] + '/', '')

        # 判断本地文件是否存在
        if not os.path.exists(localAbsPath) and not confirm(localAbsPath + ' is not exists, Continue?'):
            abort('Aborting file put task!')

        # 获取远程绝对路径
        try:
            remoteAbsPath = config.target_path_map[pathParams[0]] + path
        except KeyError:
            remoteAbsPath = config.target_basepath + path

        # 文件备份操作
        if files.exists(remoteAbsPath):
            #with hide('running', 'stdout'):
            run('tar -rPvf ' + remoteBakName + ' ' + remoteAbsPath)

        # 判断是否是文件，如果是目录，则遍历出所有的文件
        if os.path.isfile(localAbsPath):
            upload(localAbsPath, remoteAbsPath)
        else:
            # 三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
            for parent, dirnames, filenames in os.walk(localAbsPath):
                for filename in filenames:
                    tmpAbsPath = os.path.join(parent, filename).replace('\\', '/')
                    targetPath = tmpAbsPath.replace(localAbsPath, remoteAbsPath)
                    upload(tmpAbsPath, targetPath)

            # 如果是linux服务器，可以直接使用这个方法进行代码更新
            # project.rsync_project(remoteAbsPath, localAbsPath)

# 文件上传操作
def upload(source, targetPath):

    # 若远程目录不存在则创建
    targetDir = os.path.dirname(targetPath)
    if not files.exists(targetDir):
        run('mkdir -p ' + targetDir)

    #上传操作
    result = put(source, targetPath)
    if result.failed and not confirm('put file failed, Continue?'):
        abort('Aborting file put task!')

# @desc: 代码上传
# @exec: 调用方式，fab go
@task
def go():
    print yellow(u'正在上传代码到服务器...')

    remoteBakName = config.target_bak_basepath.rstrip('/') + '/' + datetime.now().strftime('%Y%m%d%H%M') + '.tar'
    print yellow(u'备份文件路径：' + remoteBakName)

    with open('source.txt') as f:
        for line in f.readlines():
            code_upload(line.strip(), remoteBakName)

# @desc: 代码回滚，v表示tar包的名称
# @exec: 调用方式，fab back:v=201606291015
@task()
def back(v=None):
    if v == None:
        with hide('running', 'stdout'):
            with cd(config.target_bak_basepath):
                v = run("ls -lt *.tar|sed -n '1p'|awk '{print $9}'|awk -F '.' '{print $1}'")
    print yellow(u'将代码回退到版本：' + v)
    #with hide('stdout'):
    with cd(config.target_bak_basepath):
        run('tar -xPvf ' + v + '.tar')







