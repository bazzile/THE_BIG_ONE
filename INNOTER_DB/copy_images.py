import os
import shapefile
import shutil


shp = shapefile.Reader(r"E:\!Go\!Arctic\Islands\OUR_DB\Our_Arctic.shp")
for x in range(len(shp.fields)):
    print(x, shp.fields[x])

counter = 0
seen_paths = set()
err_list = []
for image in shp.records():
    counter += 1
    print('Копируем файл {} из {}\n'.format(counter, len(shp.records())))
    gsd = image[10]
    path = image[-2]
    useful_path = os.path.dirname(path)
    # у pan и ms одинаковые корневые директории. Чтобы не возникало конфликтов перезаписи, проверяем на дубликаты
    try:
        if useful_path not in seen_paths:
            seen_paths.add(useful_path)
            if gsd == 4.0:
                shutil.copytree(os.path.dirname(path), os.path.join(r"U:\PRJ\2016\ARCTIC14\IMAGERY4", os.path.basename(os.path.dirname(path))))
                # print(path, os.path.join(r'U:\\PRJ\2016\ARCTIC14\IMAGERY4', os.path.basename(path)))
            elif gsd == 0.5 or gsd == 0.6:
                shutil.copytree(os.path.dirname(path), os.path.join(r"U:\PRJ\2016\ARCTIC14\IMAGERY05", os.path.basename(os.path.dirname(path))))
                # print(path, os.path.join(r'U:\PRJ\2016\ARCTIC14\IMAGERY05', os.path.basename(path)))
            else:
                err_list.append(image)
    except FileExistsError:
        continue
print(len(seen_paths))
print(err_list)
