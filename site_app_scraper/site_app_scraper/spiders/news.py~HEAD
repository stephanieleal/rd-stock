# -*- coding: utf-8 -*-
import scrapy
import requests
import urlparse
import re
import datetime
from site_app_scraper.items import NewsBotItem

class NewsSpider(scrapy.Spider):
    name = "news_spider"
    allowed_domains = ["http://quotes.wsj.com"]
    start_urls = (
        'http://quotes.wsj.com/',
    )

    def parse_news(self, response):
        print "RESPONSE", response.url, len(response.xpath("//ul[contains(@id, 'newsSummary_c')]/li"))
        for news in response.xpath("//ul[contains(@id, 'newsSummary_c')]/li"):
            item = NewsBotItem()
            date_str = news.xpath(".//li[contains(@class, 'cr_dateStamp')]/text()").extract_first().strip()

            if re.match("^\d\d/\d\d/\d\d$", date_str):
                item["date"] = datetime.datetime.strptime(date_str, "%m/%d/%y")
            elif re.search("^\d$", date_str):
                hours = int(re.search("^\d$", date_str).group(0))
                item["date"] = datetime.datetime.now() - datetime.timedelta(hours=hours)
            headline = news.xpath(".//span[contains(@class, 'headline')]/a")
            item["headline_text"] = headline.xpath("./text()").extract_first().strip()
            item["headline_link"] = headline.xpath("./@href").extract_first().strip()
            item["company"] = response.meta["company_id"]
            yield item

        companies = response.meta["companies"]
        if len(companies):
            company = companies.pop();
            meta = {"company_id": company["company_id"], "companies": companies}
            yield scrapy.Request(company["url"], callback = self.parse_news, dont_filter=True, meta=meta)


    def parse(self, response):
        request = requests.get("http://localhost:8000/get_companies_codes")
        codes = request.json()
        companies = []
        for company_id in codes:
            url = urlparse.urljoin(response.url, codes[company_id])
            companies.append({"company_id": company_id, "url": url})

        company = companies.pop();
        meta = {"company_id": company["company_id"], "companies": companies    }
	yield scrapy.Request(company["url"], callback = self.parse_news, dont_filter=True, meta=meta)
