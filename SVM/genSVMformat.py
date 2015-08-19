import sys
import glob
import os


NGRAM_DIR = 'ngram/train/'
TRAIN_DIR = 'training/training_seg/'
OUTPUT_DIR = 'ngram/train/'
ngramSet = [set()]
svmData = [[]]
outFile = [0, 0, 0, 0, 0, 0, 0, 0]

for i in range(1, 8):
    ngramSet.append(set())
    svmData.append([])
    ngFile = open(NGRAM_DIR + str(i) + '.txt', 'r')
    outFile[i] = open(OUTPUT_DIR + "svm_" + str(i) + '.txt', 'w')
    for line in ngFile:
        token = line.split()
        if len(token) != 0:
            ngramSet[i].add(token[0])
    ngFile.close()

for file in glob.glob(TRAIN_DIR + '/*.txt'):
    with open(file, 'r') as f:
        print file
        for line in f:
            line_arr = line.split()
            flag = [0, 0, 0, 0, 0, 0, 0, 0]
            data = ["", "", "", "", "", "", "", ""]
            idx = 1
            for word in line_arr:
                for i in range(1, 8):
                    if word in ngramSet[i]:
                        data[i] = data[i] + " " + str(idx) + ":1"
                        flag[i] = 1
                    else:
                        data[i] = data[i] + " " + str(idx) + ":0"
                idx += 1
            for i in range(1, 8):
                outFile[i].write(str(flag[i]) + data[i] + '\n')

for i in range(1, 8):
    outFile[i].close()
