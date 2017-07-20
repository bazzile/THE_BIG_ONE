import os
import re

root_folder = os.path.dirname(os.path.abspath(__file__))
scene_list = []
for rootdir, dirnames, filenames in os.walk(root_folder):
    for filename in filenames:
        if re.match(r'.*_MTL\.txt', filename, re.IGNORECASE) is not None:
            with open(os.path.join(rootdir, filename), 'r') as f:
                d = {}
                for line in f.read().splitlines():
                    for parameter in ['LANDSAT_PRODUCT_ID', 'DATE_ACQUIRED', 'SPACECRAFT_ID',
                                      'CLOUD_COVER_LAND', 'GRID_CELL_SIZE_PANCHROMATIC', 'GRID_CELL_SIZE_REFLECTIVE']:
                        if parameter in line:
                            d[parameter] = line.split('=')[1].strip()
                print(d)
