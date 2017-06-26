import os
import lxml.etree as etree

in_filepath = r"C:\Users\lobanov\Desktop\PANO2ARC.XML"

xml = etree.parse(in_filepath)

# string = etree.tostring(root_node)
xml.write(
    os.path.join(r"C:\Users\lobanov\Desktop",
                 os.path.splitext(os.path.basename(in_filepath))[0] + '_pretty_print' +
                 os.path.splitext(os.path.basename(in_filepath))[1]),
    pretty_print=True, xml_declaration=True, encoding='UTF-8')
