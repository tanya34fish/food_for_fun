# coding=UTF-8
import sys
import glob
import os
import termcount


def get_category_score(category, method):
    word = []
    weight = []
    with open(os.path.join(method, str(category) + '.txt'), 'r') as f:
        for line in f:
            token = line.strip().split('\t')
            word.append(token[0])
            weight.append(token[1])
    return word, weight


def predict(category, method, answer):
    # threhsolds for every label set in different 2 methods
    param = {'word_importance' : [0, 17, 10, 22, 21, 36, 11, 6],
             'cross_entropy' : [0, 17, 10, 24, 29, 22, 13, 7]}
    
    im_word,im_weight = get_category_score(category, method)

    threshold = param[method][category]

    training_data_dir = 'data/training_data/training_merge/'
    real_ans = 0
    retrieve = 0
    right_predict = 0

    for file_idx in xrange(200):
        for file in glob.glob(training_data_dir + '*_' + str(file_idx + 1) +'.txt'):
            path, input = os.path.split(file)
            idx = int(input.split('_')[1].split('.')[0])
            # filter trainin data
            if idx % 10 != 0:
                continue

            with open(file, 'r') as f:
                print 'process %s' %file
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
                            is_retrieve = True
                            break

    precision = float(right_predict)/float(retrieve)
    recall = float(right_predict)/float(real_ans)
    f1 = 2 * float(recall * precision)/(recall + precision)


    answer[method]['category'].append(category)
    answer[method]['threshold'].append(threshold)
    answer[method]['precision'].append(precision)
    answer[method]['recall'].append(recall)
    answer[method]['F1'].append(f1)

    return answer

def outputAns(answer, method, nameList, statfile):
    for i in xrange(5):
        pstr = '{0: <8}'.format(nameList[i])
        for j in xrange(7):
            # category and threshold are int type
            if i < 2:
                pstr += '\t%8d' % answer[method][nameList[i]][j]
            # other 3 metrics are float type
            else:
                pstr += '\t%8f' % answer[method][nameList[i]][j]
        statfile.write(pstr + '\n')

    
if __name__ == '__main__':
    print 'Usage: python test.py'

    methodList = ['word_importance', 'cross_entropy']
    nameList = ['category', 'threshold', 'precision', 'recall', 'F1']
    answer = {}
    for method in methodList:
        answer[method] = {}
        for name in nameList:
            answer[method][name] = []

    for category in xrange(1, 8):
        for method in methodList:
            if not os.path.exists(method):
                os.mkdir(method)    
            answer = predict(category, method, answer)

    with open('test_result.txt', 'w') as statfile:
        for method in methodList:
            statfile.write('Method %s: \n' %method)
            outputAns(answer, method, nameList, statfile)
            statfile.write('\n')
