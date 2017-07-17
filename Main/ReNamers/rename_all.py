import os

src_dir = r"E:\!Projects\963_СНИИГиМС\100k\N-44-040_обновленная_с рельефом_в_рамке_joined"

for dirpath, dirnames, filenames in os.walk(src_dir):
    for filename in filenames:
        print('Renaming {}...'.format(filename))
        os.rename(os.path.join(dirpath, filename), os.path.join(dirpath, filename.replace('-', '_')))
