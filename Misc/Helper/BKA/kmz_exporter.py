#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import zipfile
import shutil
in_kmz = r"E:\GitHub\the_big_one\Helper\BKA\QL\13_BKA15\Previews - from 20.05.2016.kmz"
out_folder = r"E:\GitHub\the_big_one\Helper\BKA\QL\13_BKA15\out"
with zipfile.ZipFile(in_kmz) as z:
    for filename in z.namelist():
        if filename.endswith(('.Jpeg', '.jpg')):
            print(type(filename))
            with z.open(filename) as zippd_ql, open(os.path.join(out_folder, '1.jpg'), 'wb') as f:
                shutil.copyfileobj(zippd_ql, f)
                break
            # z.extract(filename, out_folder)
            # # read the file
            # with z.open(filename) as f:
            #     for line in f:
            #         print line