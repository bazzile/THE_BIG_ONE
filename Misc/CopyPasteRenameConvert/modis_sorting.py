import os
import shutil
import datetime
import calendar

in_dir = r"E:\!WORK\MODIS"
out_dir = r"E:\MODIS_sorted\batch_hdf\others"

if not os.path.exists(out_dir):
    os.mkdir(out_dir)


def JulianDate_to_datetime(y, jd):
    month = 1
    day = 0
    while jd - calendar.monthrange(y, month)[1] > 0 and month <= 12:
        jd = jd - calendar.monthrange(y, month)[1]
        month += 1
    datetime_obj = datetime.datetime.strptime(str(y) + str(month) + str(jd), '%Y%m%d')
    return datetime_obj


def convert_to_ddmmmyyyy(filepath):
    filename = os.path.basename(filepath)
    product_year = int(filename.split('.')[1][1:5])
    product_julian_date = int(filename.split('.')[1][5:8])
    product_start_datetime = JulianDate_to_datetime(product_year, product_julian_date)
    product_end_datetime = product_start_datetime + datetime.timedelta(days=15)
    os.rename(
        filepath, os.path.join(os.path.dirname(filepath), 'NDVI_' + product_start_datetime.strftime('%d%b') +
                               '_' + product_end_datetime.strftime('%d%b%Y') + '.tif'))

for path, dirnames, filenames in os.walk(in_dir):
    for filename in filenames:
        # if filename.endswith('.hdf'):
            convert_to_ddmmmyyyy(os.path.join(path, filename))
    #         product_level = filename.split('.')[0]
    #         product_year = int(filename.split('.')[1][1:5])
    #         product_julian_date = int(filename.split('.')[1][5:8])
    #         product_start_datetime = JulianDate_to_datetime(product_year, product_julian_date)
    #         product_end_datetime = product_start_datetime + datetime.timedelta(days=15)
    #         # print(product_year, product_julian_date, product_start_datetime, product_start_datetime.strftime('%d%b%Y'),
    #         #       product_end_datetime.strftime('%d%b%Y'))
    #         dst_path = os.path.join(out_dir, product_level, str(product_year), product_start_datetime.strftime('%Y.%m.%d') +
    #                                 '_' + product_end_datetime.strftime('%Y.%m.%d'))
    #         if not os.path.exists(dst_path):
    #             os.makedirs(dst_path)
    #         shutil.move(os.path.join(path, filename), os.path.join(dst_path, filename))
    # for filename in filenames:
    #     if filename.endswith('.hdf'):
    #         print(filename)
    #         product_year = int(filename.split('.')[1][1:5])
    #         dst_dirpath = os.path.join(out_dir, str(product_year))
    #         if not os.path.exists(dst_dirpath):
    #             os.makedirs(dst_dirpath)
    #         shutil.move(os.path.join(path, filename), os.path.join(dst_dirpath, filename))
    # prm file creation
    # for dirname in dirnames:
    #     if any(fname.endswith('.hdf') for fname in os.listdir(os.path.join(path, dirname))):
    #         print(dirname)
    #         with open(os.)
    #         for tile_image in os.listdir(os.path.join(path, dirname)):
    #             if tile_image.endswith('.hdf'):
    #                 print(tile_image)
# shutil.rmtree(in_dir)
