# coding=UTF-8
from ai import segment
import sys
import glob
import os

def pos_category():
	vocab_list = []
	for i in range(10):
		vocab_list.append({})

	for file in glob.glob(sys.argv[1] + '/*.txt'):
		print 'process %s...' %file
		path, input = os.path.split(file)
		idx = int(input.split('_')[1].split('.')[0])
		if idx > 100:
			continue
		output = os.path.join(sys.argv[2], input)
		g = open(output, 'w')
		with open(file, 'r') as f:
			for line in f:
				line_arr = line.strip().split(' ')
				#if line_arr[0] >= '1' and line_arr[0] <= '7' and (line[1] == ',' or line[1] == ' '):
					#id_list = line_arr[0].split(',')
				for i in range(len(line_arr)):
					if not line_arr[i].strip():
						continue
					ans = segment(line_arr[i].strip())
					# if get nothing / error
					if ans == 'Fail':
						print 'error'
						print line_arr[i].strip()
						continue
					for name, tp in ans:
						g.write(name.encode('utf-8'))
						g.write(':')
						g.write('%s\t' %tp)
						#for j in id_list:
						#	if name in vocab_list[int(j)]:
						#		if tp in vocab_list[int(j)][name]:
						#			vocab_list[int(j)][name][tp] += 1
						#		else:
						#			vocab_list[int(j)][name] = {}
						#			vocab_list[int(j)][name][tp] = 1
						#	else:
						#		vocab_list[int(j)][name] = {}
						#		vocab_list[int(j)][name][tp] = 1
					g.write('\n')
		g.close()

	
	#for i in range(len(vocab_list)):
	#	f = open('category_%d.txt' %i, 'w')
	#	f.write('Category %d:\n' %(i))
	#	for (key,value) in vocab_list[i].items():
	#		f.write(key.encode('utf-8'))
	#		f.write(':\n')
	#		for (tp,count) in sorted(value.items(), key=lambda x:x[1]):
	#			f.write('%s,%d\n' %(tp,count))
	#	f.write('\n')

def cut_useless_category():
	for file in glob.glob(sys.argv[1] + '/*.txt'):
		print 'process %s...' %file
		path, input = os.path.split(file)
		output = os.path.join(sys.argv[2], input)
		g = open(output, 'w')
		with open(file, 'r') as f:
			for line in f:
				if not line.strip():
					continue
				line_arr = line.strip().split(' ')
				if '8' in line_arr[0] or '9' in line_arr[0]:
					pass
				else:
					g.write(line_arr[0]+' ')
				for i in range(1,len(line_arr)):
					g.write(line_arr[i]+' ')
				g.write('\n')
			g.close()

def get_sentence_pos():
	for file in glob.glob(sys.argv[1] + '/*.txt'):
		print 'process %s...' %file
		path, input = os.path.split(file)
		output = os.path.join(sys.argv[2], input)
		g = open(output, 'w')
		with open(file, 'r') as f:
			for line in f:
				if not line.strip():
					continue
				print line
				ans = segment(line.strip())
				for name, tp in ans:
					g.write(name.encode('utf-8'))
					g.write(':')
					g.write('%s\t' %tp)
				g.write('\n')
			g.close()
	return

def write_nolabel_data():
	for file in glob.glob(sys.argv[1] + '/*.txt'):
		print 'process %s...' %file
		path, input = os.path.split(file)
		output = os.path.join(sys.argv[2], input)
		g = open(output, 'w')
		with open(file, 'r') as f:
			for line in f:
				line_arr = line.strip().split(' ')
				if line_arr[0] >= '1' and line_arr[0] <= '7' and (line[1] == ',' or line[1] == ' '):
				for i in range(len(line_arr)):
					if not line_arr[i].strip():
						continue
				if not line.strip():
					continue
				print line
				ans = segment(line.strip())
				for name, tp in ans:
					g.write(name.encode('utf-8'))
					g.write(':')
					g.write('%s\t' %tp)
				g.write('\n')
			g.close()
	return
if __name__ == '__main__':
	pos_category()
