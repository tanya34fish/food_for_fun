# coding=UTF-8
import sys
import glob
import os

def get_category_im(c):
    word = []
    weight = []
    with open('word_importance/'+str(c)+'.txt','r') as f:
        for line in f:
            token = line.strip().split('\t')
            word.append(token[0])
            weight.append(token[1])
    return word,weight


def test(category):
    im_word,im_weight = get_category_im(category)
    threshold = 10
    dir = 'training/training_merge/'
    err_dir = 'err_analysis/'
    real_ans = 0
    retrieve = 0
    right_predict = 0
    g = open(err_dir + 'error_%d.txt' %category, 'w')
    for file in glob.glob(dir + '*.txt'):
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
                            print 'right'
                        else:
                            g.write('precision error:\n')
                            g.write('%s: Line %d\n' %(input,lineNum))
                            g.write(line)
                            g.write('\n')
                            print 'error'
                        is_retrieve = True
                        break
                if not is_retrieve and is_ans:
                    g.write('recall error:\n')
                    g.write('%s: Line %d\n' %(input,lineNum))
                    g.write(line)
                    g.write('\n')
         
    precision = float(right_predict)/float(retrieve)
    recall = float(right_predict)/float(real_ans)
    f1 = 2*float(recall*precision)/(recall+precision)
    print 'Test: category %d' %category
    g.write('Test: category %d\n' %category)
    print 'precision: %.5f' %precision
    g.write('precision: %.5f\n' %precision)
    print 'recall: %.5f' %recall
    g.write('recall: %.5f\n' %recall)
    print 'F1: %.5f' %f1
    g.write('F1: %.5f\n' %f1)
    print '================'

if __name__ == '__main__':
    for c in xrange(1,8):
        test(c)
