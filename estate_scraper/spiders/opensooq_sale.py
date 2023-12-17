"""
Instructions:
scrapy crawl SPIDER NAME
scrapy crawl opensooq-sale
"""


import scrapy
from scrapy.loader import ItemLoader
from scrapy.exceptions import CloseSpider
from estate_scraper.items import EstateItem


class OpensooqSaleSpider(scrapy.Spider):
    name = "opensooq-sale"
    allowed_domains = ["om.opensooq.com"]
    handle_httpstatus_list = [404, 403]
    page_number = 1
    

    def start_requests(self):
        url = "https://om.opensooq.com/en/real-estate-for-sale/all"
        yield scrapy.Request(
            url,
            meta={
                "playwright": True,
            }
        )


    async def parse(self, response):

        if response.status == 403:
            raise CloseSpider("403 Received: Closing Spider. Change your IP or try again later.")

        if response.status == 404:
            raise CloseSpider("404 Received: Closing Spider.")

        if len(response.css('div.flexSpaceBetween h2.font-20')) == 0:
            raise CloseSpider('No listings received: Closing Spider.')

        sales = response.css("div.sc-cfbb9bd4-3")
        for sale in sales:
            loader = ItemLoader(item=EstateItem(), selector=sale)        
            loader.add_css("description", "div.flexSpaceBetween h2.font-20::text")
            loader.add_css("size", "div.flexSpaceBetween h2.font-20::text", re="\d*m2")

            loader.add_css("bedroom", "div", re="\w*..Bedroom.")
            loader.add_css("bathroom", "div", re="\w*..Bathroom.")
            loader.add_css("building_type", "div div::text",
                           re="(Apartments|Farms & Chalets|Commercial|Townhouses|Villa|Lands|Foreign Real Estate|Whole Building)")

            loader.add_css("area", "div.category span.bold::text")
            loader.add_css("price", "div.alignItems div.postPrice::text")

            yield loader.load_item()

        self.page_number += 1
        next_page = f"https://om.opensooq.com/en/real-estate-for-sale/all?page={[self.page_number]}"
        yield response.follow(next_page, callback=self.parse)
