# coding=UTF-8
__author__ = 'mac'
import operator
for i in xrange(7):
    file1 = open('ngram/1-50_'+str(i+1)+'.txt','r')
    file2 = open('ngram/51-100_'+str(i+1)+'.txt','r')
    output = open('ngram/total_'+str(i+1)+'.txt','w')
    stop = open('stopword.txt','r')


    nGram = {}
    stopword = set()

    for line in stop:
        token = line.split()
        #print(token)
        word = token[0]

        stopword.add(word)

    for line in file1:
        token = line.split()
        #print(token)
        word = token[0]
        if word in stopword:
            continue
        nGram[word] = int(token[1])

    for line in file2:
        token = line.split()
        #print(token)
        word = token[0]
        if word in stopword:
            continue
        if word in nGram:
            nGram[word] += int(token[1])
        else:
            nGram[word] = int(token[1])

    #print(nGram)


    nGramSorted = sorted(nGram.items(), key=operator.itemgetter(1), reverse=True)
    print(nGramSorted)
    for key, value in nGramSorted:
        #key
        output.write(key+' '+str(value)+'\n')
        print(key)
        print(value)
