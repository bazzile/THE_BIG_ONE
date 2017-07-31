import os
import ftplib
import re
import shutil
from io import BytesIO

""".EOT - End of Transfer File. The end of transfer file is included with electronic (FTP) deliveries only. The 
appearance of this file on the FTP site indicates that DigitalGlobe has completed transferring all product files. It 
is a zero length file. https://dg-cms-uploads-production.s3.amazonaws.com/uploads/document/file/106/ISD_External.pdf """

out_dir = r"Y:\DG_download"

ftp = ftplib.FTP(host="ftp2.digitalglobe.com", user='xferInnoter', passwd='~6-SpvIuy->oQ0nL')
ftp.cwd('')

try:
    files = ftp.nlst()
except ftplib.error_perm as resp:
    if str(resp) == "550 No files found":
        print("No files in this directory")
    else:
        raise

download_list_full = []
# getting fully uploaded product list from ftp
print('Запрашиваем список продуктов, полностью загруженых на FTP...')
for f in files:
    if re.match(r'.*EOT\.TXT$', f, re.IGNORECASE) is not None:
        download_list_full.append(f)
total_items = len(download_list_full)
print('Готово, всего готовых продуктов на FTP: {}'.format(total_items))

# getting a list of products that's been already downloaded
print('Проверяем, какие продукты уже загружены в {}...'.format(out_dir))
ready_list = []

# checking for unfinished / interrupted downloads from previous sessions
downloading_flag = '.downloading_now'
for file in os.listdir(out_dir):
    if file.endswith(downloading_flag):
        unfinished_floder = file.split(downloading_flag)[0]
        shutil.rmtree(os.path.join(out_dir, unfinished_floder))
        os.remove(os.path.join(out_dir, file))

for dirpath, dirnames, filenames in os.walk(out_dir):
    for dirname in dirnames:
        if re.match(r'^\d{12}_\d{2}$', dirname) is not None:
            ready_list.append(dirname)

refined_download_list = [item for item in download_list_full if item.rstrip('_EOT.TXT') not in ready_list]
items_to_download_counter = len(refined_download_list)

for item in refined_download_list:
    down_filepath = os.path.join(out_dir, item.rstrip('_EOT.TXT') + downloading_flag)
    down_file = open(down_filepath, 'w').close()
    print('\n{} / {} продуктов уже загружено, продолжаем загрузку...'
          .format(total_items - items_to_download_counter, total_items))
    r = BytesIO()
    # item.replace("_EOT.TXT", ".MAN") is used beacuse EOT is just a flag-file, and MAN contains contents
    ftp.retrbinary('RETR %s' % item.replace("_EOT.TXT", ".MAN"), r.write)
    manifest_list = r.getvalue().decode("utf-8")
    # skipping MAN file and foldername
    for line in manifest_list.splitlines():
        if '.' in line.split(r'/')[-1]:
            assert line[:2] == './'
            relfile_path = line[2:]
            dst_filepath = os.path.join(out_dir, relfile_path)
            if not os.path.exists(os.path.dirname(dst_filepath)):
                os.makedirs(os.path.dirname(dst_filepath))
            print('Скачиваем {}...'.format(relfile_path))
            ftp.retrbinary("RETR %s" % line, open(dst_filepath, 'wb').write)
    r.close()
    os.remove(down_filepath)
    items_to_download_counter -= 1
ftp.quit()
print("\nГотово! Все данные ({}) успешно загружены в {}".format(len(refined_download_list), out_dir))
