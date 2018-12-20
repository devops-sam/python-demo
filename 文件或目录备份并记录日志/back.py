#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import  time, os, sys

# 定义源文件(必须全路径)
s_file = sys.argv[1]

# 定义备份目录
back_dir = "/tmp/backup/"

# 定义备份文件、目录及格式
s_fmt_file = s_file.split("/")[-1]
back_file = "%s%s-%s.tgz" % (back_dir, s_fmt_file, time.strftime("%Y%m%d_%H%M%S", time.localtime()))

# 定义记录日志
logfile = "/tmp/backup/backup.log"
def record_log(back_type, status, files, desc = "NULL"):
    date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    record_line = "%s %s %s %s %s\n" % (date, back_type, status, files, desc)
    with open(logfile, "a") as f:
        f.write(record_line)
        f.flush()

# 执行文件备份
def back_command():

    if os.path.exists(s_file):
        if len(sys.argv) == 2:
            back_command = "tar zvcf %s %s" % (back_file, s_file)
            print("----------------Normal Format Backup-----------------")
            result = os.system(back_command)
        elif len(sys.argv) == 4 and sys.argv[2] == "-X":
            exclude_file = sys.argv[3]
            back_command = "tar zvcf %s --exclude=%s %s" % (back_file, exclude_file ,s_file)
            print("----------------Exclude Format Backup-----------------")
            result = os.system(back_command)
        else:
            print("输入格式有误!")
    else:
        print("文件或者目录不存在!")
        exit(1)

    if result == 0:
        record_log("FULL BACKUP", "SUCCESS", "N/A", "test")
    else:
        record_log("FULL BACKUP", "FAILURE", "N/A", "test")

if __name__ == "__main__":
    back_command()
