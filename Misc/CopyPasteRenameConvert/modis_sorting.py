import os
import shutil
import datetime
import calendar

in_dir = r"U:\ОТА\ЯНАО17\Data\Imagery\MODIS\NDVI\14562"
out_dir = r"U:\ОТА\ЯНАО17\Data\Imagery\MODIS\NDVI\MODIS_sorted"

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

# JulianDate_to_MMDDYYY(2008, 167)

product_levels = []
for path, dirnames, filenames in os.walk(in_dir):
    for filename in filenames:
        product_level = filename.split('_')[0]
        product_year = int(filename.split('_')[1][1:5])
        product_julian_date = int(filename.split('_')[1][5:8])
        product_start_datetime = JulianDate_to_datetime(product_year, product_julian_date)
        product_end_datetime = product_start_datetime + datetime.timedelta(days=15)
        # print(product_year, product_julian_date, product_start_datetime, product_start_datetime.strftime('%d%b%Y'),
        #       product_end_datetime.strftime('%d%b%Y'))
        dst_path = os.path.join(out_dir, product_level, str(product_year), product_start_datetime.strftime('%Y.%m.%d') +
                                '_' + product_end_datetime.strftime('%Y.%m.%d'))
        if not os.path.exists(dst_path):
            os.makedirs(dst_path)
        shutil.move(os.path.join(path, filename), os.path.join(dst_path, filename))
shutil.rmtree(in_dir)
