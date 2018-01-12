import os
import csv
import shutil


def calculate_filesize(file_path, units='mb'):
    """Calculate file size in different units

    :param file_path: path to a target file
    :param units: units in which to calculate filesize
    :return: filesize in specified units
    """
    filesize_bytes = os.path.getsize(file_path)
    if units == 'b':
        return filesize_bytes
    if units == 'mb':
        return filesize_bytes / (1024 * 1024.0)
    elif units == 'gb':
        return filesize_bytes / (1024 * 1024 * 1024.0)
    else:
        raise ValueError('Unknown units')


def get_file_paths(csv_file, target_column):
    """Get file paths from CSV file as values in specific column

    :param csv_file: path to target csv file
    :param target_column: name of the column that contains file paths
    :return: list of file paths
    """
    with open(csv_file) as csv_file:
        csv_reader_content = csv.DictReader(csv_file)
        target_field_list = [value[target_column] for value in csv_reader_content]
    return target_field_list


total_size = 0
counter = 0
for f_path in get_file_paths(r"C:\Users\lobanov\Desktop\Inbox\downloads\снимки_.csv", target_column='path'):
    counter += 1
    print(counter, f_path, calculate_filesize(file_path=f_path, units='gb'))
    shutil.copyfile(f_path, os.path.join(r"D:\ДДЗ", os.path.basename(f_path)))
    total_size += calculate_filesize(file_path=f_path, units='gb')
print(total_size)
