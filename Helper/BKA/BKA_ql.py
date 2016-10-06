#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import shutil
import xml.etree.ElementTree as ET
# TODO разобраться с TEMPLATE (скорее всего, получится больше текста)
from string import Template
from PIL import Image

src_file = r"C:\Users\lobanov\PycharmProjects\THE_BIG_ONE\Helper\BKA\QL\13_BKA15\Previews - from 20.05.2016\Previews - from 20.05.2016.kml"

# TODO далее-временный блок, удалить, как только разберёшься выгрузке из сырого kmz
temp_extracted_dir = os.path.dirname(src_file)

dst_dir_name = 'QuickLooks'
dst_dir_path = os.path.join(os.path.dirname(src_file), dst_dir_name)

if not os.path.exists(dst_dir_path):
    os.makedirs(dst_dir_path)

# парсим kml
tree = ET.parse(src_file)
root = tree.getroot()

q = root.findall(".//GroundOverlay")

# print(len(q))

ql_filename = q[0].find(".//href").text
standard_ql_name = ql_filename[:13]
ql_path = os.path.join(dst_dir_path, standard_ql_name + '.jpg')
shutil.copy(os.path.join(temp_extracted_dir, ql_filename), ql_path)
ql_image_obj = Image.open(ql_path)
ql_width, ql_height = ql_image_obj.size[0], ql_image_obj.size[1]
coords_str = q[0].find(".//coordinates").text
# преобразуем строку с координатами углов в список и разбиваем по 4 точкам
coords_lst = coords_str.split('\n')
c1, c2, c3, c4 = coords_lst[3], coords_lst[0], coords_lst[1], coords_lst[2]

text_content = Template("""
!table
!version 300
!charset WindowsCyrillic

Definition Table
  File "$file_name"
  Type "RASTER"
  ($map_coords1)  (0.0,0.0) Label "Point 1",
  ($map_coords2)  (0.0,$img_hight.0) Label "Point 2",
  ($map_coords3)  ($img_width.0,$img_hight.0) Label "Point 3",
  ($map_coords4)  ($img_width.0,0.0) Label "Point 4"
 CoordSys Earth Projection 1, 0
""")
text_content = text_content.substitute(
    file_name=standard_ql_name + '.jpg', map_coords1=c1, map_coords2=c2, map_coords3=c3, map_coords4=c4,
    img_hight=str(ql_height), img_width=str(ql_width))

with open(os.path.join(dst_dir_path, standard_ql_name + '.tab'), 'w') as f:
    f.write(text_content.strip())
