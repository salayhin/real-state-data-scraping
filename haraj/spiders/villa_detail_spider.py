# -*- coding: utf-8 -*-

import scrapy, json, pdb
from haraj.items import RentVilla
from scrapy.selector import HtmlXPathSelector
import io

class VillaDetailSpider(scrapy.Spider):
    name = "villa_details"
    start_urls = []

    with open('data/rent_villas.json', encoding='utf-8') as data_file:
        authors = json.loads(data_file.read())

        for data in authors:
            start_urls.append(data['url'])

    def parse(self, response):
        hxs = HtmlXPathSelector(response)

        villa = RentVilla()
        villa['title'] = response.css('div.adxViewContainer div.adxHeader h3::text').extract_first()
        villa['city'] = response.css('div.adxViewContainer div.adxHeader div.adxExtraInfo:nth-child(1) div.adxExtraInfoPart:nth-child(1) a::attr(href)').extract_first()
        # villa['short_description'] = hxs.select("//section[@id='bookAuthor']//div[@class='container-fluid authorHeader']//div[@class='authDes']//p[@class='des']/text()").extract_first()
        # villa['image_urls'] = SITE_URL + hxs.select("//section[@id='bookAuthor']//img[@class='authImg']/@src").extract_first()
        # print villa
        yield villa
