import os
from io import BytesIO
import shapefile
import zipfile


def scanex_archives_export(root_dirname):
    """
    На входе подаётся директория со скачанными с search.kosmosnimki.ru архивами покрытия (root_dirname).
    На выходе - список словарей с метаданными снимка
    """
    img_dict_list = []
    # здесь будут отфильтровываться дубликаты
    seen_images = set()
    for dirpath, dirnames, filenames in os.walk(root_dirname):
        for filename in filenames:
            filename = os.path.join(dirpath, filename)
            if filename.endswith('.zip'):
                with zipfile.ZipFile(filename, 'r') as zfile:
                    for z_filename in zfile.namelist():
                        # в архиве SCANEX должно быть больше 10 файлов
                        if len(zfile.namelist()) < 10:
                            break
                        #  для метаданных PLEIADES
                        if z_filename.endswith('PLEIADES.shp') and 'contours.shp' not in z_filename:
                            myshp = BytesIO(zfile.read(z_filename))
                            myshx = BytesIO(zfile.read(z_filename.replace('shp', 'shx')))
                            mydbf = BytesIO(zfile.read(z_filename.replace('shp', 'dbf')))
                            myprj = BytesIO(zfile.read(z_filename.replace('shp', 'prj')))
                            shp = shapefile.Reader(shp=myshp, shx=myshx, dbf=mydbf, prj=myprj)
                            records = shp.records()
                            for r in records:
                                d = {'vendor_id': r[0], 'date': r[12], 'sat_name': 'PLEIADES',
                                     'off_nadir': r[17], 'sun_elev': r[19], 'cloud_pct': r[15]}
                                if not r[0] in seen_images:
                                    seen_images.add(r[0])
                                    img_dict_list.append(d)
                        # для метаданных DG
                        elif z_filename.endswith('.shp') and 'contours.shp' not in z_filename:
                            myshp = BytesIO(zfile.read(z_filename))
                            myshx = BytesIO(zfile.read(z_filename.replace('shp', 'shx')))
                            mydbf = BytesIO(zfile.read(z_filename.replace('shp', 'dbf')))
                            myprj = BytesIO(zfile.read(z_filename.replace('shp', 'prj')))
                            shp = shapefile.Reader(shp=myshp, shx=myshx, dbf=mydbf, prj=myprj)
                            records = shp.records()
                            # for i in range(len(shp.fields)):
                            #     print(i - 1, "=", shp.fields[i])
                            for r in records:
                                d = {'vendor_id': r[0], 'date': r[10], 'sat_name': r[32],
                                     'off_nadir': r[13], 'sun_elev': r[19], 'cloud_pct': r[31]}
                                if not r[0] in seen_images:
                                    seen_images.add(r[0])
                                    img_dict_list.append(d)
    return img_dict_list

