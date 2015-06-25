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
    fileData = []
    return fileData


def test(category, method):
    param = {[0, 17, 10, 24, 29, 22, 13, 7]}
    im_word,im_weight = get_category_im(category, method)
    threshold = param[method][category]
    dir = 'training/training_merge/'
    real_ans = 0
    retrieve = 0
    right_predict = 0

    if not os.path.exists(err_dir):
        os.mkdir(err_dir)

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
         
    
if __name__ == '__main__':
    print 'run ngram...'
    inputdir = 'training/training_merge'
    outputdir = 'training/training_train'
    ngram_count(inputdir, outputdir, train=True)
    total_ngram,category_ngram_list,category_total_count_list = get_count_statistics()
    word_importance(total_ngram,category_ngram_list,category_total_count_list)
    cross_entropy(total_ngram,category_ngram_list,category_total_count_list)
    for c in xrange(1, 8):
        for m in ['cross_entropy']:
            if not os.path.exists(m):
                os.mkdir(m)  
            test(c, m)


