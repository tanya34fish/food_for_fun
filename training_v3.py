# coding=UTF-8
import sys
import glob
import os
from ngram import *

def get_category_im(c):
    ngDict = {}
    ng_num = 1
    with open('ngram/train/' +  str(c)+'.txt','r') as f:
        for line in f:
            token = line.strip().split()
            if len(token) > 0:
                ngDict[token[0]] = ng_num
                ng_num += 1
    return ngDict


def test(category, ans):
    param = [0, 7, 4, 12, 13, 9, 7, 9]
    nGram = get_category_im(category)
    threshold = param[category]
    dir = 'training/training_merge/'
    real_ans = 0
    retrieve = 0
    right_predict = 0
    for file_idx in xrange(200):
        for file in glob.glob(dir + '*_' + str(file_idx + 1) +'.txt'):
            path, input = os.path.split(file)
            idx = int(input.split('_')[1].split('.')[0])
            if idx % 10 == 0:
                continue
            with open(file, 'r') as f:
                lineNum = 0
                for line in f:
                    #print(line)
                    token = line.split()
                    lineNum += 1
                    is_ans = False
                    is_retrieve = False

                    if str(category) in token[0]:
                        real_ans += 1
                        is_ans = True
                    for word in token[1:]:
                        if word in nGram and nGram[word] < threshold:
                            retrieve += 1
                            if is_ans:
                                right_predict += 1
                            break

         
    precision = float(right_predict)/float(retrieve)
    recall = float(right_predict)/float(real_ans)
    f1 = 2*float(recall*precision)/(recall+precision)
    #print 'Test: category %d, threshold: %d' % (category, threshold)
    ans[0].append(category)
    ans[1].append(threshold)
    #g.write('Test: category %d\n' %category)
    #print 'precision: %.5f' %precision
    ans[2].append(precision)
    #g.write('precision: %.5f\n' %precision)
    #print 'recall: %.5f' %recall
    ans[3].append(recall)
    #g.write('recall: %.5f\n' %recall)
    #print 'F1: %.5f' %f1
    ans[4].append(f1)
    #g.write('F1: %.5f\n' %f1)
    #print '================'

def printAns(ans):
    name = ['category', 'threshold', 'precision', 'recall', 'F1']
    print 'ngram'
    for i in xrange(5):
        pstr = '{0: <8}'.format(name[i])
        for j in xrange(7):
            if i < 2:
                pstr += '\t%8d' % ans[i][j]
            else:
                pstr += '\t%8f' % ans[i][j]
        print pstr

    
if __name__ == '__main__':
    ans = [[], [], [], [], []]
    for c in xrange(1, 8):
        test(c,ans)
    printAns(ans)
