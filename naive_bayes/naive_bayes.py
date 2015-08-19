# coding=UTF-8
import sys
import glob
import os
from nltk import NaiveBayesClassifier 
from nltk import classify
from nltk import MaxentClassifier

def get_category_im(c, method_dir, threshold):
    ngram = {}
    word_idx = 0
    with open(method_dir + str(c) + '.txt','r') as f:
        for line in f:
            if not line.strip():
                continue
            token = line.split('\t')
            word = token[0]
            ngram[word] = float(token[1])
            if word_idx > threshold:
                break
            word_idx += 1
    return ngram

def get_precision(test_predict, test_ans):
    retrieve_num = 0
    right = 0
    for (p,a) in zip(test_predict, test_ans):
        if p == 1:
            retrieve_num += 1
            if p == a:
                right += 1
    return float(right)/float(retrieve_num)

def get_recall(test_predict, test_ans):
    real_ans = 0
    right = 0
    for (p,a) in zip(test_predict, test_ans):
        if a == 1:
            real_ans += 1
            if p == a:
                right += 1
    return float(right)/float(real_ans)

def get_f1(precision, recall):
    return 2 * float(recall*precision) / float(recall+precision)

def gen_feature(category, out_dir, word_threshold, ce_threshold):
    dir = 'training/training_merge/'
    ngram_im = get_category_im(category, 'word_importance/', word_threshold)
    ngram_ce = get_category_im(category, 'cross_entropy/', ce_threshold)
    ngram_im_list = list(ngram_im.keys())
    ngram_ce_list = list(ngram_ce.keys())

    
    train_set = []
    test_set = []
        
    test_real_ans = []

    for file_idx in range(200):
        for file in glob.glob(dir + '*_' + str(file_idx+1) + '.txt'):
            #print 'process %s ...' %file
            with open(file, 'r') as f:
                for line in f:
                    token = line.strip().split()
                    ans_label = token[0]
                    # belongs to the specified category
                    if str(category) in ans_label:
                        ans = 1
                    else:
                        ans = 0
                    #feature = {'f1': 0.0, 'f2': 0.0}
                    feature = {}
                    for k in ngram_im_list:
                        feature[k] = 0.0
                    for k in ngram_ce_list:
                        feature[k] = 0.0
                    for word in token[1:]:
                        try:
                            n = ngram_im_list.index(word)
                        except ValueError:
                            n = -1
                        if n >= 0:
                            #feature['f1'] += ngram_im[word]
                            feature[word] += 1
                        try:
                            n = ngram_ce_list.index(word)
                        except ValueError:
                            n = -1
                        if n >= 0:
                            #feature['f2'] += ngram_ce[word]
                            feature[word] += 1
                    if (file_idx + 1) % 10 != 0:
                        train_set.append((feature,ans))
                    else:
                        test_set.append((feature,ans))
                        test_real_ans.append(ans)

    #print 'training data: %d' %len(train_set)
    #print 'test data: %d' %len(test_set)
    #with open(out_dir+'%d_svm_train.txt' %category, 'w') as f:
    #    for (feature,ans) in train_set:
    #        f.write('%d ' %ans)
    #        for key,value in feature.iteritems():
    #            f.write('%.5f ' %(value))
    #        f.write('\n')
    #with open(out_dir+'%d_svm_test.txt' %category, 'w') as f:
    #    for (feature,ans) in test_set:
    #        f.write('%d ' %ans)
    #        for key,value in feature.iteritems():
    #            f.write('%.5f ' %(value))
    #        f.write('\n')

    # naive bayes
    #a = open('ensemble/maxent_%d.txt' %category, 'w')
    b = open('ensemble/maxent_%d.txt' %category, 'w')
    nb_classifier = NaiveBayesClassifier.train(train_set)
    me_classifier = MaxentClassifier.train(train_set)
    test_predict = []
    test_ans = []
    for (j,ans) in test_set:
        nb_p = nb_classifier.classify(j)
        test_predict.append(nb_p)
        me_p = me_classifier.classify(j)
        #a.write('%d\n' %nb_p)
        b.write('%d\n' %me_p)
        test_ans.append(ans)
    #a.close()
    b.close()
    pre = get_precision(test_predict, test_ans)
    recall = get_recall(test_predict, test_ans)
    f1 = get_f1(pre, recall)
    
    #g = open('maxent/%d.txt' %category, 'w')
    print 'category: %d' %category
    #g.write('category: %d\n' %category)
    print 'precision: %.5f' %pre
    #g.write('precision: %.5f\n' %pre)
    print 'recall: %.5f' %recall
    #g.write('recall: %.5f\n' %recall)
    print 'f1: %.5f' %f1
    #g.write('f1: %.5f\n' %f1)
    #return

def vote(c,test_real_ans):
    final_ans = []
    ans = [[] for x in range(4)]
    with open('ensemble/word_importance_%d.txt' %c, 'r') as f:
        for line in f:
            ans[0].append(int(line.strip()))
    with open('ensemble/cross_entropy_%d.txt' %c, 'r') as f:
        for line in f:
            ans[1].append(int(line.strip()))
    with open('ensemble/maxent_%d.txt' %c, 'r') as f:
        for line in f:
            ans[2].append(int(line.strip()))
    with open('ensemble/nb_%d.txt' %c, 'r') as f:
        for line in f:
            ans[3].append(int(line.strip()))
    for (im,ce,maxent,nb) in zip(ans[0],ans[1],ans[2],ans[3]):
        j = [im,ce,maxent,nb]
        if j.count(1) >= j.count(0):
            final_ans.append(1)
        else:
            final_ans.append(0)
    
    pre = get_precision(final_ans, test_real_ans)
    recall = get_recall(final_ans, test_real_ans)
    f1 = get_f1(pre, recall)
    
    #g = open('maxent/%d.txt' %category, 'w')
    print 'category: %d' %c
    #g.write('category: %d\n' %category)
    print 'precision: %.5f' %pre
    #g.write('precision: %.5f\n' %pre)
    print 'recall: %.5f' %recall
    #g.write('recall: %.5f\n' %recall)
    print 'f1: %.5f' %f1
    #g.write('f1: %.5f\n' %f1)
    return 
 
if __name__ == '__main__':
    out_dir = 'svm/'
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    word_im_threshold = [17, 10, 22, 21, 36, 11, 6]
    ce_threshold = [17, 10, 24, 29, 22, 13, 7]
    for x in range(1,8):
        real_ans = gen_feature(x, out_dir, word_im_threshold[x-1], ce_threshold[x-1])
        #vote(x,real_ans)
