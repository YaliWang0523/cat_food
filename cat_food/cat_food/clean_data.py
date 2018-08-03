import pandas as pd
import sys
import io
import json
import pymysql
import sqlalchemy

# utf-8編碼處理
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def get_clean_struct():
	# df = pd.read_json(open('/Users/yali-mac/Desktop/food.json', encoding='utf-8'))
	engine = sqlalchemy.create_engine('mysql+pymysql://root:root@localhost/cat_food?charset=utf8')
	df = pd.read_sql('cat_food_dirty',engine)
	error_datas_struct = []
	# 取得所有欄位名稱
	keys = df.columns
	# 重覆名字的資料集
	dupes_data = df[df.duplicated('name_tw')]
	index = dupes_data.index
	# for in 依重覆資料集名稱取得資料集
	for i in range(len(index)):
		error_data_struct = {}
		rec_diff_datas = ''
		name = dupes_data.at[index[i],'name_tw']
		single_dupes_data_set = df[df.name_tw == name]
		# 比對每個欄位的異質程度
		for key in keys:
			# 不比對圖片來源與資料連結
			if key != 'id' and key != 'photo_src' and key != 'data_detail_src':
				diff_data_num = (single_dupes_data_set[key].describe()[['unique']])
				if diff_data_num[0] > 1:
					if rec_diff_datas:
						rec_diff_datas = rec_diff_datas+ ',' + key + '|'+ str(diff_data_num[0])
					else:
						rec_diff_datas = key + '|'+ str(diff_data_num[0])
		id_set = ''
		single_dupes_data_set_index = single_dupes_data_set.index
		for j in range(len(single_dupes_data_set_index)):
			if id_set:
				id_set = id_set + '|' + str(single_dupes_data_set.at[single_dupes_data_set_index[j],'id'])
			else :
				id_set = str(single_dupes_data_set.at[single_dupes_data_set_index[j],'id'])
		error_data_struct['id'] = id_set
		# error_data_struct['name_tw'] = name
		error_data_struct['content'] = rec_diff_datas
		error_data_struct['count'] = str(single_dupes_data_set.count()[0])
		error_datas_struct.append(error_data_struct)

	with open('/Users/yali-mac/Desktop/data.json', 'w', encoding='utf-8') as outfile:
		json.dump(error_datas_struct, outfile)

get_clean_struct()
