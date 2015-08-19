# coding=UTF-8
__author__ = 'mac'
import operator

file = open('7.txt','r')
stop = open('stopword.txt','r')


nGram = {}
stopword = set()
for line in stop:
    token = line.split()
    #print(token)
    word = token[0]

    stopword.add(word)
#print(stopword)
for line in file:
    token = line.split()
    #print(token)
    word = token[0]
    if word not in stopword:
        nGram[word] = int(token[1])

#print(nGram)

nGramSorted = sorted(nGram.items(), key=operator.itemgetter(1), reverse=True)
print(nGramSorted)
for key, value in nGramSorted:
    #key
    print(key)
    print(value)
