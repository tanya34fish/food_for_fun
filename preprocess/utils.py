# coding=UTF-8
from ai import segment
import sys
import glob
import os

def pos_category():
	for file in glob.glob(sys.argv[1] + '/*.txt'):
		print 'process %s...' %file
		path, input = os.path.split(file)
		idx = int(input.split('_')[1].split('.')[0])
		#if idx <= 263:
		#	continue
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

def split_sentence():
	# split sentence from "word:pos" file
	for file in glob.glob(sys.argv[1] + '/*.txt'):
		print 'split sentence %s...' %file
		path, input = os.path.split(file)
		output = os.path.join(sys.argv[2], input)
		g = open(output, 'w')
		with open(file, 'r') as f:
			for line in f:
				word_list = line.strip().split('\t')
				for i in range(len(word_list)):
					w = word_list[i].split(':')
					g.write(w[0])
					if i != len(word_list) - 1:
						g.write(' ')
				g.write('\n')
			g.close()
	return
	

def write_nolabel_file():
	for file in glob.glob(sys.argv[1] + '/*.txt'):
		print 'process %s...' %file
		path, input = os.path.split(file)
		idx = int(input.split('_')[1].split('.')[0])
		#if idx < 1 or idx > 100:
		#	continue
		output = os.path.join(sys.argv[2], input)
		g = open(output, 'w')
		with open(file, 'r') as f:
			for line in f:
				line_arr = line.strip().split(' ')
				if line_arr[0] >= '1' and line_arr[0] <= '7' and (line[1] == ',' or line[1] == ' '):
					for i in range(1,len(line_arr)):
						g.write(line_arr[i])
					g.write('\n')
				else:
					for i in range(len(line_arr)):
						g.write(line_arr[i])
					g.write('\n')
		g.close()

def gen_ans_file():
	for file in glob.glob(sys.argv[1] + '/*.txt'):
		print 'process %s...' %file
		path, input = os.path.split(file)
		idx = int(input.split('_')[1].split('.')[0])
		#if idx < 1 or idx > 100:
		#	continue
		output = os.path.join(sys.argv[2], input)
		g = open(output, 'w')
		with open(file, 'r') as f:
			for line in f:
				line_arr = line.strip().split(' ')
				if line_arr[0] >= '1' and line_arr[0] <= '7' and (line[1] == ',' or line[1] == ' '):
					g.write(line_arr[0])
				else:
					g.write('8')
				g.write('\n')
		g.close()

def merge_seg_label():
	for file in glob.glob(sys.argv[1] + '/*.txt'):
		print 'process %s...' %file
		path, input = os.path.split(file)
		ans = os.path.join('training/training_ans', input)
		output = os.path.join(sys.argv[2], input)
		
		g = open(output, 'w')
		seg_list = []
		ans_list = []
		with open(file, 'r') as f, open(ans, 'r') as h:
			for line in f:
				seg_list.append(line.strip())
			for line in h:
				ans_list.append(line.strip())

		for (line, ans) in zip(seg_list,ans_list):
			g.write('%s %s\n' %(ans, line))
		g.close()
if __name__ == '__main__':
	merge_seg_label()
