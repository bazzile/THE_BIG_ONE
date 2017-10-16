import os
import sentinelhub


# TODO сделать збс

os.chdir(r"E:\!temp\s2_open_test\S2A_MSIL1C_20170817\41_X_PA\SAFE")

tile_id = '41XPA'

sentinelhub.download_safe_format(tile=('T{tile_id}'.format(tile_id=tile_id.upper()), '2017-08-17'))