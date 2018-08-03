
keys = df.columns
# 重覆名字的資料集
dupes_data = df[df.duplicated('name_tw')]

# for in 依重覆資料集名稱取得資料集
a = df[df.name_tw == dupes_data.get_value(index[i],'name_tw')]

rec_diff_datas = ''
# 比對每個欄位的異質程度
for key in keys:
	# 不比對圖片來源與資料連結

	if key != 'photo_src':
		diff_data_num = (a[key].describe()[['unique']])
		if diff_data_num > 1:
			if not rec_diff_datas:
				rec_diff_datas = rec_diff_datas+ ',' + a[key] + '| '+ str(diff_data_num)
			else:
				rec_diff_datas = a[key] + '| '+ str(diff_data_num)
			yeild()
