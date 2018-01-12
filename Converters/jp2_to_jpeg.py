import os
import PIL

from PIL import Image

src_dir = r'U:\PRJ\2017\YANAO17\2_Data\1_Imagery\Sentinel\period_2'

for root_path, dirnames, filenames in os.walk(src_dir):
    for filename in filenames:
        if filename.lower().endswith('_preview.jp2'):
            print(filename)
            with Image.open(os.path.join(root_path, filename)) as im:
                im.save(os.path.join(root_path, filename.replace('.jp2', '.jpg')))
