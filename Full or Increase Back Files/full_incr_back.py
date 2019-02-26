#!/usr/bin/python3
# -*- coding:utf8 -*-

import os, sys, hashlib, time, tarfile, fnmatch, json

src_dir = '/root'
target_dir = '/data/back'
ex_dir = ['docker-http']
md5file = 'md5.data'


fullname = "full-%s-%s.tar.gz" % (src_dir.split('/',-1)[-1], time.strftime('%Y%m%d-%H%M%S'))
incrname = "incr-%s-%s.tar.gz" % (src_dir.split('/',-1)[-1], time.strftime('%Y%m%d-%H%M%S'))

# 获取文件md5值
def md5sum(file):
    h = hashlib.md5()
    with open(file) as f:
        while True:
            data = f.read(4096)
            if len(data) == 0:
                break
            h.update(data.encode('utf8'))
        return h.hexdigest()

def findfile(root, patterns=['*'], exclude_dir=[]):
    for root_dir, dirnames, filenames in os.walk(src_dir):
        for ex in exclude_dir:
            if ex in dirnames:
                dirnames.remove(ex)

        for pattern in patterns:
            for file in filenames:
                if  fnmatch.fnmatch(file,pattern):
                    yield os.path.join(root_dir, file)

def fullback():
    md5dic = {} 

    os.chdir(target_dir)

    with tarfile.open(fullname, 'w:gz') as t:
        for item in findfile(src_dir, exclude_dir=ex_dir):
            try:
                md5dic[item] = md5sum(item)
            except Exception as e:
                pass
            t.add(item)

    with open(md5file, 'w') as f:
        json.dump(md5dic,f)


def incrback():
    nmd5dic = {}

    os.chdir(target_dir)
    
    with open(md5file) as f:
        stored_md5_info = json.load(f)

    for item in findfile(src_dir, exclude_dir=ex_dir):
        try:
            nmd5dic[item] = md5sum(item)
        except Exception as e:
            pass

    with tarfile.open(incrname, 'w:gz') as t:
        for key in nmd5dic:
            if (key not in stored_md5_info) or (nmd5dic[key] != stored_md5_info[key]):
                t.add(key)

    with open(md5file, 'w') as f:
        json.dump(nmd5dic,f)

def explain():
    print("""Usage: python3 %s [1|2] 
        1.full back
        2.increase backup""" % (sys.argv[0])) 

def main():
    sys.argv.append('')
    if sys.argv[1] == '1':
        fullback()
    elif sys.argv[1] == '2':
        incrback()
    else:
        explain()

if __name__ == "__main__":
    main()


