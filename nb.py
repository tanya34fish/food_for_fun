# coding=UTF-8
import sys
import glob
import os
from nltk import NaiveBayesClassifier 
from nltk import classify

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

def gen_feature(category, out_dir):
    dir = 'training/training_merge/'
    ngram_im = get_category_im(category, 'word_importance/', 20)
    ngram_ce = get_category_im(category, 'cross_entropy/', 300)
    ngram_im_list = list(ngram_im.keys())
    ngram_ce_list = list(ngram_ce.keys())

    
    train_set = []
    test_set = []
    
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
                    feature = {'f1': 0.0, 'f2': 0.0}
                    for word in token[1:]:
                        try:
                            n = ngram_im_list.index(word)
                        except ValueError:
                            n = -1
                        if n >= 0:
                            feature['f1'] += ngram_im[word]
                        try:
                            n = ngram_ce_list.index(word)
                        except ValueError:
                            n = -1
                        if n >= 0:
                            feature['f2'] += ngram_ce[word]
                    if (file_idx + 1) % 10 != 0:
                        train_set.append((feature,ans))
                    else:
                        test_set.append((feature,ans))
    print 'training data: %d' %len(train_set)
    print 'test data: %d' %len(test_set)
    with open(out_dir+'%d_svm_train.txt' %category, 'w') as f:
        for (feature,ans) in train_set:
            f.write('%d ' %ans)
            for key,value in feature.iteritems():
                f.write('%.5f ' %(value))
            f.write('\n')
    with open(out_dir+'%d_svm_test.txt' %category, 'w') as f:
        for (feature,ans) in test_set:
            f.write('%d ' %ans)
            for key,value in feature.iteritems():
                f.write('%.5f ' %(value))
            f.write('\n')

    # naive bayes
    #nb_classifier = NaiveBayesClassifier.train(train_set)
    #acc = classify.accuracy(nb_classifier, test_set)
    #test_predict = []
    #test_ans = []
    #for (j,ans) in test_set:
    #    test_predict.append(nb_classifier.classify(j))
    #    test_ans.append(ans)
    #pre = get_precision(test_predict, test_ans)
    #recall = get_recall(test_predict, test_ans)
    #f1 = get_f1(pre, recall)
    #print 'category: %d' %category
    #print 'precision: %.5f' %pre
    #print 'recall: %.5f' %recall
    #print 'f1: %.5f' %f1
    
    return

if __name__ == '__main__':
    out_dir = 'svm/'
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    for x in range(1,8):
        gen_feature(x, out_dir)
