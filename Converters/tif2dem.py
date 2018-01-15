import os
import subprocess

osgeo_bat_path = r'C:\OSGeo4W64\OSGeo4W.bat'
src_dem = r"S:\!ipython\test\test_dem_conv\!pytest\N000E009_AVE_DSM.tif"
dst_dem = src_dem.split('_AVE_DSM')[0] + '.dem'

command = '{osgeo_path} gdal_translate -of USGSDEM {in_dem} {out_dem}'\
    .format(osgeo_path=osgeo_bat_path, in_dem=src_dem, out_dem=dst_dem)

p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
stdout, stderr = p.communicate()
p.wait()  # wait for process to terminate
print('STDOUT: {}\nSTDERR: {}'.format(stdout.decode("utf-8"), stderr.decode("utf-8")))
