import os
import re


in_folder = r"E:\!temp\Alex\Партии"
out_folder = os.path.join(in_folder, 'output')
if not os.path.exists(out_folder):
    os.mkdir(out_folder)
for file in [file for file in os.listdir(in_folder) if file.endswith('.txt')]:
    with open(os.path.join(in_folder, file), 'r', encoding='CP1251') as in_file:
        corrected_quad_list = []
        for line in in_file.readlines():
            print(re.sub(r'-0', r'-', line.rstrip()))
            corrected_quad_list.append("'" + re.sub(r'-0', r'-', line.rstrip()) + "'")
        with open(os.path.join(out_folder, file), 'w') as out_file:
            out_file.write(', \n'.join(corrected_quad_list))
