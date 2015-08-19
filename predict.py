# coding=UTF-8
import sys
import glob
import os

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

def gen_feature(category, out_dir, threshold, train=True):
    dir = 'training/training_merge/'
    ngram_im = get_category_im(category, 'word_importance/', threshold)
    ngram_ce = get_category_im(category, 'cross_entropy/', threshold)
    ngram_im_list = list(ngram_im.keys())
    ngram_ce_list = list(ngram_ce.keys())

    g = open(os.path.join(out_dir, 'train_svm_%d.txt' %category), 'w')
    for file_idx in range(200):
        for file in glob.glob(dir + '*_' + str(file_idx+1) + '.txt'):
            if train and (file_idx+1) % 10 == 0:
                continue
            print 'process %s ...' %file
            with open(file, 'r') as f:
                for line in f:
                    token = line.strip().split()
                    ans_label = token[0]
                    # belongs to the specified category
                    
                    if str(category) in ans_label:
                        g.write('1 ')
                    else:
                        g.write('0 ')
                    feature = [0.0, 0.0]
                    for word in token[1:]:
                        try:
                            n = ngram_im_list.index(word)
                        except ValueError:
                            n = -1
                        if n >= 0:
                            feature[0] += ngram_im[word]
                        try:
                            n = ngram_ce_list.index(word)
                        except ValueError:
                            n = -1
                        if n >= 0:
                            feature[1] += ngram_ce[word]
                        
                    for idx in range(len(feature)):
                        if idx == 0:
                            g.write('%d:%.5f ' %(idx+1,feature[idx]))
                        else:
                            g.write('%d:%.5f' %(idx+1,feature[idx]))
                    g.write('\n')
    return

if __name__ == '__main__':
    out_dir = 'svm'
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    for x in range(1,8):
        gen_feature(x, out_dir, threshold, train=True)
