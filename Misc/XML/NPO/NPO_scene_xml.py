import os
from lxml import etree


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
# create XML
root_node = etree.Element('scene')
coord_sys_node = add_node(root_node, "coordSys")
add_node(coord_sys_node, "sceneCoordSys", {'Datum': 'WGS84'})
add_node(coord_sys_node, "sceneCoordSys", {'Zone': '37N'})
add_node(coord_sys_node, "sceneCenter", {'x': '404741.841902', 'y': '6081869.255131', 'z': '72.636400'})

model_node = add_node(root_node, "model")
add_node(model_node, "path", 'Data/Object')
add_node(model_node, "file", 'klen.3ds')
add_node(model_node, "position", {'x': '28', 'y': '9', 'z': '-40'})
add_node(model_node, "rotation", {'x': '10', 'y': '0', 'z': '0'})
add_node(model_node, "scale", {'coef': '5'})

string = etree.tostring(root_node)
xml_tree = etree.ElementTree(root_node)
xml_tree.write(
    os.path.join(r"C:\Users\lobanov\PycharmProjects\THE_BIG_ONE\Misc\XML\NPO", "scene.xml"),
    pretty_print=True, xml_declaration=True, encoding='UTF-8')
