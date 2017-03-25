# -*- coding: utf-8 -*-

import scrapy, json, pdb
from haraj.items import RentVilla
from scrapy.selector import HtmlXPathSelector
import re
import arabic_reshaper
from bidi.algorithm import get_display


class VillaDetailSpider(scrapy.Spider):
    name = "villa_details"
    start_urls = []

    with open('data/rent_villas.json', encoding='utf-8') as data_file:
        authors = json.loads(data_file.read())

        for data in authors:
            start_urls.append(data['url'])

    def reshape_arabic(self, arabic_string):
        reshaped_text = arabic_reshaper.reshape(arabic_string)
        return get_display(reshaped_text)

    def parse(self, response):
        hxs = HtmlXPathSelector(response)

        villa = RentVilla()

        # not working
        # villa['created_at'] = response.css('.adxExtraInfoPart:first-child > a::text').extract_first()
        # villa['created_at'] = response.css('div.adxViewContainer div.adxHeader h3:nth-child(2) div.adxExtraInfo div.adxExtraInfoPart:nth-child(1)::text').extract_first()



        # working
        id = (hxs.select("//div[@class='adxViewContainer']//div[@class='adxHeader']//div[@class='adxExtraInfo']//div[@class='adxExtraInfoPart'][position() = (last())]/a/text()").extract_first()).strip()
        title = (response.css('div.adxViewContainer div.adxHeader h3::text').extract_first()).strip()
        created_at = (hxs.select("//div[@class='adxViewContainer']//div[@class='adxHeader']//div[@class='adxExtraInfo'][position() = (last())]//div[position() = (last() - 1)]/text()").extract_first()).strip()
        description = (response.css('div.adxViewContainer div.adxBody::text').extract_first()).strip()
        picture_url = hxs.select("//div[@class='adxViewContainer']//div[@class='adxBody']//img/@src").extract_first()
        address = (response.css('div.metaBody a:nth-child(1)::text').extract_first()).strip()

        villa['id'] = self.reshape_arabic(id)
        villa['title'] = ((self.reshape_arabic(title)).replace("«", "")).strip()
        villa['created_at'] = self.reshape_arabic(created_at)
        villa['description'] = description
        villa['description'] = re.sub('\s+',' ', self.reshape_arabic(villa['description']))
        villa['picture_url'] = self.reshape_arabic(picture_url)

        self.getCityDis(villa, self.reshape_arabic(address))

        villa['phone'] = self.reshape_arabic(response.css('div.adxViewContainer div.adxBody div.contact strong a::text').extract_first())
        villa['url'] = self.reshape_arabic(response.request.url)
        pdb.set_trace()
        # print villa
        yield villa

    def getCityDis(self, villa, address):
        address_titles = [self.reshape_arabic('في'), 'حي']
        addr = re.split(' ', address)
        addr = addr[1:]

        villa['city'] = self.reshape_arabic(" ".join(addr[addr.index(address_titles[0])+1:]))
        villa['district'] = self.reshape_arabic(" ".join(addr[1:addr.index(address_titles[0])]))


    def calculate_regex(self, description):
        price_texts = ['‫الف‬' , '‫ألف‬' , '‫مليون‬',  '‫مليون‬']
        age_texts = ['‫جديد‬', '‫جديدة‬', '‫سنتان‬', '‫سنتين‬', '‫سنين‬', '‫سنوات‬']
        area_texts = ['‫م‬', '‫متر‬', '2 ‫م‬', '‫المساحة‬']
        room_texts = ['‫غرف‬', '‫الغرف‬ ‫عدد‬', '‫غرفتين‬', '‫غرفتان‬']

        splited_description = re.split(' ', description)

        numbers = [int(s) for s in splited_description if s.isdigit()]
        for number in numbers:
            indexOfNumber = splited_description.index(str(number))


