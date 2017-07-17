#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import requests
import time


def alos_ql_downloader():
    """Функция скачивает квиклуки для ALOS, используя в качестве исходных данных ссылки из 2х .txt-листов:
    main_links_filepath = основной файл со ссылками,
    auxl_links_filepath = резервный (на случай 404) файл со ссылками
    По окончанию в файл report_file записывается список ссылок от незагруженных квиклуков."""
    dir = os.path.dirname(__file__)

    main_links_filepath = os.path.join(dir, 'ALOS_data', 'AL04B.txt')
    auxl_links_filepath = os.path.join(dir, 'ALOS_data', 'AL05B.txt')
    report_file = os.path.join(dir, 'ALOS_data', u'Отчёт.txt')

    dst_dir = os.path.join(dir, 'ALOS_data', 'Downloads')

    if not os.path.exists(dst_dir):
        os.mkdir(dst_dir)
    err_links_list = []

    with open(main_links_filepath) as f1:
        main_links_list = [line.strip() for line in f1.readlines()]
    with open(auxl_links_filepath) as f2:
        auxl_links_list = [line.strip() for line in f2.readlines()]

    for x in range(len(main_links_list) - 1):
        print('Скачиваем файл {} из {}'.format(x + 1, len(main_links_list) - 1))
        filename = main_links_list[x].rsplit('/')[-1]
        assert filename == auxl_links_list[x].rsplit('/')[-1]
        if filename not in os.listdir(dst_dir):
            with open(os.path.join(dst_dir, filename), 'wb') as img_f:
                r = requests.get(auxl_links_list[x])
                try:
                    r.raise_for_status()
                    img_f.write(r.content)
                    print('{0} quicklooks downloaded'.format(x + 1))
                    time.sleep(0)
                except requests.HTTPError:
                    r = requests.get(main_links_list[x])
                    try:
                        r.raise_for_status()
                        img_f.write(r.content)
                        print('{0} quicklooks downloaded'.format(x + 1))
                        time.sleep(0)
                    except requests.HTTPError:
                        err_links_list.append(auxl_links_list[x])
        else:
            print('{} уже скачан, пропускаем'.format(filename))
    with open(report_file, 'w') as rf:
        rf.writelines(err_links_list)


alos_ql_downloader()
