# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import CrawlSpider , Rule
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request
from bs4 import BeautifulSoup, Comment
from scrapy.conf import settings
import time
from ..items import TechinasiaItem
import re

class TechinasiaSpider(CrawlSpider):
	name = "techinasia"
	allowed_domains = [
		"www.techinasia.com",
	]

	start_urls = [
		'https://www.techinasia.com/category/news/'
	]

	

	__queue = [
		'https://www.techinasia.com/category/[\w\/]+',
		'https://www.techinasia.com/author[\w\/]+'
	]

	rules = [
	    Rule(
			LinkExtractor(allow=(
				), deny=__queue,
			restrict_xpaths=[
			'//section/section/div/div[1]',
			'//section/section/div/div[1]/article//div[@class="post-content"]'
			'//section/section/div/div[1]/article/h1',
			'//section/section/div/div[1]/div[2]'
			]), 
			callback='parse_extract_data_news', follow=True
			),
	    Rule(LinkExtractor(deny_domains=["com","jp"]))
	]

	def extract(self,sel,xpath):
		try:
			text = filter(lambda element: element.strip(), sel.xpath(xpath).extract())
			return ''.join(text)
			# return re.sub(r"\s+", "", ''.join(text).strip(), flags=re.UNICODE)

		except Exception, e:
			raise Exception("Invalid XPath: %s" % e)


	def parse_extract_data_news(self, response):
		item = None
		try:
			item = TechinasiaItem()
			item['content'] = self.extract(response,'//section/section/div/div[1]/article/div[@class="post-content"]//text()')
			item['title'] = self.extract(response,'//section/section/div/div[1]/article/h1//text()')
			item['url'] = response.url
		except Exception, e:
			pass
		if ('content' in item and item['content'] != ''):
			return item
		


