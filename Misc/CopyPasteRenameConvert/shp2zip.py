import os
import zipfile


def ZipShp(inShp, Delete=True):
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
    # Base name of shapefile
    inName = os.path.basename(os.path.splitext(inShp)[0])
    # Create zipfile name
    zipfl = os.path.join(inLocation, inName + ".zip")
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

target_dir = r"U:\ОТА\ЯНАО17\Data\Vector\AOI\Районы от Анны\zip\simplified\Anna_AOIs_simplified\SPLIT"
shp_file_list = []
for dirpath, dirnames, filenames in os.walk(target_dir):
    for filename in filenames:
        if filename.endswith(('.shp', '.SHP')):
            shp_filepath = os.path.join(dirpath, filename)
            shp_file_list.append(shp_filepath)
shp_list_length = len(shp_file_list)
for i, shp_file in enumerate(shp_file_list):
    print('{}/{}. Архивируем {}'.format(i + 1, shp_list_length, os.path.basename(shp_file)))
    ZipShp(shp_file, Delete=False)
print('\nГотово!')
