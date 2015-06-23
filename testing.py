# coding=UTF-8
from ai import segment
import sys
import glob
label = 7
freq = 5

nGram = {}
file1 = open('ngram/train_'+str(label)+'.txt','r')
for line in file1:
    token = line.split()
    #print(token)
    word = token[0]
    nGram[word] = int(token[1])

vocab_list = []
print(nGram)
lineNum = 0
label1 = 0
find1 = 0
is1 = 0
#label = 'test'
for i in range(10):
    vocab_list.append({})
for i in xrange(10):
    for file in glob.glob('training/training_merge/*'+str((i+1)*10)+'.txt'):
    #for file in glob.glob('*.txt'):
        with open(file, 'r') as f:
            print file
            lineNum = 0
            for line in f:
                #print(line)
                token = line.split()
                lineNum+=1

                if int(token[0]) == label:
                    label1+=1
                for i in xrange(len(token)):
                    if token[i] in nGram and nGram[token[i]]>=freq:
                        #print(token[i])
                        find1 +=1
                        if int(token[0]) == label:
                            is1+=1
                        print(lineNum)
                        break


print(label1)
print(find1)
print(is1)
print(float(is1)/label1)
print(float(is1)/find1)
recall = float(is1)/label1
pre = float(is1)/find1
print(2*float(recall*pre)/(recall+pre))

"""

            break
            ans = segment(line.strip())
            #print(ans)
            for name, tp in ans:
                #print(name)
                #name
                if name in nGram and nGram[name]>3:
                    print(name)
                    print(line)

            #line_arr = line.strip().split(" ")
            #print(line_arr)

            #break

            if line_arr[0] >= '1' and line_arr[0] <= '7' and (line[1] == ',' or line[1] == ' '):
                id_list = line_arr[0].split(',')

            for i in range(1, len(line_arr)):
                #print(line_arr[i])
                ans = segment(line_arr[i].strip())
                #print(ans)
                for name, tp in ans:
                    print(name)
                    #break
"""
                            #else:
                                #vocab_list[int(j)][name] = 1

"""
for i in range(1, 8):
    print "Dict in " + str(i)
    output = open(label+'_'+str(i)+'.txt', 'w')

    for key, val in vocab_list[i].items():
        print key.encode("UTF-8"), val
        output.write(key.encode("UTF-8")+'\t'+str(val)+'\n')
    print "\n"
    #output.write('\n')
"""