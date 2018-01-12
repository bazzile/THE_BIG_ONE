import os
import re
import tarfile


def check_archive(archive_name):
    try:
        with tarfile.open(archive_name) as tardude:
            pass
        return True
    except tarfile.ReadError:
        return False

bad_file_list = []
for file in os.listdir(os.curdir):
    if re.search('.*\.tar$', file, re.IGNORECASE) is not None:
        is_good = check_archive(os.path.join(os.curdir, file))
        if not is_good:
            bad_file_list.append(file)

with open('!report.txt', 'w') as f:
    f.write(("\n".join(bad_file_list)))
