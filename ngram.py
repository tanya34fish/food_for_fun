# coding=UTF-8
import sys
import glob
import os 
import operator 

def get_stopword():
    stop = open('stopword.txt','r')
    stopword = set()

    for line in stop:
        token = line.split()
        word = token[0]
        stopword.add(word)
    stop.close()
    return stopword

def ngram_count(inputdir,outputdir,train=True):

    stopword = get_stopword()
    vocab_list = []
	#ignore vocab_list[0]
    for i in range(9):
        vocab_list.append({})
    train_file_count = 0
    test_file_count = 0
    for file in glob.glob(inputdir +'/*.txt'):
        path, input = os.path.split(file)
        if train:
            idx = int(input.split('_')[1].split('.')[0])
            """ '10,20,30,....,190,200' for testing (no 180)
            """
            if idx % 10 == 0:
                test_file_count += 1
                continue
        with open(file, 'r') as f:
            #print file
            for line in f:
                line_arr = line.strip().split(" ")
                id_list = line_arr[0].split(',')
                for i in range(1, len(line_arr)):
                    name = line_arr[i]
                    if name in stopword:
                        continue
                    for j in id_list:
                        if name in vocab_list[int(j)]:
                            vocab_list[int(j)][name] += 1
                        else:
                            vocab_list[int(j)][name] = 1

        train_file_count += 1
    print 'read %d training files done.' %train_file_count
    print 'exclude %d testing files done.' %test_file_count

    for i in range(1, 9):
        nGramSorted = sorted(vocab_list[i].items(), key=operator.itemgetter(1), reverse=True)
        #print "Dict in " + str(i)
        output = open(os.path.join(outputdir, str(i) +'.txt'), 'w')
        for key, val in nGramSorted:
            if key == '':
                continue
            output.write(key)
            output.write('\t'+str(val)+'\n')
        output.write('\n')
        output.close()

    total_vocab = vocab_list[1].copy()
    for i in xrange(2,8):
        for key,value in vocab_list[i].items():
            if key in total_vocab:
                total_vocab[key] += value
            else:
                total_vocab[key] = value

    output = open(os.path.join(outputdir, '1-7total.txt'), 'w')
    nGramSorted = sorted(total_vocab.items(), key=operator.itemgetter(1), reverse=True)
    for key, val in nGramSorted:
        if key == '':
            continue
        output.write(key)
        output.write('\t'+str(val)+'\n')
    output.write('\n')
    output.close()
    
    return vocab_list

def word_importance():
    total_ngram = {}
    with open('ngram/train/1-8total.txt', 'r')  as f:
        for line in f:
            if not line.strip():
                continue
            tmp = line.strip().split('\t')
            total_ngram[tmp[0]] = int(tmp[1])

    category_ngram_list = [[] for i in range(7)]
    category_total_count_list = [0] * 7
    for i in xrange(7):
        with open('ngram/train/%d.txt' %(i+1), 'r')  as f:
            for line in f:
                if not line.strip():
                    continue
                tmp = line.strip().split('\t')
                category_ngram_list[i].append((tmp[0], int(tmp[1])))
                category_total_count_list[i] += int(tmp[1])
    
    topn = 10
    for c in xrange(7):
        g = open('word_importance/%d.txt' %(c+1), 'w')
        im = {}
        for top_idx in xrange(len(category_ngram_list[c])):
            word, count = category_ngram_list[c][top_idx]
            total_count = total_ngram[word]
            im[word] = (float(count)/float(total_count)) * (float(count)/float(category_total_count_list[c]))
        im_sorted = sorted(im.items(), key=operator.itemgetter(1), reverse=True)
        for word,value in im_sorted:
            g.write(word)
            g.write('\t%.3f\n' %value)
        g.close()
    return

if __name__ == '__main__':
    #inputdir = 'training/training_merge'
    #outputdir = 'ngram/train'
    #vocab_list = ngram_count(inputdir,outputdir,train=True)
    word_importance()
