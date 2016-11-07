#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import io
from xml.etree import ElementTree as ET
import xml.dom.minidom

# задание корневой директории
src_dir = os.path.dirname(os.path.realpath(__file__))
dst_dir = os.path.join(src_dir, 'test_data')
src_filepath = os.path.join(src_dir, 'test_data', 'fr_0041_0102_07233_1_07229_03_G_10.xml')


def make_good_xml(bad_xml_file, dst_path, src_encoding='Windows-1251'):
    """Преобразование xml в удобочитаемый формат"""
    xml_tree = xml.dom.minidom.parse(bad_xml_file)
    pretty_xml_as_string = xml_tree.toprettyxml(encoding=src_encoding)
    with open(os.path.join(dst_path, '_'.join(('GOOD', os.path.basename(bad_xml_file)))), 'w') as f:
        f.write(pretty_xml_as_string)


def search_xml(xml_filepath, parameter_list, src_encoding='Windows-1251'):
    """Поиск в xml-файле по списку тэгов """
    parser = ET.XMLParser(encoding=src_encoding)
    root = ET.parse(xml_filepath, parser=parser)
    result_list = []
    for parameter in parameter_list:
        item = root.find('.//' + parameter)
        result_list.append(item.text)
    return result_list

with io.open(os.path.join(dst_dir, 'result.txt'), 'a', encoding='Windows-1251') as f:
    for path, dirnames, filenames in os.walk(dst_dir):
        for filename in filenames:
            xml_file_path = os.path.join(path, filename)
            if filename.lower().endswith('.xml'):
                parameters = search_xml(xml_file_path, ['dSceneDate', 'nLineOff', 'nHeightScale'])
                full_string = [filename] + parameters + ['\n']
                f.write('|'.join(full_string).encode('Windows-1251').decode('Windows-1251'))

make_good_xml(src_filepath, dst_dir)
