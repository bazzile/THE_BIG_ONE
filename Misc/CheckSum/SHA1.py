# -*- coding: utf-8 -*-
import sys
import os
import hashlib

root_dir = r"D:\WORK\SHA_test"

def get_checksum(target_file):
    # BUF_SIZE is totally arbitrary, change for your app!
    BUF_SIZE = 65536  # lets read stuff in 64kb chunks!

    # md5 = hashlib.md5()
    sha1 = hashlib.sha1()

    with open(target_file, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            # md5.update(data)
            sha1.update(data)

    # print("MD5: {0}".format(md5.hexdigest()))
    print("SHA1: {0}".format(sha1.hexdigest()))
    return sha1.hexdigest()

path, dirs, files = os.walk(root_dir)
file_counter = len(files) + 1

for root, dirnames, filenames in os.walk(root_dir):
    done_counter = 0
    for dirpath in [os.path.join(root, dirname) for dirname in dirnames]:
        for f in os.listdir(dirpath):
            print('Расчитываем SHA1 для файла {}...'.format(f))
            with open(os.path.join(dirpath, "ФОРМУЛЯР_НОСИТЕЛЯ.txt"), 'a') as log_f:
                log_f.write('{}={};\n'.format(f, get_checksum(os.path.join(dirpath, f))))
            file_counter -= 1
            print("Готово. Осталось файлов: {}\n".format(file_counter))
