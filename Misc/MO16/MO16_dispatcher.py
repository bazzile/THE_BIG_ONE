# -*- coding: utf-8 -*-
import zipfile
import os
import time
import math

elapsed_time = 0


root_dir = r"\\Ws071\f\FOR_BASILE\product_test"
change_root_dir = input('Путь к корневой директории с данными {}\n1 = "Да"\n0 = "Нет, изменить"'.format(root_dir))
if change_root_dir == str(0):
    root_dir = input(r'Введите путь к корневой директории с данными. (Пример: "\\Ws071\f\FOR_BASILE"):  ')

dst_catalog = r"\\Ws071\f\FOR_BASILE\DISKS_test"
change_dst_catalog = input('Путь для сохранения результата: {}\n1 = "Да"\n0 = "Нет, изменить"'.format(dst_catalog))
if change_dst_catalog == str(0):
    dst_catalog = input(r'Введите путь для сохранения результата. (Пример: "\\Ws071\f\FOR_BASILE\DISKS_test"):  ')
print('\n')


def make_archive(dir_to_compress, dst_dir_name, compression=False):
    global elapsed_time
    dst_file = os.path.join(dst_dir_name, os.path.basename(dir_to_compress)) + '.zip'
    print('Создаём архив {}...'.format(os.path.basename(dst_file)))
    if os.path.exists(dst_file):
        print('Архив уже существует, переписываем...')
    #     action_flag = input(
    #         'Архив {} уже существует. Заменить?\n0 = "Нет, пропустить", 1 = "Земенить", 2 = "Заменить все"'.format(
    #             dst_file))
    #     if action_flag == 0:
    #
    start_time = time.time()
    os.chdir(os.path.dirname(dir_to_compress))
    with zipfile.ZipFile(dst_file,
                         "w",
                         zipfile.ZIP_STORED if compression is False else zipfile.ZIP_DEFLATED,
                         allowZip64=True) as zf:
        for root, _, filenames in os.walk(os.path.basename(dir_to_compress)):
            for name in filenames:
                name = os.path.join(root, name)
                name = os.path.normpath(name)
                zf.write(name, name)
        elapsed_time += time.time() - start_time
        print('Архив {} создан, затрачено времени: {} с (всего {} мин.)\n'.format(os.path.basename(
            dir_to_compress), round(time.time() - start_time, 1), round(elapsed_time / 60, 1)))


# Вычисляем нужное количество папок для выходных данных
in_dir_count = 0
for _, dirs, files in os.walk(root_dir):
    in_dir_count += len([os.path.join(_, d) for d in dirs if d.startswith('СТЕРЕОПАРА_')])
out_dir_count = int(math.ceil(in_dir_count / 7))

# Создаём нужное количество папок для выходных данных
# TODO удалять существующие папки с данными или нет?
for i in range(out_dir_count):
    if not os.path.exists(os.path.join(dst_catalog, str(i))):
        os.mkdir(os.path.join(dst_catalog, str(i)))

curr_dir_counter = 0
out_dir_name = 0

for rootpath, dirnames, filenames in os.walk(root_dir):
    for dirpath in sorted([os.path.join(rootpath, d) for d in dirnames if d.startswith('СТЕРЕОПАРА_')]):
        curr_dir_counter += 1
        print('{}/{}'.format(curr_dir_counter, in_dir_count))
        make_archive(dirpath, os.path.join(dst_catalog, str(out_dir_name)), compression=False)
        if curr_dir_counter % 7 == 0:
            out_dir_name += 1

print('{0}\nГотово! Затрачено времени: {1} мин.\nВсего папок создано: {2}\nВсего архивов создано: {3}'.format(
    80 * "#", round(elapsed_time / 60, 1), out_dir_count, curr_dir_counter))

