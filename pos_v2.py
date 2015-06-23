# coding=UTF-8
from ai import segment
import sys
import glob
import os
from multiprocessing import Process

def pos_category(start, end):
	for file in glob.glob(sys.argv[1] + '/*.txt'):
		path, input = os.path.split(file)
		idx = int(input.split('_')[1].split('.')[0])
		if idx < start or idx >= end:
			continue
		print 'process %s...' %file
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
					g.write('\n')
		g.close()

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

if __name__ == '__main__':
#	p = []
#for i in range(1,10):
#    p.append(Process(target=pos_category, args= ((i)*10,(i+1)*10)))
#for i in range(9):
#    p[i].start()
	pos_category(100,101)
