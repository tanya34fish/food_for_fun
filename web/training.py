# coding=UTF-8
import sys
import glob
import os
from ai import segment

# For training output files

def get_category_im(c,method):
    word = []
    weight = []
    with open(os.path.join('../' + method, str(c)+'.txt'),'r') as f:
        for line in f:
            token = line.strip().split('\t')
            word.append(token[0])
            weight.append(token[1])
    return word,weight

def getFile(fileName):
    fileData = []
    with open(fileName, 'r') as f:
        line_num = 0
        for line in f:
            fileData.append(line.strip())
    return fileData

def parseFile(fileData):
    fileParse = []
    for line in fileData:
        tokList = ['']
        for name, tp in segment(line):
            tokList.append(name.encode("UTF-8"))
        fileParse.append(tokList)
    return fileParse

def printFile(fileName, fileData):
    outFile = open(fileName, 'w')
    for sentence in fileData:
        if sentence[0] == '':
            outFile.write(str(8) + ' ')
        else:
            outFile.write(sentence[0] + ' ')
        for word in sentence[1:]:
            outFile.write(word)
        outFile.write('\n')
    outFile.close
    

def test(category, method, fileData):
    param = {'word_importance' : [0, 17, 10, 22, 21, 36, 11, 6],
             'cross_entropy' : [0, 17, 10, 24, 29, 22, 13, 7]}
    im_word, im_weight = get_category_im(category, method)
    threshold = param[method][category]
    predict = []

    line_num = 0
    for line in fileData:
        for word in line[1:]:
            if word in im_word and im_word.index(word) < threshold:
                predict.append(line_num)
                break
        line_num += 1

    return predict


def trainRealTime():
#if __name__ == '__main__':
    print 'run ngram...'
    fileData = getFile('temp.txt')
    fileParse = parseFile(fileData)
    for c in xrange(1, 8):
        for m in ['cross_entropy']:
            pred = test(c, m, fileParse)
            for i in pred:
                if fileParse[i][0] == '':
                    fileParse[i][0] = str(c)
                else:
                    fileParse[i][0] += ',' + str(c)
    printFile('result.txt', fileParse)

