# -*- coding: utf-8 -*-

"""go to OSGEO4W/bin and launch python-qgis.bat in cmd then
import sys
sys.path.append('path to this module')
import bands_merge"""
import locale
import os
import re
import sys

import gdal_merge

print('Model imported successfully!')
user_input = raw_input("Enter the path to Sentinel-2 files root folder: ")\
    .decode(sys.stdin.encoding or locale.getpreferredencoding(True))

assert os.path.exists(user_input), "I did not find the file at, "+str(user_input)
root_folder = user_input
print('Path found, looking for Sentinel-2 files...')

for dirpath, dirnames, filenames in os.walk(root_folder):
    for dirname in dirnames:
        dir_path = os.path.join(dirpath, dirname)
        if any(re.match(r'.*B\d{2}\.jp2', f) for f in os.listdir(dir_path)):
            id_0 = dirname
            id_1 = os.path.basename(os.path.dirname(dir_path))
            id = id_1.split('_')[-1] + '_' + id_0
            out_file_name = id + '.tif'
            print(dir_path, id, out_file_name)
            bands = [os.path.join(dir_path, band + '.jp2') for band in ['B02', 'B03', 'B04']]
            print('Merging ' + dir_path)
            gdal_merge.main(['', '-separate', '-o', os.path.join(dir_path, out_file_name), bands[-1], bands[-2], bands[-3]])