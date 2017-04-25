import os
from lxml import etree
import csv

# # src_dir = r'C:\Users\lobanov\PycharmProjects\THE_BIG_ONE\Misc\XML\NPO\тестовый участок'
# src_dir = input("Введите путь к целевой директории:\n (Пример: C:/NPO/тестовый участок")
#
# assert os.path.exists(src_dir), "Директория не найдена: , "+str(src_dir)
# src_dir = os.path.dirname(__file__)

in_csv = r"E:\!WORK\Dima_new\4_catalogs\OKA_model_catalogs.csv"

with open(in_csv) as in_csv:
    model_info_list = []
    reader = csv.DictReader(in_csv)
    for row in reader:
        model_info_list.append(row)


def add_node(root_name, name, attributes=None):
    if attributes is None:
        node = etree.SubElement(root_name, name)
    else:
        if type(attributes) == str:
            node = etree.SubElement(root_name, name)
            node.text = attributes
        elif type(attributes) == dict:
            node = etree.SubElement(root_name, name)
            for attribute, value in sorted(attributes.items()):
                node.set(attribute, value)
        else:
            raise Exception('attributes must be str or dict')
    return node


def create_xml(model_list, dst_dir):
    root_node = etree.Element('scene')
    add_node(root_node, "scenename", 'OKA')
    add_node(root_node, "sceneid", '1')
    add_node(root_node, "coordsystem", 'WGS84UTM37N')
    centerscene_node = add_node(root_node, "centerscene", dict(zip(['x', 'y', 'z'], ['0', '0', '0'])))
    # add_node(coord_sys_node, "sceneCoordSys", {'Datum': 'WGS84'})
    # add_node(coord_sys_node, "sceneCoordSys", {'Zone': '37N'})
    # cs_dict = model_list[0]['cs']
    # add_node(coord_sys_node, "sceneCenter", cs_dict)

    for model in model_list:
        # in_file_name, cs_dict, pos_dict, rot_dict = model['file'], model['cs'], model['pos'], model['rot']
        model_node = add_node(root_node, "model")
        add_node(model_node, "path", '170425')
        add_node(model_node, "file", model)
        add_node(model_node, "position", dict(zip(['x', 'y', 'z'], ['0', '0', '0'])))
        add_node(model_node, "rotation", dict(zip(['x', 'y', 'z'], ['0', '0', '0'])))
        add_node(model_node, "scale", {'coef': '1'})
        add_node(model_node, "id", model.split('.')[0])

        for model_entry in model_info_list:
            if model_entry.get('ID') == model.split('.')[0]:
                print(model, model_entry.get('Comments'))
                add_node(model_node, "class", model_entry.get('Class'))
                add_node(model_node, "type", model_entry.get('Type').zfill(2))
                add_node(model_node, "origin", model_entry.get('Origin'))
                add_node(model_node, "comments", model_entry.get('Comments'))
                break
        # add_node(model_node, "class", model.split('.')[0])
        # add_node(model_node, "type", model.split('.')[0])
        # add_node(model_node, "origin", model.split('.')[0])
        # add_node(model_node, "comments", model.split('.')[0])
        texture_list = get_texture_list(model)
        for (i, texture) in enumerate(texture_list):
            add_node(model_node, 'texture' + str(i + 1), texture)

    # string = etree.tostring(root_node)
    xml_tree = etree.ElementTree(root_node)
    xml_tree.write(
        os.path.join(dst_dir, "!170425.xml"),
        pretty_print=True, xml_declaration=True, encoding='UTF-8')


def get_texture_list(model_file):
    model_name = model_file.split('.')[0]
    texture_list = []
    for fname in os.listdir(src_dir):
        if fname.startswith(model_name) and not fname.endswith(('.3ds', '.3DS')):
            texture_list.append(fname)
    return texture_list


def get_values(filepath):
    with open(filepath, "r") as in_f:
        filename = os.path.splitext(os.path.basename(filepath))[0] + '.3ds'

        curr_line_num = None
        for line_num, line_text in enumerate(in_f):
            if 'Center=' in line_text:
                center_coords = line_text.replace('Center=', '').rstrip().split()
                center_coords_dict = dict(
                    zip(['x', 'y', 'z'],
                        [center_coords[0], center_coords[1], center_coords[2]]))
                curr_line_num = line_num
                break
        for line_num, line_text in enumerate(in_f, start=curr_line_num):
            if 'Pos=' in line_text:
                pos_coords = line_text.replace('Pos=', '').rstrip().split()
                pos_coords_dict = dict(
                    zip(['x', 'y', 'z'],
                        [pos_coords[0], pos_coords[1], pos_coords[2]]))
                curr_line_num = line_num
        for line_num, line_text in enumerate(in_f):
            if 'Rot=' in line_text:
                rot_coords = line_text.replace('Rot=', '').rstrip().split()
                rot_coords_dict = dict(
                    zip(['x', 'y', 'z'],
                        [rot_coords[0], rot_coords[1], rot_coords[2]]))
                curr_line_num = line_num

        try:
            center_coords_dict
        except NameError:
            raise Exception('Кординаты центральной точки (Center) не найдены в {}'.format(filepath))
        try:
            pos_coords_dict
        except NameError:
            raise Exception('Значения положения (Pos) не найдены в {}'.format(filepath))
        try:
            rot_coords_dict
        except NameError:
            rot_coords_dict = dict(zip(['x', 'y', 'z'], ['0', '0', '0']))

        d = {'file': filename, 'cs': center_coords_dict, 'pos': pos_coords_dict, 'rot': rot_coords_dict}
    return d


src_dir = r'E:\!WORK\Dima_new\4_catalogs\170425'

model_list = []
for file in os.listdir(src_dir):
    if file.endswith(('.3ds', '.3DS')):
        filepath = os.path.join(src_dir, file)
        # model = get_values(filepath)
        # model_list.append(model)
        model_list.append(file)
create_xml(model_list, src_dir)

