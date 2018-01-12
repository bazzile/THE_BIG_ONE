import os
import re
import tarfile

in_dir = r'V:\AW30D30\BASIC'
out_dir = r'U:\PRJ\2017\BANS17\1_QuickWork\4_DEM\ALL\src_TIF'

counter = 0
for rootpath, dirnames, filenames in os.walk(in_dir):
    for filename in filenames:
        if filename.lower().endswith('.tar'):
            with tarfile.open(os.path.join(rootpath, filename)) as tar:
                for member in tar.getmembers():
                    if os.path.exists(os.path.join(out_dir, member.name)):
                        print('File already extracted, skipping')
                    else:
                        if member.isreg():  # skip if the TarInfo is not files
                            if re.search(r'(.)*_AVE_DSM\.tif', member.name, re.IGNORECASE):
                                counter += 1
                                print('Extracting {} ({} files extracted total)'.format(member.name, counter))
                                # excluding internal path
                                member.name = os.path.basename(member.name)
                                tar.extract(member, path=out_dir)
