## 基于python和python fabric开发的上线脚本

> fabric基于python 2.5及以上版本，推荐使用python2.7

> pip install fabric 安装fabric模块

### 脚本使用说明
1. config.py 路径配置。配置本地路径及远程路径
2. fabfile.py fab的执行文件，如果不是以这个文件命名则执行的时候需要带-f参数： fab -f test.py go
3. source.txt 需要上线的文件列表，可以是目录

### 执行方式
直接在命令行中执行fab go

> 0.2版本更新说明

1. 增加打包回滚功能。回滚执行命令fab back:v=201606291043
2. 增加本地文件不存在的容错处理
3. 增加无项目名称的本地路径的处理

> 0.3版本更新说明

1. 直接执行fab back 回滚到上一版本