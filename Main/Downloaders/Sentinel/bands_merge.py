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

user_sat_input = raw_input("Select satellite: Sentinel-2 or Landsat-8. Type (S/L):")\
    .decode(sys.stdin.encoding or locale.getpreferredencoding(True)).upper()
# python 3
# user_sat_input = input("Select satellite: Sentinel-2 or Landsat-8. Type (S/L):").upper()
if user_sat_input == 'S':
    sat = 'Sentinel-2'
elif user_sat_input == 'L':
    sat = 'Landsat-8'
else:
    print('Received wrong input, terminating...')
    exit()

user_path_input = raw_input("Enter the path to {satellite} files root folder: ".format(satellite=sat))\
    .decode(sys.stdin.encoding or locale.getpreferredencoding(True))
# python 3
# user_path_input = input("Enter the path to {satellite} files root folder: ".format(satellite=sat))

assert os.path.exists(user_path_input), "I did not find the file at, " + str(user_path_input)
root_folder = user_path_input
print('Path found, looking for {satellite} bands...'.format(satellite=sat))

for dirpath, dirnames, filenames in os.walk(root_folder):
    for dirname in dirnames:
        dir_path = os.path.join(dirpath, dirname)
        if sat == 'Sentinel-2':
            if any(re.match(r'.*B\d{2}\.jp2', f) for f in os.listdir(dir_path)):
                id_0 = dirname
                id_1 = os.path.basename(os.path.dirname(dir_path))
                id = id_1.split('_')[-1] + '_' + id_0
                out_file_name = id + '.tif'
                print(dir_path, id, out_file_name)
                bands = [os.path.join(dir_path, band + '.jp2') for band in ['B02', 'B03', 'B04']]
                print('Merging ' + dir_path)
                gdal_merge.main(['', '-separate', '-o', os.path.join(dir_path, out_file_name), bands[-1], bands[-2], bands[-3]])
        elif sat == 'Landsat-8':
            if any(re.match(r'LC08.*B\d{1,2}\.TIF', f) for f in os.listdir(dir_path)):
                id_0 = dirname
                sat_id, path_row, date = id_0.split('_')[0], id_0.split('_')[2], id_0.split('_')[3]
                id = '_'.join((sat_id, path_row, date))
                band_ids = ['B2', 'B3', 'B4']
                bands = [os.path.join(dir_path, id_0 + '_' + band + '.TIF') for band in band_ids]
                out_file_name = id + '_' + ''.join(list(reversed(band_ids))).replace('B', '') + '_merged' + '.tif'
                print(dir_path, id, out_file_name)
                print('Merging ' + dir_path)
                gdal_merge.main(['', '-separate', '-o', os.path.join(dir_path, out_file_name), bands[-1], bands[-2], bands[-3]])