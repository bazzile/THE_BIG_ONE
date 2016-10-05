#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import xml.etree.ElementTree as ET
# TODO разобраться с TEMPLATE (скорее всего, получится больше текста)
from string import Template

src_file = r"E:\GitHub\the_big_one\Helper\BKA\QL\13_BKA15\Previews - from 20.05.2016\Previews - from 20.05.2016.kml"
dst_dir = os.path.dirname(src_file)

tree = ET.parse(src_file)
root = tree.getroot()

q = root.findall(".//GroundOverlay")

# print(len(q))

filename = q[0].find(".//href").text
print(filename)
print(q[0].find(".//coordinates").text)

with open(os.path.join(dst_dir, filename.split('.')[0] + '.tab'), 'w') as f:
    # TODO достать пример таблицы для растрового файла
    # TODO запросить у Димы пример названия выходного файла (306361-306371.Jpeg / 306361_306370quicklook_306361_306370_1.Jpeg)
    lines = ['!table', '!version 300', '!charset WindowsLatin1', '', 'Definition Table']
    f.writelines("\n".join(lines))
