# -*- coding: utf-8 -*-
# cat_food
# frmdata = {"source_form": "country_zone_query","qrycode": '1', "qrycode3": '貓', "selectpage": '1', "pageto":'1',"pagerecs":'10'}

# url = "http://animal.coa.gov.tw/html2/seekfood.aspx"
# r = FormRequest(url, formdata=frmdata)
# fetch(r)
import scrapy
import re
import json


BASE_URL = "http://animal.coa.gov.tw/html2"
IMG_BASE_URL = "http://animal.coa.gov.tw"
SOURCE_TYPE = "3"

class CatFoodDetailItem(scrapy.Item):
	name_tw = scrapy.Field()
	name_en = scrapy.Field()
	owner = scrapy.Field()
	source = scrapy.Field()
	food_type = scrapy.Field()
	# 淨重
	net_weight = scrapy.Field()
	# 容量
	capacity = scrapy.Field()
	# 添加物
	additives = scrapy.Field()
	# 主要營養成分及含量
	analytical_constituents = scrapy.Field()
	# 適用寵物種類、使用方法及保存方法
	feeding_instructions = scrapy.Field()
	# 產品外包裝照片連結
	photo_src = scrapy.Field()
	#原產地
	country_of_origin = scrapy.Field()
	# 以下資料來自列表
	date_of_applied = scrapy.Field()
	data_detail_src = scrapy.Field()
	data_extra_info = scrapy.Field()

# B:建立具名蜘蛛
class CatfoodSpider(scrapy.Spider):
	"""爬取諾貝爾獎得主的國藉與連結文字"""
	name = 'cat_food'
	allowed_domins = ['animal.coa.gov.tw/html2']
	start_urls = ["http://animal.coa.gov.tw/html2/seekfood.aspx"]
	
	def start_requests(self):
		frmdata = {"source_form": "country_zone_query","qrycode": SOURCE_TYPE, "qrycode3": '貓', "selectpage": '1', "pageto":'1',"pagerecs":'10',"b":'a'}
		return [scrapy.FormRequest("http://animal.coa.gov.tw/html2/seekfood.aspx",formdata=frmdata,callback=self.parse)]

	def requests_callback(self,response):
		pass

	
# C:parse方法處理http回應
	def parse(self,response):
		tables = response.xpath('//table')
		table = tables[2]
		trs = table.xpath('tr')
		tr = trs[11]
		td = tr.xpath('td')[0]
		select = td.xpath('select')[0]
		options = select.xpath('option')
		page = options[len(options) - 1].css('::attr(value)').extract()[0]
		intpage = int(page)
		if intpage > 1:
			for j in range(1,intpage + 1):
				frmdata = {"source_form": "country_zone_query","qrycode": SOURCE_TYPE, "qrycode3": '貓', "selectpage": str(j), "pageto": str(j),"pagerecs":'10'}
				request = scrapy.FormRequest("http://animal.coa.gov.tw/html2/seekfood.aspx",formdata=frmdata,callback=self.parse_detail_page)
				yield request
			

	def parse_detail_page(self,response):
		tables = response.xpath('//table')
		table = tables[2]
		trs = table.xpath('tr')
		for i in range(1,len(trs) -1):
			src = ''
			tr = trs[i]
			tds = tr.xpath('td')
			# 取得連結
			src = BASE_URL + '/' + tds[0].xpath('a/@href')[0].extract()
			for x in range(1,8):
				src = str.replace(src,"&source_type=" + str(x),"")
			request = scrapy.FormRequest(src,callback=self.parse_data)
			list_data = {}
			# 取得申請日
			date_of_applied = tds[3].xpath('text()')[0].extract()
			list_data['date_of_applied'] = date_of_applied + ' 00:00:00'
			# 取得id
			list_data['data_detail_src'] = src
			request.meta['item'] = list_data
			yield request

	def parse_data(self,response):
		date_of_applied = response.meta['item']['date_of_applied']
		data_detail_src = response.meta['item']['data_detail_src']
		tables = response.xpath('//table')
		table = tables[0]
		trs = table.xpath('tr')
		name = ''
		owner = ''
		source = ''
		food_type = ''
		net_weight = ''
		capacity = ''
		additives = ''
		analytical_constituents =''
		feeding_instructions = ''
		photo_src = ''
		country_of_origin =''
		name_tw = ''
		name_en = ''
		data_extra_info = ''
		# 資料
		for i in range(1,len(trs)):	
			tr = trs[i]
			if i == 1:
				td = tr.xpath('td')[1]
				texts = td.xpath('text()').extract()
				all_name = []
				for j in range(len(texts)):
					text = texts[j].strip()
					if text and j == 0:
						name_tw = text
					if text and j == 1:
						name_en = text
				# 有些產品會備註已停售 http://animal.coa.gov.tw/html2/content.aspx?id=A20170800300
				extra_info = td.xpath('font')
				if len(extra_info) > 0:
					data_extra_info = extra_info[0].xpath('text()').extract()[0]
			if i == 2:
				td = tr.xpath('td')[1]
				owner = td.xpath('text()')[0].extract().strip()
			if i == 3:
				td = tr.xpath('td')[1]
				source = td.xpath('text()')[0].extract().strip()
			if i == 4:
				td = tr.xpath('td')[1]
				food_type = td.xpath('text()')[0].extract().strip()
			if i == 5:
				td = tr.xpath('td')[1]
				texts = td.xpath('text()').extract()
				net_weight = array_to_str(texts)
			if i == 6:
				td = tr.xpath('td')[1]
				capacity = td.xpath('text()')[0].extract().strip()
			if i == 7:
				td = tr.xpath('td')[1]
				texts = td.xpath('text()').extract()
				additives = array_to_str(texts)
			if i == 8:
				td = tr.xpath('td')[1]
				texts = td.xpath('text()').extract()
				analytical_constituents = array_to_str(texts)
			if i == 9:
				td = tr.xpath('td')[1]
				feed_items = td.xpath('text()').extract()
				feeding_instructions = array_to_str(feed_items)
			if i == 11:
				td = tr.xpath('td')[1]
				imgs = td.xpath('img')
				photos = []
				if len(imgs) > 0:
					for j in range(len(imgs)):
						photo_src = IMG_BASE_URL + imgs[j].xpath('@src')[0].extract().strip()
						photos.append(photo_src)
			if i == 12:
				td = tr.xpath('td')[1]
				country_of_origin = td.xpath('text()')[0].extract().strip()
		yield CatFoodDetailItem(
			name_tw = name_tw , name_en = name_en , owner = owner,
			source = source , food_type = food_type ,
			net_weight = net_weight , capacity = capacity,
			additives = additives , analytical_constituents = analytical_constituents ,
			feeding_instructions = feeding_instructions , photo_src = photos ,
			country_of_origin = country_of_origin,date_of_applied = date_of_applied ,
			data_detail_src = data_detail_src,data_extra_info = data_extra_info
		)

def array_to_str(array_text):
	texts = []
	result = ''
	# 有些資料會採換行，為取到完整資料，需檢查文字長度
	for j in range(len(array_text)):
		text = array_text[j].strip()
		if text:
			texts.append(text)
	# 取代,，空白
	result = "、".join(str(x) for x in texts)
	return result
