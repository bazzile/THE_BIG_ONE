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
links_file = r"U:\ОТА\ЯНАО17\Data\Imagery\Sentinel\подбор для мозаики\Ямальский\Спсиок сцен Ямальский3.txt"
out_folder = r"U:\ОТА\ЯНАО17\Data\Imagery\Sentinel\подбор для мозаики\Ямальский\p3"

with open(links_file) as f:
    d_link_list = f.read().splitlines()
# d_link_list = [r'http://sentinel-s2-l1c.s3-website.eu-central-1.amazonaws.com/#tiles/42/X/WG/2016/7/3/0/']
total = len(d_link_list)
for i, d_link in enumerate(d_link_list):
    print(i + 1, '/', total, ' downloading ', d_link)

    base_part = 'http://sentinel-s2-l1c.s3.amazonaws.com/tiles'
    tile_num = d_link.split('#tiles')[1]
    with urllib.request.urlopen(base_part + tile_num + 'productInfo.json') as url:
        data = json.loads(url.read().decode())
        prod_id = data['name'].rsplit('T')[0]
        print(prod_id)
    dst_subdir = os.path.join(out_folder, prod_id, tile_num[1:8].replace('/', '_'))
    if not os.path.exists(dst_subdir):
        os.makedirs(dst_subdir)
    items = ['B02.jp2', 'B03.jp2', 'B04.jp2', 'metadata.xml', 'preview.jp2', 'productInfo.json', 'tileInfo.json']
    for item in items:
        full_link = base_part + tile_num + item
        print('Downloading...   ' + item)
        urllib.request.urlretrieve(full_link, os.path.join(dst_subdir, item))
print('\nГотово!')
