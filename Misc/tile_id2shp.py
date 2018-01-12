import os
import re
import tarfile
import shapefile

in_dir = r'V:\POKROV\03_AW3D30_11\1_AVE'
out_dir = r'V:\POKROV\03_AW3D30_11\4_VEC'


def id2shp(tile_id_list, dst_shape_filepath):
    polygon_type_index = 5
    w = shapefile.Writer(shapeType=polygon_type_index)
    w.field('tile_id', fieldType='C', size=20)
    for tile_id in tile_id_list:
        sign_lat = -1 if tile_id[:1] == 'S' else 1
        sign_lon = -1 if tile_id[4:5] == 'W' else 1
        ll_lat = sign_lat * int(tile_id[1:4])
        ll_lon = sign_lon * int(tile_id[5:8])
        w.poly(parts=[[[ll_lon, ll_lat], [ll_lon, ll_lat + 1], [ll_lon + 1, ll_lat + 1], [ll_lon + 1, ll_lat]]])
        w.record(tile_id)
    w.save(dst_shape_filepath)


counter = 0
id_list = []
for rootpath, dirnames, filenames in os.walk(in_dir):
    for filename in filenames:
        if filename.lower().endswith('.tar'):
            with tarfile.open(os.path.join(rootpath, filename)) as tar:
                for member in tar.getmembers():
                    if member.isreg():  # skip if the TarInfo is not files
                        if re.search(r'(.)*_AVE_DSM\.tif', member.name, re.IGNORECASE):
                            counter += 1
                            print('Appending {} ({} files appended in total)'.format(member.name, counter))
                            # excluding internal path
                            member.name = os.path.basename(member.name)
                            id_list.append(member.name)
        else:
            if re.search(r'(.)*_AVE_DSM\.tif', filename, re.IGNORECASE):
                counter += 1
                print('Appending {} ({} files appended in total)'.format(filename, counter))
                id_list.append(filename)
id2shp(id_list, os.path.join(out_dir, 'tile_id_new.shp'))
