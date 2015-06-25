# coding=UTF-8
from ai import segment
import sys
import glob
label = 7

nGram = {}
file1 = open('ngram/train/'+str(label)+'.txt','r')
ng_num = 1
for line in file1:
    token = line.split()
    #print(token)
    if len(token) > 0:
        nGram[token[0]] = ng_num
        ng_num += 1


f1_bound = 0
freq_best = 1
prec_best = 0
recall_best = 0

for freq in xrange(3, 30):
    vocab_list = []
    lineNum = 0
    label1 = 0
    find1 = 0
    is1 = 0
#label = 'test'
    for i in range(20):
        vocab_list.append({})
    for i in xrange(20):
        for file in glob.glob('training/training_merge/*'+str((i+1)*10)+'.txt'):
        #for file in glob.glob('*.txt'):
            with open(file, 'r') as f:
                lineNum = 0
                for line in f:
                    #print(line)
                    token = line.split()
                    lineNum+=1

                    if str(label) in token[0]:
                        label1+=1
                    for i in xrange(len(token)):
                        if token[i] in nGram and nGram[token[i]] < freq:
                            #print(token[i])
                            find1 +=1
                            if str(label) in token[0]:
                                is1+=1
                            #print(lineNum)
                            break

    recall = float(is1)/label1
    pre = float(is1)/find1
    print 'Test: category %d, Freq: %d' % (label, freq)
    print 'precision: %.5f' %pre
    print 'recall: %.5f' %recall
    print 'F1: %.5f' % (2*float(recall*pre)/(recall+pre))
    print '================'
    if (2*float(recall*pre)/(recall+pre)) > f1_bound:
        f1_bound = (2*float(recall*pre)/(recall+pre))
        freq_best = freq
        prec_best = pre
        recall_best = recall


 
print '\nTest %d' % label
print 'best freq: %d' % freq_best
print 'best precision: %f' % prec_best
print 'best recall: %f' % recall_best
print 'best F1: %f\n' % f1_bound

'''
label              1           2           3           4           5           6           7
freq               7           4          12          13           9           7           9
precision   0.758621    0.869565    0.548387    0.911281    0.448276    1.000000    0.131980
recall      0.550000    0.444444    0.571749    0.832000    0.339130    0.724138    0.553191
F1          0.637681    0.588235    0.559824    0.870293    0.386139    0.840000    0.213115
'''
