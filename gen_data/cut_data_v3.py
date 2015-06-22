# -*- coding: utf-8 -*-
import sys
import os
import re

end_list = ["。","！","？","～"]
normal_end_list = ['!','?','~']
punc_list = ["，","…","；"]
normal_punc_list = [',',';']
paren_list = ["（","）","［","］","「","」","〈","〉","《","》","【", "】"]
normal_paren_list = ['(',')','[',']','{','}', "\""]

def punc_remove(para):
	for punc in end_list:
		para = re.sub(punc, '\n', para)
	for punc in normal_end_list:
		para = re.sub('[%s]+' %punc, '\n', para)
	for punc in punc_list:
		para = re.sub(punc, ',', para)
	for punc in normal_punc_list:
		para = re.sub('[%s]+' %punc, ',', para)
	for punc in paren_list:
		para = re.sub(punc, ',', para)
	for punc in normal_paren_list:
		para = re.sub('[%s]+' %punc, ',', para)
	para = para.strip()

	return para

def final_prune(para):
	"""final prune"""
	para = re.sub('[,]+', ',', para)
	para = re.sub(r",\n", '\n', para)
	para = re.sub(r",$", '', para, flags=re.M)
	para = re.sub("^,", '', para, flags=re.M)
	para = re.sub('[ \t]+','', para)
	para = re.sub('[\n]+', '\n', para)
	return para

def special_remove(para):	
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

	"""7: -----"""
	para = re.sub('--[-]+', '', para)
	
	"""8: ===== & =="""
	para = re.sub('=[=]+', '', para)
	
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

	"""4: price"""
	para = re.sub(r'(\$\d+)',r'\1,', para)
	para = re.sub('[,]+', ',', para)
	para = re.sub(r'(NT.*\d+)',r'\1,', para)
	
	
	"""signature"""
	#para = re.sub(r'--\n.*', '', para, flags=re.DOTALL)
	#para = re.sub(r'--', '', para)

	para = final_prune(para)	
	return para

def clean(para):
	"""return 0: break, return 1: continue, other: write content"""
	if not para.strip():
		return 1
	if "延伸閱讀" in para:
		return 0
	
	para = para.replace('\n', '')

	"""split by '。'"""
	if para.count(end_list[0]) > 0:
		para = re.sub(end_list[0], '\n', para)
	
	para = punc_remove(para)
	para = special_remove(para)
	
	if para == '':
		return 1
	else:
		return para

def parse_data(doc, output):
	"""split by paragraph"""
	cont = doc.strip().split('\n')
	# omit header (3 lines)
	head = cont[:3]

	g = open(output, 'w')
	for h in head:
		g.write(h)
		g.write('\n')

	des_tag = ["店名","餐廳","時間","地址","交通","電話","每人平均價位","低消","平日","假日","週","周","刷卡","包廂","推薦菜色","FB", "ＦＢ","官網", 'http']
	end_of_des = 4
	for i in range(4, len(cont)):
		line = cont[i].strip()
		if not line:
			continue
		is_des = False
		for des in des_tag:
			if des in line:
				is_des = True
				#line = punc_remove(line)
				#line = final_prune(line)	
				g.write(line)
				g.write('\n')
				break
		if not is_des:
			end_of_des = i
			g.write('\n')
			break
	
	real_cont = ''
	for i in range(end_of_des,len(cont)):
		line = cont[i].strip()
		if line:	
			if 'http' in line:
				continue
			else:
				real_cont += line + '\n'

	# all contents split by '。'
	if real_cont.count(end_list[0]) > 10:
		real_cont = re.sub(r'\n', '', real_cont)
		para = re.sub(end_list[0], '\n', real_cont)
		para = punc_remove(real_cont)
		para = special_remove(para)
		g.write(para)
		g.write('\n')
	else:
		#print 'here'
		real_cont = re.split(r"\n[\n]+", real_cont)
		for para in real_cont:
			#print '==='
			#print para
			return_value = clean(para)
			#print '==='
			#print return_value
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
		#if idx == 100:
		#	break
