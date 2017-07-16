# coding=utf-8
import os
import zipfile


def ZipShp(inShp, dst_dir=None, Delete=True):
    """
    Creates a zip file containing the input shapefile
    inputs -
    inShp: Full path to shapefile to be zipped
    Delete: Set to True to delete shapefile files after zip
    """

    # List of shapefile file extensions
    extensions = [".shp",
                  ".shx",
                  ".dbf",
                  ".sbn",
                  ".sbx",
                  ".fbn",
                  ".fbx",
                  ".ain",
                  ".aih",
                  ".atx",
                  ".ixs",
                  ".mxs",
                  ".prj",
                  ".xml",
                  ".cpg",
                  ".shp.xml"]

    # Directory of shapefile
    inLocation = os.path.dirname(inShp)
    # Output directory
    if dst_dir is None:
        outLocation = inLocation
    else:
        outLocation = dst_dir
    # Base name of shapefile
    inName = os.path.basename(os.path.splitext(inShp)[0])
    # Create zipfile name
    zipfl = os.path.join(dst_dir, inName + ".zip")
    # Create zipfile object
    ZIP = zipfile.ZipFile(zipfl, "w")

    # Empty list to store files to delete
    delFiles = []

    # Iterate files in shapefile directory
    for fl in os.listdir(inLocation):
        # Iterate extensions
        for extension in extensions:
            # Check if file is shapefile file
            if fl == inName + extension:
                # Get full path of file
                inFile = os.path.join(inLocation, fl)
                # Add file to delete files list
                delFiles += [inFile]
                # Add file to zipfile
                ZIP.write(inFile, fl)
                break

    # Delete shapefile if indicated
    if Delete is True:
        for fl in delFiles:
            os.remove(fl)

    # Close zipfile object
    ZIP.close()

    # Return zipfile full path
    return zipfl

# target_dir = r"U:\ОТА\ЯНАО17\Data\Vector\AOI\Районы от Анны\zip\simplified\Anna_AOIs_simplified\SPLIT"
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)
target_dir = dname

out_dir = os.path.join(target_dir, '!shp2zip')
if not os.path.exists(out_dir):
    os.mkdir(out_dir)

shp_file_list = []
for dirpath, dirnames, filenames in os.walk(target_dir):
    for filename in filenames:
        if filename.endswith(('.shp', '.SHP')):
            shp_filepath = os.path.join(dirpath, filename)
            shp_file_list.append(shp_filepath)
shp_list_length = len(shp_file_list)
for i, shp_file in enumerate(shp_file_list):
    print(u'{}/{}. Архивируем {}'.format(i + 1, shp_list_length, os.path.basename(shp_file)))
    ZipShp(shp_file, dst_dir=out_dir, Delete=False)
print('\nГотово!')
