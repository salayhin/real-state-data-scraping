# -*- coding: utf-8 -*-

import scrapy, json, pdb
from haraj.items import RentVilla
from scrapy.selector import HtmlXPathSelector
import re


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
        villa['city'] = response.css('div.adxViewContainer div.adxHeader div.adxExtraInfo:nth-child(1) div.adxExtraInfoPart:nth-child(1) a::text').extract_first()
        villa['description'] = response.css('div.adxViewContainer div.adxBody p:nth-child(1)::text').extract_first()
        villa['description'] = villa['description'] + " " + response.css('div.adxViewContainer div.adxBody p:nth-child(2)::text').extract_first()
        # villa['short_description'] = hxs.select("//section[@id='bookAuthor']//div[@class='container-fluid authorHeader']//div[@class='authDes']//p[@class='des']/text()").extract_first()
        # villa['image_urls'] = SITE_URL + hxs.select("//section[@id='bookAuthor']//img[@class='authImg']/@src").extract_first()
        # print villa
        yield villa

    def calculate_regex(self, description):
        price_texts = ['‫الف‬' , '‫ألف‬' , '‫مليون‬',  '‫مليون‬']
        age_texts = ['‫جديد‬', '‫جديدة‬', '‫سنتان‬', '‫سنتين‬', '‫سنين‬', '‫سنوات‬']
        area_texts = ['‫م‬', '‫متر‬', '2 ‫م‬', '‫المساحة‬']
        room_texts = ['‫غرف‬', '‫الغرف‬ ‫عدد‬', '‫غرفتين‬', '‫غرفتان‬']

        splited_description = re.split(' ', description)

        numbers = [int(s) for s in splited_description if s.isdigit()]
        for number in numbers:
            indexOfNumber = splited_description.index(str(number))


