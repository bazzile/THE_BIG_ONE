import os
import shutil

# def s2_tile_rename(in_file):


in_dir = r"U:\ОТА\ЯНАО17\Data\Imagery\Sentinel\подбор для мозаики\Тазовский"
for dirpath, dirnames, filenames in os.walk(in_dir):
    for filename in filenames:
        if filename == 'tileInfo.json':
            # if filename.endswith('_preview.jp2'):
            filepath = os.path.join(dirpath, filename)
            # os.remove(filepath)
            print('Processing ' + filepath)
            id_0 = os.path.basename(os.path.dirname(filepath))
            id_1 = os.path.basename(os.path.dirname(os.path.dirname(filepath)))
            id = id_1.split('_')[-1] + '_' + id_0
            shutil.copyfile(filepath, os.path.join(os.path.dirname(filepath), id + '_tileInfo.json'))

