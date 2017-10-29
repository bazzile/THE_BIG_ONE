import os
import re
import tarfile

in_dir = r'/Users/vasily/!MyFiles/Google Drive/untitled folder'
out_dir = r'/Users/vasily/Desktop/Temp/temp'

counter = 0
for rootpath, dirnames, filenames in os.walk(in_dir):
    for filename in filenames:
        if filename.lower().endswith('.tar'):
            with tarfile.open(os.path.join(rootpath, filename)) as tar:
                for member in tar.getmembers():
                    if re.search(r'(.)*_AVE_DSM\.tif', member.name, re.IGNORECASE):
                        counter += 1
                        print('Extracting {} ({} files extracted total)'.format(member.name, counter))
                        # excluding internal path
                        member.name = os.path.basename(member.name)
                        tar.extract(member, path=out_dir)
