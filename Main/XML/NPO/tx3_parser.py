import os


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

# print(get_values(r"C:\Users\lobanov\PycharmProjects\THE_BIG_ONE\Misc\XML\NPO\тестовый участок\Т_000110001.tx3"))
