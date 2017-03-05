import os
from Misc.XML.NPO.NPO_scene_xml import create_xml
from Misc.XML.NPO.tx3_parser import get_values

src_dir = r'C:\Users\lobanov\PycharmProjects\THE_BIG_ONE\Misc\XML\NPO\тестовый участок'

model_list = []
for file in os.listdir(src_dir):
    if file.endswith(('.tx3', '.TX3')):
        filepath = os.path.join(src_dir, file)
        model = get_values(filepath)
        model_list.append(model)
create_xml(model_list, src_dir)

