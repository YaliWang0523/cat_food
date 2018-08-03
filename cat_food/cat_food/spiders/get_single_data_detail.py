# 取得明細資料
import scrapy
import re

class CatFoodDetailItem(scrapy.Item):
	name = scrapy.Field()
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
	feedind_instructions = scrapy.Field()
	# 產品外包裝照片連結
	photo_src = scrapy.Field()
	#原產地
	country_of_origin = scrapy.Field()
	# 以下資料來自列表
	date_of_applied = scrapy.Field()
	detail_link = scrapy.Field()


# B:建立具名蜘蛛
class CatfoodDetailSpider(scrapy.Spider):
	"""爬取諾貝爾獎得主的國藉與連結文字"""
	name = 'cat_food_detail'
	allowed_domins = ['animal.coa.gov.tw']
	start_urls = ["http://animal.coa.gov.tw/html2/content.aspx?id=A20180300265"]


	def parse(self,response):
		tables = response.xpath('//table')
		table = tables[0]
		trs = table.xpath('tr')
		# 資料
		for i in range(1,len(trs) - 1):	
			tr = trs[i]
			if i == 1:
				td = tr.xpath('td')[1]
				name = td.xpath('text()')[0].extract().strip()
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
				net_weight = td.xpath('text()')[0].extract().strip()
			if i == 6:
				td = tr.xpath('td')[1]
				capacity = td.xpath('text()')[0].extract().strip()
			if i == 7:
				td = tr.xpath('td')[1]
				additives = td.xpath('text()')[0].extract().strip()
			if i == 8:
				td = tr.xpath('td')[1]
				analytical_constituents = td.xpath('text()')[0].extract().strip()
			if i == 9:
				td = tr.xpath('td')[1]
				feedind_instructions = td.xpath('text()')[0].extract().strip()
			if i == 10:
				# td = tr.xpath('td')[1]
				photo_src = 'aaa'
			if i == 11:
				td = tr.xpath('td')[1]
				country_of_origin = td.xpath('text()')[0].extract().strip()

			
		yield CatFoodDetailItem(
				name = name , owner = owner,
			 	source = source , food_type = food_type ,
			 	net_weight = net_weight , capacity = capacity,
			 	additives = additives , analytical_constituents = analytical_constituents ,
			 	feedind_instructions = feedind_instructions , photo_src = photo_src ,
			 	country_of_origin = country_of_origin
			)