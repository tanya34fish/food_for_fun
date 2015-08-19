# coding=UTF-8
import sys
import glob
import os 
import operator 
import math

def get_stopword():
    stop = open('stopword.txt','r')
    stopword = set()

    for line in stop:
        token = line.split()
        word = token[0]
        stopword.add(word)
    stop.close()
    return stopword

def count_total(outputdir, start, end, vocab_list):
    total_vocab = vocab_list[start].copy()
    for i in xrange(start+1,end+1):
        for key,value in vocab_list[i].items():
            if key in total_vocab:
                total_vocab[key] += value
            else:
                total_vocab[key] = value

    output = open(os.path.join(outputdir, '%d-%dtotal.txt' %(start,end)), 'w')
    nGramSorted = sorted(total_vocab.items(), key=operator.itemgetter(1), reverse=True)
    for key, val in nGramSorted:
        if key == '':
            continue
        output.write(key)
        output.write('\t'+str(val)+'\n')
    output.write('\n')
    output.close()
    return

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

    count_total(outputdir, 1, 7, vocab_list)
    count_total(outputdir, 1, 8, vocab_list)

def get_count_statistics():
    total_ngram = {}
    with open('ngram/train/1-8total.txt', 'r')  as f:
        for line in f:
            if not line.strip():
                continue
            tmp = line.strip().split('\t')
            total_ngram[tmp[0]] = int(tmp[1])

    category_ngram_list = [{} for i in range(8)]
    category_total_count_list = [0] * 8
    for i in xrange(8):
        with open('ngram/train/%d.txt' %(i+1), 'r')  as f:
            for line in f:
                if not line.strip():
                    continue
                tmp = line.strip().split('\t')
                category_ngram_list[i][tmp[0]] = int(tmp[1])
                #category_ngram_list[i].append((tmp[0], int(tmp[1])))
                category_total_count_list[i] += int(tmp[1])
    return total_ngram,category_ngram_list,category_total_count_list

def word_importance(total_ngram,category_ngram_list,category_total_count_list):
    topn = 10
    for c in xrange(8):
        g = open('word_importance/%d.txt' %(c+1), 'w')
        im = {}
        for word,count in category_ngram_list[c].iteritems():
            total_count = total_ngram[word]
            im[word] = float(count)/float(total_count) * float(count)/float(category_total_count_list[c])
        im_sorted = sorted(im.items(), key=operator.itemgetter(1), reverse=True)
        for word,value in im_sorted:
            g.write(word)
            g.write('\t%.3f\n' %value)
        g.close()
    return

def cross_entropy(total_ngram,category_ngram_list,category_total_count_list):
    dir = 'cross_entropy/'
    ece = {}
    total_count = 0
    for c in category_total_count_list:
        total_count += c
    for key,value in total_ngram.iteritems():
        for c in xrange(8):
            try:
                p_w_given_c = float(category_ngram_list[c][key])/ float(category_total_count_list[c])
            except KeyError:
                ece.setdefault(key,[]).append(0.0)
                continue
            try:
                p_c_given_w = float(category_ngram_list[c][key])/ float(total_ngram[key])
            except KeyError:
                ece.setdefault(key,[]).append(0.0)
                continue
            p_c = float(category_total_count_list[c]) / float(total_count)
            weight = p_w_given_c * p_c_given_w * math.log(p_c_given_w/float(p_c))
            ece.setdefault(key,[]).append(weight)
    
    for c in xrange(8):
        category_im = {}
        for key,w_list in ece.iteritems():
            final = ece[key][c] - sum([w_list[a] for a in range(len(w_list)) if a != c]) 
            category_im[key] = final
        sorted_category_im = sorted(category_im.items(), key=operator.itemgetter(1), reverse=True)
        with open(dir + '%d.txt' %(c+1), 'w') as g:
            for key,value in sorted_category_im:
                g.write(key)
                g.write('\t%.5f\n' %value)
    return

if __name__ == '__main__':
    inputdir = 'training/training_merge'
    outputdir = 'ngram/train'
    ngram_count(inputdir,outputdir,train=True)
    total_ngram,category_ngram_list,category_total_count_list = get_count_statistics()
    word_importance(total_ngram,category_ngram_list,category_total_count_list)
    cross_entropy(total_ngram,category_ngram_list,category_total_count_list)
