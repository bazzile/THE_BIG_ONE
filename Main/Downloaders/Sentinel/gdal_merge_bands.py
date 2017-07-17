import subprocess

filea = 'C:/Users/claudio/workspace/test/test1/rasa.tif'
fileb = 'C:/Users/claudio/workspace/test/test1/rasb.tif'
output = 'C:/Users/claudio/workspace/test/test1/output.tif'
subprocess.call(['gdal_merge', '-o', output, filea, fileb])



gdalmerge -o /path/foo.tif -separate /path/red_band.jp2 /path/green_band.jp2
/path/blue_band.jp2

