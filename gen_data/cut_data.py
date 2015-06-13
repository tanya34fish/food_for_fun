# -*- coding: utf-8 -*-
import sys
import os
import re

punc_list = ["，","。","！","？","～","…","（","）","［","］","「","」","〈","〉","《","》","；"]
normal_punc_list = [',','!','?','~','(',')','[',']','{','}',';']

def parse_data(cont):
	cont = cont.strip().split('\n')
	# omit header (4 lines)
	head = cont[:3]
	end_of_des = 0
	for i in range(4,len(cont)):
		if not cont[i].strip():
			continue
		else:
			if 'http' in cont[i]:
				end_of_des = i
				break
	des = cont[4:end_of_des+1]
	cont = ''.join(cont[end_of_des+1:])
	# '\n' to ' ' and split by '。'
	if cont.count(punc_list[1]) > 10:
		cont = cont.replace('\n', ' ')
	# else: split by '\n'
	cont = re.sub('[ \t]+',' ',cont)
	for punc in punc_list:
		cont = re.sub(punc, '\n', cont)
	for punc in normal_punc_list:
		cont = re.sub('[%s]+' %punc, '\n', cont)
	cont = re.sub('[ \t]+', '', cont)
	cont = re.sub('-[-]+', '', cont)
	cont = re.sub('&gt[\n]*["]*&lt', '', cont)
		
	cont = re.sub('[\n]+', '\n', cont)
	new_cont = ''
	new_cont += '\n'.join(head)
	for d in des:
		if not d.strip():
			continue
		new_cont += re.sub('[ \t]+','',d.strip()) + '\n'
	new_cont += cont
	return new_cont
	
if __name__ == '__main__':
	filename_list = os.listdir(sys.argv[1])
	idx = 0
	for file in filename_list:
		with open(sys.argv[1] + '/' + file, 'r') as f:
			content = f.read()
		content = parse_data(content)
		with open(sys.argv[2] + '/' + file, 'w') as g:
			g.write(content)
		idx += 1
		#if idx > 10:
		#	break
