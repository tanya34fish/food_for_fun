# coding=UTF-8
from ai import segment
import sys
import glob

if __name__ == '__main__':
    vocab_list = []
    for i in range(10):
        vocab_list.append({})
    for file in glob.glob(sys.argv[1] + '/*.txt'):
        with open(file, 'r') as f:
            print file
            for line in f:
                line_arr = line.split(" ")
                if line_arr[0] >= '1' and line_arr[0] <= '7' and (line[1] == ',' or line[1] == ' '):
                    id_list = line_arr[0].split(',')
                    for i in range(1, len(line_arr)):
                        ans = segment(line_arr[i])
                        for name, tp in ans:
                            for j in id_list:
                                if name in vocab_list[int(j)]:
                                    vocab_list[int(j)][name] += 1
                                else:
                                    vocab_list[int(j)][name] = 1

    for i in range(1, 8):
        print "Dict in " + str(i)
        for key, val in vocab_list[i].items():
            print key.encode("UTF-8"), val
        print "\n"
