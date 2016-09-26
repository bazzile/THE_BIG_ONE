import os

src_dir = r"E:\!WORK\Kravtsov\Tomsk_n_v1_QGIS\reproj\shp2tab"

for path, dirnames, filenames in os.walk(src_dir):
    for filename in filenames:
        # print(filename[9:])
        os.rename(os.path.join(path, filename), os.path.join(path, filename[9:]))
