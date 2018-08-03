# 從爬回來的成份欄位擷取有用資料
import pandas as pd
import pymysql
import sqlalchemy
import jieba as jb
import numpy as np
import sys
import io
import json

# utf-8編碼處理
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
FILE_SRC = "/Users/yali-mac/Desktop/food3.json"

class Analytics_con():
	def start(self):
		df = self.get_df_from_my_sql()
		ser = self.get_ser_analytical_constituents(df)
		result_list = self.parse_by_jieba(ser)
		data = self.get_Kcal(result_list)
		self.save_json(data)


	# # 寫入json
	def save_json(self,data):
		with open("/Users/yali-mac/Desktop/aaa.json", 'w', encoding='utf8') as json_file:
			json.dump(data, json_file, ensure_ascii=False)
		
	# 取熱量
	def get_Kcal(self,result_list):
		cons = []
		for i in range(1,len(result_list)):
			a = result_list[i]
			con = a.split('|')
			constituents = con[1].split('/')
			num = 0.0
			count_con = len(constituents)
			get_value = False
			unit = ''
			for j in range(count_con):

				if constituents[j].strip() == "熱量" or constituents[j].strip() == "總熱量" or constituents[j].strip() == "熱量約":
					get_value = True
				if constituents[j].strip() == "公斤" or constituents[j].strip().lower() == "kg" or constituents[j].strip().lower() == "100g" or constituents[j].strip() == "袋" or constituents[j].strip() == "100克" or constituents[j].strip() == "100公克" or constituents[j].strip() == "120g" or constituents[j].strip() == "罐":
						unit = constituents[j]
				if get_value and isfloat(constituents[j]) and (num == "0.0" or num == 0.0):
					num = constituents[j]
					if(constituents[j + 1]):
						if (constituents [j+1]) == ',':
							num = constituents[j] + constituents [j+2]		
			else:
				b='b'
			if str(num) != "0.0" :
				cons.append({'id':con[0] , 'kcal':str(float(num)) , 'unit' : unit})
		return cons

	# 用jb分析,回傳[]
	def parse_by_jieba(self,ser):
		data = []
		jb.load_userdict("/Users/yali-mac/Documents/cat_food/cat_food/userdict.txt")
		for i in ser.keys():
			name = ser[i]
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
			jb_result = jb.cut(name,cut_all=False)
			result = str(i+1) + '|' + '/'.join(jb_result)
			data.append(result)
		return data
	# 取得成份欄位，回傳ser
	def get_ser_analytical_constituents(self,df):
		ser = pd.Series(df['analytical_constituents'])
		return ser	

	# 載入sql，回傳df
	def get_df_from_my_sql(self):
		engine = sqlalchemy.create_engine('mysql+pymysql://root:root@localhost/cat_food?charset=utf8')
		df = pd.read_sql('cat_food_dirty',engine)
		return df

def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False

Analytics_con().start()