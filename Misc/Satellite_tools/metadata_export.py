import os
import re

root_folder = os.path.dirname(os.path.abspath(__file__))
out_dir = root_folder

parameter_list = ['LANDSAT_PRODUCT_ID', 'DATE_ACQUIRED', 'SPACECRAFT_ID',
                  'CLOUD_COVER_LAND', 'GRID_CELL_SIZE_PANCHROMATIC', 'GRID_CELL_SIZE_REFLECTIVE']

scene_list = []
for rootdir, dirnames, filenames in os.walk(root_folder):
    for filename in filenames:
        if re.match(r'.*_MTL\.txt', filename, re.IGNORECASE) is not None:
            with open(os.path.join(rootdir, filename), 'r') as f:
                d = {}
                for line in f.read().splitlines():
                    for parameter in parameter_list:
                        if parameter in line:
                            d[parameter] = line.split('=')[1].strip()
            scene_list.append(d)
# sorting list of dictionaries by LANDSAT_PRODUCT_ID key
sorted_scene_list = sorted(scene_list, key=lambda k: k['LANDSAT_PRODUCT_ID'])
with open(os.path.join(out_dir, 'scene_info.txt'), 'w') as of:
    csv_list = []
    header = parameter_list
    of.write(', '.join(parameter_list) + '\n')
    for scene in sorted_scene_list:
        of.write(', '.join(
            [scene[parameter] for parameter in
             parameter_list]) + '\n')

