#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import xml.etree.ElementTree as ET
# TODO разобраться с TEMPLATE (скорее всего, получится больше текста)
from string import Template

src_file = r"C:\Users\lobanov\PycharmProjects\THE_BIG_ONE\Helper\BKA\QL\13_BKA15\Previews - from 20.05.2016\Previews - from 20.05.2016.kml"
dst_dir = os.path.dirname(src_file)

tree = ET.parse(src_file)
root = tree.getroot()

q = root.findall(".//GroundOverlay")

# print(len(q))

filename = q[0].find(".//href").text
print(filename)
coords_str = q[0].find(".//coordinates").text
# преобразуем строку с координатами углов в список и разбиваем по 4 точкам
coords_lst = coords_str.split('\n')
c1 = coords_lst[3]
c2 = coords_lst[0]
c3 = coords_lst[1]
c4 = coords_lst[2]
print c1, c2, c3, c4

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
    file_name=filename, map_coords1=c1, map_coords2=c2, map_coords3=c3, map_coords4=c4,
    img_hight=str(518), img_width=str(516))

with open(os.path.join(dst_dir, filename.split('.')[0] + '.tab'), 'w') as f:
    f.write(text_content.strip())
