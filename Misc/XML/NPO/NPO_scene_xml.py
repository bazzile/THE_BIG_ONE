import os
from lxml import etree

# # src_dir = r'C:\Users\lobanov\PycharmProjects\THE_BIG_ONE\Misc\XML\NPO\тестовый участок'
# src_dir = input("Введите путь к целевой директории:\n (Пример: C:/NPO/тестовый участок")
#
# assert os.path.exists(src_dir), "Директория не найдена: , "+str(src_dir)
src_dir = os.path.dirname(__file__)


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
    coord_sys_node = add_node(root_node, "coordSys")
    add_node(coord_sys_node, "sceneCoordSys", {'Datum': 'WGS84'})
    add_node(coord_sys_node, "sceneCoordSys", {'Zone': '37N'})
    cs_dict = model_list[0]['cs']
    add_node(coord_sys_node, "sceneCenter", cs_dict)
    for model in model_list:
        in_file_name, pos_dict, rot_dict = model['file'], model['pos'], model['rot']
        model_node = add_node(root_node, "model")
        add_node(model_node, "path", 'Data/Object')
        add_node(model_node, "file", in_file_name)
        add_node(model_node, "position", pos_dict)
        add_node(model_node, "rotation", rot_dict)
        add_node(model_node, "scale", {'coef': '1'})

    # string = etree.tostring(root_node)
    xml_tree = etree.ElementTree(root_node)
    xml_tree.write(
        os.path.join(dst_dir, "scene.xml"),
        pretty_print=True, xml_declaration=True, encoding='UTF-8')


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

model_list = []
for file in os.listdir(src_dir):
    if file.endswith(('.tx3', '.TX3')):
        filepath = os.path.join(src_dir, file)
        model = get_values(filepath)
        model_list.append(model)
create_xml(model_list, src_dir)

