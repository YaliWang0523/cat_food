# 從成份中分析出給 jieba 的新詞匯

import pandas as pd
import jieba as jb
import numpy as np
import sys
import io

# utf-8編碼處理
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
FILE_SRC = "/Users/yali-mac/Desktop/food3.json"

class SearchNewWord():
	def start(self):
		
		df = self.open_file()
		name = self.get_analytical_constituents_str(df)
		con_list = self.jieba_process(name)
		ser = self.replace_symbol(con_list)
		new_word_list = self.get_new_word_list(ser)
		clean_dup_and_nan = self.clean_dup_and_nan(new_word_list)
		print(len(clean_dup_and_nan))
		for word in clean_dup_and_nan:
			print(word)
		
		# 去掉重覆，回傳list
	def clean_dup_and_nan(self,new_word_list):
		new_list = []
		for i in new_word_list:
			name = i.replace('nan','')
			if len(new_list) == 0:
				new_list.append(name)
			for j in new_list:
				if name == j:
					break
			else:
				new_list.append(name)

		return new_list


	# 重新組字，回傳list
	def get_new_word_list(self,con_ser):
		ser_not_empty = con_ser[con_ser.notnull()]
		single_word = ser_not_empty[ser_not_empty.str.len() == 1]
		new_word_list = []
		for i in single_word.keys():
			new_word_list.append(str(con_ser[i-1]) + str(con_ser[i]) + str(con_ser[i+1]))
		return new_word_list

	# 去掉符號，回傳series
	def replace_symbol(self,con_list):
		ser = pd.Series(con_list)
		num = pd.to_numeric(ser, errors='coerce')
		not_num = num[num.notnull()]
		for i in not_num.keys():
			ser[i] = np.nan
		for j in ser.keys():
			if isinstance(ser[j], str):
				ser[j] = ser[j].strip()
		ser = ser.replace('',np.nan)
		ser = ser.replace(' ' ,np.nan)
		ser = ser.replace('%',np.nan)
		ser = ser.replace('、',np.nan)
		ser = ser.replace(' (',np.nan)
		ser = ser.replace(' )',np.nan)
		ser= ser.replace('(',np.nan)
		ser= ser.replace(')',np.nan)
		ser = ser.replace('）',np.nan)
		ser = ser.replace('（',np.nan)
		ser = ser.replace('g' ,np.nan)
		ser = ser.replace(':' ,np.nan)
		ser = ser.replace('：',np.nan)
		ser = ser.replace('~' ,np.nan)
		ser = ser.replace('，',np.nan)
		ser = ser.replace(',',np.nan)
		ser = ser.replace(';',np.nan)
		ser = ser.replace('；',np.nan)
		ser = ser.replace('%',np.nan)
		ser = ser.replace('％',np.nan)
		ser = ser.replace('%',np.nan)
		ser = ser.replace('。',np.nan)
		ser = ser.replace('mg',np.nan)
		ser = ser.replace('每',np.nan)
		ser = ser.replace('克',np.nan)
		ser = ser.replace('份',np.nan)
		ser = ser.replace('.',np.nan)
		ser = ser.replace('杯',np.nan)
		ser = ser.replace('公克',np.nan)
		ser = ser.replace('毫克',np.nan)
		ser = ser.replace('↑',np.nan)
		ser = ser.replace('↓',np.nan)
		ser = ser.replace('',np.nan)
		ser = ser.replace('"',np.nan)

		return ser

	# 用jieba分解，存成series回傳
	def jieba_process(self,str_name):
		jb.load_userdict("/Users/yali-mac/Documents/cat_food/cat_food/userdict.txt")
		jb_result = jb.cut(str_name,cut_all=False)
		result = '/'.join(jb_result)
		con_list = []
		con_list = result.split('/')
		return con_list

	# 取得成份，回傳字串
	def get_analytical_constituents_str(self,df):
		ser = df['analytical_constituents']
		name = str.join('、',ser)
		name = name.replace('mg','')
		name = name.replace('%','')
		name = name.replace('≦','')
		name = name.replace('≧','')
		name = name.replace('０.','0.')
		name = name.replace('１０','10')
		name = name.replace('１1','11')
		name = name.replace('蛋 白 質','蛋白質')
		name = name.replace('脂 肪','脂肪')
		name = name.replace('灰 分','灰分')
		return name
	# 載入檔案
	def open_file(self):
		df = pd.read_json(open(FILE_SRC, encoding='utf-8'))
		return df



SearchNewWord().start()