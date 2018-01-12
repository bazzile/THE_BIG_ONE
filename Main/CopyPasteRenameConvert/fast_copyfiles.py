import os
import re
import shutil


src_dir = r'V:\AW30D30\01_TIFF'
dst_dir = r'F:\SE'

counter = 0
for file in os.listdir(src_dir):
    if re.search(r'^S\d*E\d*.*\.tif$', file, re.IGNORECASE) is not None:
        counter += 1
        print(file, counter)
        shutil.copyfile(os.path.join(src_dir, file), os.path.join(dst_dir, file))
