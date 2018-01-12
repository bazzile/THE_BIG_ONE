import os
from collections import Counter
import shutil

src_path = r'U:\PRJ\2017\BANS17\1_QuickWork\4_DEM\ALL\src_TIF\10'

duplicate_fname_list = [file for file, n in Counter(
    [os.path.splitext(file)[0] for file in os.listdir(src_path)]).items() if n > 1]
print(duplicate_fname_list)

if len(duplicate_fname_list) > 0:
    duplicate_dir = os.path.join(src_path, 'ready')
    if not os.path.exists(duplicate_dir):
        os.mkdir(duplicate_dir)

    for file in os.listdir(src_path):
        if os.path.splitext(file)[0] in duplicate_fname_list:
            shutil.move(os.path.join(src_path, file), os.path.join(duplicate_dir, file))
else:
    print('Файлов-дубликатов не обнаружено')

