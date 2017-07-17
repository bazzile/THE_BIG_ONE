import os


def parse_csv(filepath):
    file_part = 0
    with open(filepath, 'r') as infile:
        line_block_list = []
        for n, line in enumerate(infile):
            print('Working on line {}'.format(n))
            line = line[:10] + ';' + line[10:21] + ';' + line[21:28] + ';\n'
            line_block_list.append(line)
            if n % 11000001 == 0:
                file_part += 1
            if n % 1000000 != 0:
                pass
            else:
                print('End of the block, writing lines to file...')
                with open(os.path.join(os.path.dirname(filepath),
                                       os.path.splitext(os.path.basename(filepath))[0] + '_part_' + str(
                                    file_part) +
                                os.path.splitext(os.path.basename(filepath))[-1]), 'a') as outfile:
                    outfile.writelines(line_block_list)
                line_block_list = []
        if len(line_block_list) != 0:
            print('Writing last lines to file...')
            with open(os.path.join(os.path.dirname(filepath),
                                   os.path.splitext(os.path.basename(filepath))[0] + '_part_' + str(
                                       file_part) +
                                           os.path.splitext(os.path.basename(filepath))[-1]), 'a') as outfile:
                outfile.writelines(line_block_list)



                # if n == 149:
                #     break


parse_csv(r"U:\PRJ\2016\NPOMASH16\8_цмр\матрицы\1.csv")
