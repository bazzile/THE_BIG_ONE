import os
import re

root_folder = os.path.dirname(os.path.abspath(__file__))

for rootdir, dirnames, filenames in os.walk(root_folder):
    for filename in filenames:
        if re.match(r'.*_MTL\.txt', filename, re.IGNORECASE) is not None:
            print(filename)