import os
import urllib.request

download_file = r"E:\MODIS_appeears\2000_2003\yanao17_full_2000_2003-download-list.txt"
out_folder = r'E:\MODIS_appeears\2000_2003'
with open(download_file) as d_file:
    links_list = d_file.readlines()
    n_items = len(links_list)
    for count, item_http_link in enumerate(links_list):
        fname = item_http_link.split('/')[-1].replace('_aid0001', '').rstrip()
        print(count + 1, '/', n_items, fname)
        urllib.request.urlretrieve(item_http_link.rstrip(), os.path.join(out_folder, fname))
