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


def test(category,method):
    #### thresholdTable_m1 = [17, 10, 22, 21, 36, 11, 6]
    #### thresholdTable_m2 = [17, 10, 24, 29, 22, 13, 7]
    f1_bound = 0.
    th_best = 0
    for i in range(1, 15):
        im_word,im_weight = get_category_im(category, method)
        threshold = i
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
                if idx %10 != 0:
                    continue
                with open(file, 'r') as f:
                    #print file
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
        print 'Test: category %d, threshold: %d' % (category, threshold)
        #g.write('Test: category %d\n' %category)
        print 'precision: %.5f' %precision
        #g.write('precision: %.5f\n' %precision)
        print 'recall: %.5f' %recall
        #g.write('recall: %.5f\n' %recall)
        print 'F1: %.5f' %f1
        #g.write('F1: %.5f\n' %f1)
        print '================'
        if f1 > f1_bound:
            f1_bound = f1
            th_best = threshold

    print '\nTest %d' % category
    print 'best threshold: %d' % th_best
    print 'best F1: %f\n' % f1_bound
    
if __name__ == '__main__':
    print 'Usage: python testing_v2.py'
    print 'This program will use ngram.py to count ngram again'
    print 'also run word_importance and cross_entropy'
    print 'run ngram...'
    inputdir = 'training/training_merge'
    outputdir = 'ngram/train'
    ngram_count(inputdir,outputdir,train=True)
    total_ngram,category_ngram_list,category_total_count_list = get_count_statistics()
    word_importance(total_ngram,category_ngram_list,category_total_count_list)
    cross_entropy(total_ngram,category_ngram_list,category_total_count_list)
    for c in [2,6,7]:
        for m in ['word_importance', 'cross_entropy']:
            print m
            if not os.path.exists(m):
                os.mkdir(m)    
            test(c,m)
