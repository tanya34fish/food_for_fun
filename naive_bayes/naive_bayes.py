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

def gen_feature(category, word_threshold, ce_threshold):
    dir = 'data/training_data/training_merge/'
    ngram_im = get_category_im(category, 'word_importance/', word_threshold)
    ngram_ce = get_category_im(category, 'cross_entropy/', ce_threshold)
    
    ngram_im_list = list(ngram_im.keys())
    ngram_ce_list = list(ngram_ce.keys())

    
    train_set = []
    test_set = []
    test_real_ans = []

    for file_idx in range(200):
        for file in glob.glob(dir + '*_' + str(file_idx+1) + '.txt'):
            print 'process %s ...' %file
            with open(file, 'r') as f:
                for line in f:
                    token = line.strip().split()
                    ans_label = token[0]
                    # belongs to the specified category
                    if str(category) in ans_label:
                        ans = 1
                    else:
                        ans = 0

                    feature = {}
                    for k in ngram_im_list:
                        feature[k] = 0.0
                    for k in ngram_ce_list:
                        feature[k] = 0.0
                    # term count
                    for word in token[1:]:
                        try:
                            n = ngram_im_list.index(word)
                        except ValueError:
                            n = -1
                        if n >= 0:
                            feature[word] += 1
                        try:
                            n = ngram_ce_list.index(word)
                        except ValueError:
                            n = -1
                        if n >= 0:
                            feature[word] += 1
                    # training data
                    if (file_idx + 1) % 10 != 0:
                        train_set.append((feature,ans))
                    # testing data
                    else:
                        test_set.append((feature,ans))
                        test_real_ans.append(ans)

    return train_set, test_set, test_real_ans


def train_and_predict(train_set, test_set, test_real_ans, category, method):

    if method == 'naive_bayes':
        classifier = NaiveBayesClassifier.train(train_set)
    elif method == 'maxent':
        classifier = MaxentClassifier.train(train_set)

    test_predict = []
    test_ans = []
    for (j,ans) in test_set:
        predict = classifier.classify(j)
        test_predict.append(predict)
        test_ans.append(ans)


    precision = get_precision(test_predict, test_ans)
    recall = get_recall(test_predict, test_ans)
    f1 = get_f1(precision, recall)
    
    print 'Method %s' %method
    print 'category: %d' %category
    print 'precision: %.5f' %precision
    print 'recall: %.5f' %recall
    print 'f1: %.5f' %f1
    print '----------------'
 
if __name__ == '__main__':
    methodList = ['naive_bayes', 'maxent']
    word_im_threshold = [17, 10, 22, 21, 36, 11, 6]
    ce_threshold = [17, 10, 24, 29, 22, 13, 7]

    for category in range(1,8):
        train_set, test_set, test_real_ans = gen_feature(category, word_im_threshold[category-1], ce_threshold[category-1])
        for method in methodList:
            train_and_predict(train_set, test_set, test_real_ans, category, method)
