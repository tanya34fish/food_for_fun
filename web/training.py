# coding=UTF-8
import sys
import glob
import os
from ngram import *

# For training output files

def get_category_im(c,method):
    word = []
    weight = []
    with open(os.path.join(method, str(c)+'.txt'),'r') as f:
        for line in f:
            token = line.strip().split('\t')
            word.append(token[0])
            weight.append(token[1])
    return word,weight


def getFile(filedir):
    fileData = [[]]
    for file_idx in xrange(200):
        fileData.append([])
        for file in glob.glob(filedir + '*_' + str(file_idx + 1) +'.txt'):
            with open(file, 'r') as f:
                line_num = 0
                for line in f:
                    fileData[file_idx + 1].append(line.strip().split())
                    fileData[file_idx + 1][line_num][0] = ""
                    line_num += 1
    return fileData

def printFile(filedir, fileData):
    for file_idx in xrange(200):
        outFile = open(filedir + '/' + str(file_idx + 1) + '.txt', 'w')
        print 'write %d' % (file_idx + 1)
        for sentence in fileData[file_idx + 1]:
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
    im_word,im_weight = get_category_im(category, method)
    threshold = param[method][category]
    predict = [[]]

    for file_idx in xrange(200):
        print "file id %d, category %d" % (file_idx + 1, category)
        predict.append([])
        line_num = 0
        for line in fileData[file_idx + 1]:
            for word in line[1:]:
                if word in im_word and im_word.index(word) < threshold:
                    predict[file_idx + 1].append(line_num)
                    break
            line_num += 1
    return predict


if __name__ == '__main__':
    print 'run ngram...'
    inputdir = 'training/training_merge/'
    outputdir = 'ngram/train/'
    webdir = 'training/training_train/'
    ngram_count(inputdir, outputdir, train=True)
    total_ngram,category_ngram_list,category_total_count_list = get_count_statistics()
    word_importance(total_ngram,category_ngram_list,category_total_count_list)
    cross_entropy(total_ngram,category_ngram_list,category_total_count_list)
    fileData = getFile(inputdir)
    for c in xrange(1, 8):
        for m in ['cross_entropy']:
            pred = test(c, m, fileData)
            for i in xrange(1, 201):
                for j in pred[i]:
                    if fileData[i][j][0] == '':
                        fileData[i][j][0] = str(c)
                    else:
                        fileData[i][j][0] += ',' + str(c)
    printFile(webdir, fileData)
