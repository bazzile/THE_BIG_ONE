import os
import urllib.request
import xml.etree.ElementTree as ET
import json


# download_file = r"E:\MODIS_appeears\2000_2003\yanao17_full_2000_2003-download-list.txt"
# out_folder = r'E:\MODIS_appeears\2000_2003'
# with open(download_file) as d_file:
#     links_list = d_file.readlines()
#     n_items = len(links_list)
#     for count, item_http_link in enumerate(links_list):
#         fname = item_http_link.split('/')[-1].replace('_aid0001', '').rstrip()
#         print(count + 1, '/', n_items, fname)
#         urllib.request.urlretrieve(item_http_link.rstrip(), os.path.join(out_folder, fname))
# links_file = r"U:\PRJ\2017\YANAO17\2_Data\1_Imagery\Sentinel\period_2\Спсиок сцен Ямальский 3.txt"
# out_folder = r"U:\PRJ\2017\YANAO17\2_Data\1_Imagery\Sentinel\period_2\Yamalsky\3"
out_folder = r"U:\PRJ\2017\YANAO17\2_Data\1_Imagery\Sentinel\period_2\Tazovsky"
src_folder = r"U:\PRJ\2017\YANAO17\2_Data\1_Imagery\Sentinel\period_2"

for file in os.listdir(src_folder):
    if file.lower().endswith('.txt') and 'тазовский' in file.lower():
        links_file = os.path.join(src_folder, file)
        fragment_number = os.path.splitext(file)[0].split()[-1]
        with open(links_file) as f:
            d_link_list = f.read().splitlines()
        total = len(d_link_list)
        for i, d_link in enumerate(d_link_list):
            print(i + 1, '/', total, ' downloading ', d_link)

            base_part = 'http://sentinel-s2-l1c.s3.amazonaws.com/tiles'
            tile_num = d_link.split('#tiles')[1]
            with urllib.request.urlopen(base_part + tile_num + 'productInfo.json') as url:
                data = json.loads(url.read().decode())
                prod_id = data['name'].rsplit('T')[0]
                print(prod_id)
            dst_subdir = os.path.join(out_folder, fragment_number, prod_id, tile_num[1:8].replace('/', '_'))
            if not os.path.exists(dst_subdir):
                os.makedirs(dst_subdir)
            # items = ['B' + str(i).zfill(2) + '.jp2' for i in range(1, 13)] + \
            #         ['B8A.jp2', 'metadata.xml', 'preview.jp2', 'productInfo.json', 'tileInfo.json']
            items = ['preview.jp2']
            for item in items:
                full_link = base_part + tile_num + item
                print('Downloading...   ' + item)
                dst_file_path = os.path.join(dst_subdir, item)
                if not os.path.exists(dst_file_path):
                    # urllib.request.urlretrieve(full_link, dst_file_path)
                    # add data and tile num to element
                    urllib.request.urlretrieve(
                        full_link, os.path.join(
                            dst_subdir, '_'.join((tile_num[1:8].replace('/', '_'), prod_id.split('_')[-1], item))))
                else:
                    print('File is already downloaded, skipping...')

        print('\nГотово!')
