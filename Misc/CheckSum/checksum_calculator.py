# -*- coding: utf-8 -*-
import sys
import os
import hashlib
import time
import zlib

root_dir = r"U:\PRJ\2017\BANS17\1_QuickWork\4_DEM\HD"
checksum = 'crc32'  # 'md5' 'sha1'


def crc(fileName):
    prev = 0
    for eachLine in open(fileName, "rb"):
        prev = zlib.crc32(eachLine, prev)
    return "%X" % (prev & 0xFFFFFFFF)


def get_checksum(target_file, sum_type):
    if sum_type == 'crc32':
        prev = 0
        for eachLine in open(target_file, "rb"):
            prev = zlib.crc32(eachLine, prev)
        return "%X" % (prev & 0xFFFFFFFF)
    else:
        # buff_size is totally arbitrary, change for your app!
        buff_size = 65536  # lets read stuff in 64kb chunks!

        md5 = hashlib.md5()
        sha1 = hashlib.sha1()

        with open(target_file, 'rb') as f:
            while True:
                data = f.read(buff_size)
                if not data:
                    break
                else:
                    if sum_type == 'md5':
                        md5.update(data)
                    elif sum_type == 'sha1':
                        sha1.update(data)
        if checksum == 'md5':
            print("MD5: {0}".format(md5.hexdigest()))
            return md5.hexdigest()
        elif checksum == 'sha1':
            print("SHA1: {0}".format(sha1.hexdigest()))
            return sha1.hexdigest()


def worker(dir_path, counter):
    print('{}\nРаботаем с {}'.format(80 * '=', dir_path))
    if not os.path.isfile(os.path.join(dir_path, "ФОРМУЛЯР_НОСИТЕЛЯ.txt")):
        t = time.time()
        for f in os.listdir(dir_path):
            print('Расчитываем {checksum} для файла {f_name}...'.format(checksum=checksum, f_name=f))
            with open(os.path.join(dir_path, "ФОРМУЛЯР_НОСИТЕЛЯ.txt"), 'a') as log_f:
                log_f.write('{}={};\n'.format(f, get_checksum(os.path.join(dir_path, f), checksum)))
            counter -= 1
            print(
                "Готово. Осталось файлов: {}\n".format(counter))
        print('Затрачено времени на папку: {} c'.format(round(time.time() - t, 1), ))

file_count = 0
for _, dirs, files in os.walk(root_dir):
    file_count += len(files)


for root, dirnames, filenames in os.walk(root_dir):
    done_counter = 0
    if not dirnames:
        worker(root, file_count)
    else:
        for dirpath in [os.path.join(root, dirname) for dirname in dirnames]:
            worker(dirpath, file_count)

# input("\nГотово, насяльника! Нажми любую кнопку для завершениянама...")
