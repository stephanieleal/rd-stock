# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import requests

class SiteAppScraperPipeline(object):
    def process_item(self, item, spider):
        if type(item).__name__ == "WikiBotItem":
            requests.post('http://localhost:8000/include_company/', data=item)
        elif type(item).__name__ == "NewsBotItem":
            requests.post('http://localhost:8000/include_news/', data=item)
	return item
