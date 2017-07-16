import os
import shutil

root_path = r"E:\LS8_Taz\espa-lobanov@innoter.com-0101707127583"

for dirpath, dirnames, filenames in os.walk(root_path):
    for filename in filenames:
        if filename.endswith('MTL.txt'):
            filepath = os.path.join(dirpath, filename)
            with open(filepath) as f:
                lines = f.read().splitlines()
                lines = [line.replace('T1_B', 'T1_sr_band') for line in lines]
                lines = [line.replace('T1_sr_bandQA', 'T1_pixel_qa') for line in lines]
                del lines[54:58]
            shutil.move(filepath, filepath.replace('MTL.txt', 'MTL_original.txt'))
            with open(filepath, 'w') as f1:
                f1.write('\n'.join(lines))

