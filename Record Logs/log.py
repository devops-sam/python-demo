#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import logging, time, os

# 定义日志目录及文件
log_dir = os.getcwd() + "/logs/"

if os.path.exists(log_dir):
    pass
else:
    os.system("mkdir %s" % (log_dir))

pre_log = time.strftime("%Y-%m-%d")
log_name = log_dir + pre_log + ".log"

# 创建一个logger对象
logger = logging.getLogger("__name__")
# 设置记录的级别
logger.setLevel(logging.DEBUG)

# 创建一个处理日志的文件
fh = logging.FileHandler(log_name)
# 设置处理日志的日志级别
fh.setLevel(logging.INFO)

# 定义handler输入的格式
datefmt = "%Y-%m-%d %H:%M:%S"
fmt = "%(asctime)s %(levelname)s %(filename)s[line:%(lineno)d] %(process)d %(message)s"
formatter = logging.Formatter(fmt, datefmt)
fh.setFormatter(formatter)

# 添加logger对象到handler日志处理
logger.addHandler(fh)

# 输出日志
logger.debug('this is a logger debug message')
logger.info('this is a logger info message')
logger.warning('this is a logger warning message')
logger.error('this is a logger error message')
logger.critical('this is a logger critical message')
