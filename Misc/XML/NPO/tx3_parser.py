import os


def get_values(filepath):
    with open(filepath, "r") as in_f:
        curr_line_num = None
        for line_num, line_text in enumerate(in_f):
            if 'Center=' in line_text:
                center_coords = line_text.replace('Center=', '').rstrip().split()
                center_coords_dict = dict(
                    zip(['x', 'y', 'z'],
                        [center_coords[0], center_coords[1], center_coords[2]]))
                curr_line_num = line_num
                break
        # try:
        #     center_coords_dict
        # except NameError:
        #     print('В файле не найдены координаты центра: Center=...?')
        # TODO подсчитать количество упоминаний Name и
        print(in_f.read().count('Name='))
        # for line_num, line_text in enumerate(in_f):
        #     if line_num == curr_line_num:
        #         if 'Name=' in line_text:
        #             model_name = line_text.replace('Name=', '').rstrip()




        #     # else:
        #     #     raise Exception('В файле не найдено имя объека: Name=...?')
        #
        #     if 'Pos=' in line:
        #         pos_coords = line.replace('Pos=', '').rstrip()
        #         pos_coords_dict = dict(
        #             zip(['x', 'y', 'z'],
        #                 [pos_coords[0], pos_coords[1], pos_coords[2]]))
        #     # else:
        #     #     raise Exception('В файле не найдены координаты объека: Pos=...?')
        #
        #     if 'Rot=' in line:
        #         rot_coords = line.replace('Rot=', '').rstrip()
        #         rot_coords_dict = dict(
        #             zip(['x', 'y', 'z'],
        #                 [rot_coords[0], rot_coords[1], rot_coords[2]]))
        #     # else:
        #     #     raise Exception('В файле не найдены координаты объека: Rot=...?')
        #
        #     # model_name = os.path.splitext(os.path.basename(filepath))[0]
        #
        # d = {'file': model_name, 'CS': center_coords_dict, 'pos': pos_coords_dict, 'rot': rot_coords_dict}
        # # break
    return center_coords_dict
print(get_values(r"C:\Users\lobanov\PycharmProjects\THE_BIG_ONE\Misc\XML\NPO\000110001.tx3"))
