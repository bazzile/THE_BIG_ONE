import os
import re

# root_folder = os.path.dirname(os.path.abspath(__file__))
root_folder = r'U:\ОТА\ЯНАО17\Data\Imagery\Sentinel\подбор для мозаики\Тазовский'
out_dir = root_folder

# product = input('Please choose product type: \nLandsat-8 C1 [L]\nSentinel-2 L1C from AWS [S]\nYour choice: ').upper()
product = 'S'

if product == 'L':
    regex = r'.*_MTL\.txt'
    separator = '='
    parameter_list = ['LANDSAT_PRODUCT_ID', 'DATE_ACQUIRED', 'SPACECRAFT_ID',
                      'CLOUD_COVER_LAND', 'GRID_CELL_SIZE_PANCHROMATIC', 'GRID_CELL_SIZE_REFLECTIVE']
    sorting_parameter = 'DATE_ACQUIRED'
elif product == 'S':
    regex = r'tileInfo.json'
    separator = ' : '
    parameter_list = ["productName", "timestamp", "cloudyPixelPercentage", "utmZone", "latitudeBand", "gridSquare"]
    sorting_parameter = "timestamp"
else:
    raise Exception('Wrong parameter')

scene_list = []
for rootdir, dirnames, filenames in os.walk(root_folder):
    for filename in filenames:
        if re.match(regex, filename, re.IGNORECASE) is not None:
            with open(os.path.join(rootdir, filename), 'r') as f:
                d = {}
                for line in f.read().splitlines():
                    for parameter in parameter_list:
                        if parameter in line:
                            d[parameter] = line.split(separator)[1].strip().replace('"', '').replace(',', '')
            scene_list.append(d)
# sorting list of dictionaries by sorting_parameter (i.e. LANDSAT_PRODUCT_ID) key
sorted_scene_list = sorted(scene_list, key=lambda k: k[sorting_parameter], reverse=True)
with open(os.path.join(out_dir, 'scene_info.csv'), 'w') as of:
    header = parameter_list
    of.write(', '.join(parameter_list) + '\n')
    for scene in sorted_scene_list:
        print(scene)
        of.write(', '.join(
            [scene[parameter] for parameter in
             parameter_list]) + '\n')
