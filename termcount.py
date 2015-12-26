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
"""
    calculate total term counts for start:end in training data
    @outputdir: ngram/training
    @start: 1 (label)
    @end: 7 (label)
    @vocab_list: a list that records term counts for each label set
"""
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

"""
    calculate term counts for each label (1-8) in training data
    also calculate total term counts for 1-7 labels and 1-8 labels
    @inputdir: data/training_data/training_merge
    @outputdir: ngram/training || ngram/total
    @train: if True, just term counts in training data
            else, term counts in total data
"""
def term_count(inputdir,outputdir,train=True):

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
            for line in f:
                line_arr = line.strip().split(" ") 
                # labels
                id_list = line_arr[0].split(',')
                # terms
                for i in range(1, len(line_arr)):
                    term = line_arr[i]
                    if term in stopword:
                        continue
                    for j in id_list:
                        if term in vocab_list[int(j)]:
                            vocab_list[int(j)][term] += 1
                        else:
                            vocab_list[int(j)][term] = 1

        train_file_count += 1
    print 'read %d training files done.' %train_file_count
    print 'exclude %d testing files done.' %test_file_count

    for i in range(1, 9):
        nGramSorted = sorted(vocab_list[i].items(), key=operator.itemgetter(1), reverse=True)
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

"""
    read term counts from file for convenience
    input:
        @termcount_file: total term count file
    output:
        @total_ngram: total term count dict
        @category_ngram_list: a list records term count for each label set
        @category_total_count_list: a list records total term counts
"""
def get_count_statistics(termcount_file):
    total_ngram = {}
    with open(termcount_file, 'r')  as f:
        for line in f:
            if not line.strip():
                continue
            tmp = line.strip().split('\t')
            total_ngram[tmp[0]] = int(tmp[1])

    category_ngram_list = [{} for i in range(8)]
    category_total_count_list = [0] * 8
    
    for i in xrange(8):
        with open('termcount/train/%d.txt' %(i+1), 'r')  as f:
            for line in f:
                if not line.strip():
                    continue
                tmp = line.strip().split('\t')
                category_ngram_list[i][tmp[0]] = int(tmp[1])
                category_total_count_list[i] += int(tmp[1])

    return total_ngram, category_ngram_list, category_total_count_list

"""
    calculate word importance of terms for each label set
    use metric: word importance = total_ratio * category_ratio
"""
def word_importance(total_ngram, category_ngram_list, category_total_count_list):
    dir = 'word_importance/'
    for c in xrange(8):
        g = open(dir + '%d.txt' %(c+1), 'w')
        im = {}
        for word, count in category_ngram_list[c].iteritems():
            total_count = total_ngram[word]
            category_ratio = float(count)/float(category_total_count_list[c])
            total_ratio = float(count)/float(total_count)
            im[word] = category_ratio * total_ratio
        im_sorted = sorted(im.items(), key=operator.itemgetter(1), reverse=True)
        for word, value in im_sorted:
            g.write(word)
            g.write('\t%.3f\n' %value)
        g.close()
    return

"""
    calculate expected cross entropy (ECE) of terms for each label set
    Reference: Combining Lexical and Semantic Features for Short Text Classification, KES, 2013
"""
def cross_entropy(total_ngram, category_ngram_list, category_total_count_list):
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

def main():
    inputdir = 'data/training_data/training_merge'
    outputdir = 'termcount/train'
    term_count(inputdir,outputdir,train=True)
    total_ngram, category_ngram_list, category_total_count_list = get_count_statistics('termcount/train/1-8total.txt')
    word_importance(total_ngram,category_ngram_list,category_total_count_list)
    cross_entropy(total_ngram,category_ngram_list,category_total_count_list)

if __name__ == '__main__':
    main()