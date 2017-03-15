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

        # not working
        # villa['created_at'] = response.css('.adxExtraInfoPart:first-child > a::text').extract_first()
        # villa['id'] = response.css('div.adxViewContainer div.adxHeader h3:nth-child(2) div.adxExtraInfo div.adxExtraInfoPart:nth-child(2)::text').extract_first()
        # villa['created_at'] = response.css('div.adxViewContainer div.adxHeader h3:nth-child(2) div.adxExtraInfo div.adxExtraInfoPart:nth-child(1)::text').extract_first()
        # villa['picture_url'] = response.css('div.adxViewContainer div.adxBody img.first-child::attr(src)').extract_first()

        # working
        villa['title'] = response.css('div.adxViewContainer div.adxHeader h3::text').extract_first()
        villa['description'] = response.css('div.adxViewContainer div.adxBody::text').extract_first()
        villa['description'] = re.sub('\s+',' ',villa['description'])
        villa['phone'] = response.css('div.adxViewContainer div.adxBody div.contact strong a::text').extract_first()
        address = response.css('div.metaBody a:nth-child(1)::text').extract_first()
        self.getCityDis(villa, address)

        # print villa
        yield villa

    def getCityDis(self, villa, address):
        address_titles = ['في', 'حي']
        addr = re.split(' ', address)
        addr = addr[1:]

        villa['city'] = " ".join(addr[addr.index(address_titles[0])+1:])
        villa['district'] = " ".join(addr[1:addr.index(address_titles[0])])


    def calculate_regex(self, description):
        price_texts = ['‫الف‬' , '‫ألف‬' , '‫مليون‬',  '‫مليون‬']
        age_texts = ['‫جديد‬', '‫جديدة‬', '‫سنتان‬', '‫سنتين‬', '‫سنين‬', '‫سنوات‬']
        area_texts = ['‫م‬', '‫متر‬', '2 ‫م‬', '‫المساحة‬']
        room_texts = ['‫غرف‬', '‫الغرف‬ ‫عدد‬', '‫غرفتين‬', '‫غرفتان‬']

        splited_description = re.split(' ', description)

        numbers = [int(s) for s in splited_description if s.isdigit()]
        for number in numbers:
            indexOfNumber = splited_description.index(str(number))


