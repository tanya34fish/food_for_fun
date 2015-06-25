# coding=UTF-8
import sys
import glob
import os
from ngram import *

def get_category_im(c,method):
    word = []
    weight = []
    with open(os.path.join(method, str(c)+'.txt'),'r') as f:
        for line in f:
            token = line.strip().split('\t')
            word.append(token[0])
            weight.append(token[1])
    return word,weight


def test(category,method,ans):
    param = {'word_importance' : [0, 17, 10, 22, 21, 36, 11, 6],
             'cross_entropy' : [0, 17, 10, 24, 29, 22, 13, 7]}
    im_word,im_weight = get_category_im(category, method)
    threshold = param[method][category]
    dir = 'training/training_merge/'
    err_dir = 'err_analysis/%s' %method
    real_ans = 0
    retrieve = 0
    right_predict = 0

    if not os.path.exists(err_dir):
        os.mkdir(err_dir)

    #g = open(os.path.join(err_dir,'error_%d.txt' %category), 'w')
    for file_idx in xrange(200):
        for file in glob.glob(dir + '*_' + str(file_idx + 1) +'.txt'):
            path, input = os.path.split(file)
            idx = int(input.split('_')[1].split('.')[0])
            if idx %10 == 0:
                continue
            with open(file, 'r') as f:
                print file
                lineNum = 0
                for line in f:
                    lineNum += 1
                    token = line.strip().split()
                    is_ans = False
                    is_retrieve = False
                    if str(category) in token[0]:
                        real_ans += 1
                        is_ans = True
                    for word in token[1:]:
                        if word in im_word and im_word.index(word) < threshold:
                            retrieve += 1
                            if is_ans:
                                right_predict += 1
                                #print 'right'
                            #else:
                                #g.write('%s: Line %d\n' %(input,lineNum))
                                #g.write(line)
                                #g.write('program error prediction: %d\n' %category)
                                #g.write('\n')
                                #print 'error'
                            is_retrieve = True
                            break
                    #if not is_retrieve and is_ans:
                        #g.write('%s: Line %d\n' %(input,lineNum))
                        #g.write(line)
                        #g.write('program did not classify it as category %d\n' %category)
                        #g.write('\n')
         
    precision = float(right_predict)/float(retrieve)
    recall = float(right_predict)/float(real_ans)
    f1 = 2*float(recall*precision)/(recall+precision)
    #print 'Test: category %d, threshold: %d' % (category, threshold)
    ans[method][0].append(category)
    ans[method][1].append(threshold)
    #g.write('Test: category %d\n' %category)
    #print 'precision: %.5f' %precision
    ans[method][2].append(precision)
    #g.write('precision: %.5f\n' %precision)
    #print 'recall: %.5f' %recall
    ans[method][3].append(recall)
    #g.write('recall: %.5f\n' %recall)
    #print 'F1: %.5f' %f1
    ans[method][4].append(f1)
    #g.write('F1: %.5f\n' %f1)
    #print '================'

def printAns(ans, method, statfile):
    name = ['category', 'threshold', 'precision', 'recall', 'F1']
    statfile.write(method + '\n')
    for i in xrange(5):
        pstr = '{0: <8}'.format(name[i])
        for j in xrange(7):
            if i < 2:
                pstr += '\t%8d' % ans[method][i][j]
            else:
                pstr += '\t%8f' % ans[method][i][j]
        statfile.write(pstr + '\n')

    
if __name__ == '__main__':
    print 'Usage: python testing_v4.py'
    print 'This program will use ngram.py to count ngram again'
    print 'also run word_importance and cross_entropy'
    print 'run ngram...'
    inputdir = 'training/training_merge'
    outputdir = 'ngram/train'
    ans = {'word_importance' : [[], [], [], [], []],
             'cross_entropy' : [[], [], [], [], []]}
    ngram_count(inputdir,outputdir,train=True)
    total_ngram,category_ngram_list,category_total_count_list = get_count_statistics()
    word_importance(total_ngram,category_ngram_list,category_total_count_list)
    cross_entropy(total_ngram,category_ngram_list,category_total_count_list)
    for c in xrange(1, 8):
        for m in ['word_importance', 'cross_entropy']:
            if not os.path.exists(m):
                os.mkdir(m)    
            test(c,m,ans)

    statfile = open('training_result.txt', 'w')
    for m in ['word_importance', 'cross_entropy']:
        printAns(ans, m, statfile)
