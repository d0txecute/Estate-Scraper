"""
Instructions:
scrapy crawl SPIDER NAME -O data/DATA-NAME.EXT
scrapy crawl opensooq-rent -O data/rent-data.json
"""


import scrapy
from scrapy.loader import ItemLoader
from scrapy.exceptions import CloseSpider
from estate_scraper.items import EstateItem


class OpensooqRentSpider(scrapy.Spider):
    name = "opensooq-rent"
    allowed_domains = ["om.opensooq.com"]
    handle_httpstatus_list = [404, 403]
    page_number = 1
    

    def start_requests(self):
        url = "https://om.opensooq.com/en/real-estate-for-rent/all"
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
        
        rents = response.css("div#listing_posts")
        for rent in rents:
            loader = ItemLoader(item=EstateItem(), selector=rent)        
            loader.add_css("description", "div.flexSpaceBetween h2.font-20::text")
            loader.add_css("size", "div.flexSpaceBetween h2.font-20::text", re="\d*m2")
            
            loader.add_css("bedroom", "div.flexNoWrap div::text", re="\w*..Bedroom.")
            loader.add_css("bathroom", "div.flexNoWrap div::text", re="\w*..Bathroom.")
            loader.add_css("furnishing", "div.flexNoWrap div::text", re="(Furnished|Unfurnished|Semi Furnished)")
            loader.add_css(
                "building_type", "div.flexNoWrap div::text", 
                re="(Apartments|Shared Rooms|Farms & Chalets|Commercial|Townhouses|Villa|Lands|Hotel Apartments)"
            )
    
            loader.add_css("area", "div.category span.bold::text")
            loader.add_css("price", "div.alignItems div.postPrice::text")

            yield loader.load_item()
            
        self.page_number += 1
        next_page = f"https://om.opensooq.com/en/real-estate-for-rent/all?page={[self.page_number]}"
        yield response.follow(next_page, callback=self.parse)    
        