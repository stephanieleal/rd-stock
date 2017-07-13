# -*- coding: utf-8 -*-
import scrapy
import wikipedia
import json
import requests
from site_app_scraper.items import WikiBotItem

class WikiSpider(scrapy.Spider):
    name = "wiki_spider"
    allowed_domains = ["https://en.wikipedia.org"]
    start_urls = (
        'https://en.wikipedia.org/wiki/',
    )

    def parse_en(self, response):
        item = WikiBotItem()
        infobox = response.xpath("//table[contains(@class, 'infobox')]")
        item["name"] = infobox.xpath("./caption/text()").extract_first().strip()

        logo = infobox.xpath("./tr/td/a[contains(@class, 'image')]/img/@src")
        if not logo:
            logo = "https://pbs.twimg.com/media/CdlFCYmXIAAGkiH.jpg"
        else:
            logo = logo.extract_first().strip()

        item["logo"] = logo

        item["nasdaq"] = infobox.xpath(".//a[contains(@href, 'http://www.nasdaq.com/symbol/')]/text()").extract_first().strip()
        item["wikipedia"] = {"link": response.url, "summary": wikipedia.summary(item["name"], sentences=2), "infobox": {}}
        for tr in response.xpath("//table[contains(@class, 'infobox')]/tr"):
            subsidiary = tr.xpath("./th/a[contains(@title, 'Subsidiary')]")
            key_people = tr.xpath("./th/div/text()")

            if key_people and key_people.extract_first() == "Key people":
                table_head = "Key people"
            elif subsidiary:
                table_head = subsidiary.xpath("./text()").extract_first();
            else:
                table_head = tr.xpath("./th/text()").extract_first();

            table_content = tr.xpath("./td").extract_first()
            if table_head == "Founded" or table_head == "Headquarters" or table_head == "Founders" or table_head == "Key people" or table_head == "Subsidiaries" or table_head == "Owner":
                item["wikipedia"]["infobox"][table_head] = table_content.replace("/wiki/", "https://en.wikipedia.org/wiki/")

        item["wikipedia"] = json.dumps(item["wikipedia"])
        yield item

    def parse(self, response):
        request = requests.get("http://localhost:8000/get_companies_wikis")
        urls = request.json()
        for url in urls:
	    yield scrapy.Request(url, callback = self.parse_en, dont_filter=True)
