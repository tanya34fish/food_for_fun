# -*- coding: utf-8 -*-
import sys
import os
import re

punc_list = ["，","。","！","？","～","…","；"]
normal_punc_list = [',','!','?','~',';']
paren_list = ["（","）","［","］","「","」","〈","〉","《","》","【", "】"]
normal_paren_list = ['(',')','[',']','{','}', "\""]

def clean(para):
	"""return 0: break, return 1: continue, other: write content"""
	if not para.strip():
		return 1
	if "延伸閱讀" in para:
		return 0
	
	para = re.sub('[\n]+', '\n', para)

	"""split by '。'"""
	if para.count(punc_list[1]) > 0:
		para = para.replace('\n', '')
		para = re.sub(punc_list[1], '\n', para)
	else:
		linec = para.count('\n')
		#if para.count(punc_list[0]) + para.count(normal_punc_list[0]) > linec:
		
	for punc in punc_list:
		para = re.sub(punc, ',', para)
	for punc in normal_punc_list:
		para = re.sub('[%s]+' %punc, ',', para)
	for punc in paren_list:
		para = re.sub(punc, ',', para)
	for punc in normal_paren_list:
		para = re.sub('[%s]+' %punc, ',', para)
	para = para.strip()
	"""some special cases:"""
	"""1: XDDDD"""
	para = re.sub('X[D]+',',', para)

	"""2: &gt, &lt"""
	para = re.sub('&gt', '', para)
	para = re.sub('&lt', '', para)

	"""3: &amp"""
	para = re.sub('&amp,', '&', para)

	"""4: 全型空白"""
	para = re.sub("　", ',', para)	
	para = re.sub('[ \t]+','', para)
	
	"""5: ："""
	para = re.sub("：", ',', para)

	"""6: ....."""
	para = re.sub('\.[\.]+', '\n', para)

	"""7: :)"""
	para = re.sub(":", '', para)

	"""some special replace"""
	"""1: 惹"""
	para = para.replace("惹","了")
	"""2: 注音文"""
	para = para.replace("ㄌ","了")
	para = para.replace("ㄋ","呢")
	para = para.replace("ㄅ","吧")
	para = para.replace("ㄏ","哈")
	para = para.replace("ㄉ","的")
	para = para.replace("ㄎ",'')
	"""3: 幾霸摳"""
	para = para.replace("幾霸摳", "100元")
	para = para.replace("擠霸摳", "100元")

	"""price"""
	para = re.sub(r'(\$\d+)',r'\1,', para)
	para = re.sub('[,]+', ',', para)
	para = re.sub(r'(NT.*\d+)',r'\1,', para)
	
	
	"""signature"""
	para = re.sub(r'--\n.*', '', para, flags=re.DOTALL)
	para = re.sub(r'--', '', para)

	"""final prune"""
	para = re.sub('[,]+', ',', para)
	para = re.sub(r",\n", '\n', para)
	para = re.sub(r",$", '', para, flags=re.M)
	para = re.sub("^,", '', para, flags=re.M)
	para = re.sub('-[-]+', '', para)
	para = re.sub('[ \t]+','', para)
	para = re.sub('[\n]+', '\n', para)
	
	
	if para == '':
		return 1
	else:
		return para

def parse_data(doc, output):
	"""split by paragraph"""
	doc = doc.strip()
	
	para_num = doc.count('\n\n')
	line_num = doc.count('\n')
	# if the author loves 2 newlines for every sentence
	if (line_num - para_num)/2 <= para_num:
		print 'The author loves 2 newlines for every sentence'
		cont = re.split("\n\n[\n]+", doc)
	else:
		cont = re.split("\n\n", doc)
	# omit header (3 lines)
	head = cont[0]
	#print head
	end_of_des = 0
	for i in range(1,len(cont)):
		if 'http' in cont[i] and ("圖文" in cont[i] or "網誌" in cont[i] or "版" in cont[i]):
			end_of_des = i
			break
	description = cont[1:end_of_des+1]
	g = open(output, 'w')
	g.write(head)
	g.write('\n')

	des_tag = ["餐廳","時間","地址","電話","每人平均價位","刷卡","包廂","推薦","FB", "ＦＢ","官網", 'http']

	for des in description:
		real_des = ''
		miss_content = ''
		des = re.sub('[\n]+', '\n', des)
		#print des
		#print '====='
		entry_list = des.strip().split('\n')
		miss_idx = 0
		for i in range(1,len(entry_list)):
			tag_hit = False
			pre_line = entry_list[i-1].strip()
			cur_line = entry_list[i].strip()
			for tag in des_tag:
				if (tag in pre_line) or (tag in cur_line):
					real_des += pre_line + '\n'
					tag_hit = True
					break
			# error split on some contents
			miss_idx = i
			if not tag_hit:
				break
		for i in range(miss_idx,len(entry_list)):
			if entry_list[i].strip():
				miss_content += entry_list[i].strip() + '\n'
		g.write(real_des)
		g.write(miss_content)
		#for line in entry_list:
		#	tag_hit = False
		#	if 'http' in line:
		#		continue
		#	for tag in des_tag:
		#		if tag in line:
		#			real_des = line.strip() + '\n'
		#			#g.write(line.strip())
		#			#g.write('\n')
		#			tag_hit = True
		#			break
		#	# error split on some contents
		#	if not tag_hit and line.strip():
		#		miss_content += line + '\n'
	
	#if miss_content.strip():
	#	return_value = clean(miss_content)
	#	if return_value == 0:
	#		pass
	#	elif return_value == 1:
	#		pass
	#	else:
	#		g.write(return_value)
	#		g.write('\n')

	for i in range(end_of_des+1,len(cont)):
		para = cont[i]
		return_value = clean(para)
		if return_value == 0:
			break
		elif return_value == 1:
			continue
		else:
			g.write(return_value)
			g.write('\n')

	g.close()
	return 
	
if __name__ == '__main__':
	filename_list = os.listdir(sys.argv[1])
	idx = 0
	for file in filename_list:
		print 'process %s...' %file
		with open(sys.argv[1] + '/' + file, 'r') as f:
			content = f.read()
		output = sys.argv[2] + '/' + file
		parse_data(content, output)
		idx += 1
		#if idx == 10:
		#	break
