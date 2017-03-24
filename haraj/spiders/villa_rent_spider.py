# -*- coding: utf-8 -*-

import scrapy, pdb
from haraj.items import RentVilla
from haraj.config import SITE_URL_VILLA_RENT, SITE_URL_VILLA_SALE, SITE_URL_APARTMENT_RENT, SITE_URL_APARTMENT_SALE
from haraj.config import SITE_URL_STORE_RENT, SITE_URL_STORE_SALE, SITE_URL_LAND_SALE
from scrapy.selector import HtmlXPathSelector


class VillaRentSpider(scrapy.Spider):
    name = "rent_villa"

    start_urls = [SITE_URL_VILLA_RENT, SITE_URL_VILLA_SALE, SITE_URL_APARTMENT_RENT, SITE_URL_APARTMENT_SALE,
                  SITE_URL_STORE_RENT, SITE_URL_STORE_SALE, SITE_URL_LAND_SALE]

    def parse(self, response):

        ''' Grab all author list and browse pagination '''

        # hxs = HtmlXPathSelector(response)

        # file_path = 'data/villas.json'
        #
        # # if os.path.exists(file_path):
        #
        # with open(file_path, encoding='utf-8') as data_file:
        #     try:
        #         categories = json.loads(data_file.read())
        #
        #         for data in categories:
        #             start_urls.append(data['url'])
        #     except:
        #         pass

        # ads = hxs.select("//div[@class='adsx']/div[@class='adx']")
        ads = response.css('div.adsx div.adx')

        for ad in ads:
            ad_obj = RentVilla()
            ad_obj['url'] = ad.css("div.adxTitle a::attr(href)").extract_first()
            # print(ad_obj['url'])
            yield ad_obj

        # next_page = response.xpath("//div[@class='pagination']//a[position() = (last())]/@href").extract_first()
        # if next_page is not None:
        #     next_page = response.urljoin(next_page)
        #     yield scrapy.Request(next_page, callback=self.parse)
