# -*- coding: utf-8 -*-

import re


description = "45 ألف ريال سعودي 4 غرف نوم 1 مطبخ 4 دورات مياة 1 صالة عرض الشارع 20 متر undefined درج صالة بيت شعر حوش ملحق مدخل سيارة جنوب المساحة 300 متر مربع الأن مع عروض شركة عبر التواصل العقاريه فيلا درج داخلي للايجار تشطيب راقي جدا بالرمال موقع ممتاز قريب من جميع الخدمات السعر ٤٥٠٠٠الف ريال قابل للتفاوض للتواصل :احمد الشومي ٠٥٣٥٤٤٨٤٨٤"

price_texts = ['‫الف‬', '‫ألف‬', '‫مليون‬', '‫مليون‬']
age_texts = ['‫جديد‬', '‫جديدة‬', '‫سنتان‬', '‫سنتين‬', '‫سنين‬', '‫سنوات‬']
area_texts = ['‫م‬', '‫متر‬', '2 ‫م‬', '‫المساحة‬']
room_texts = ['‫غرف‬', '‫الغرف‬ ‫عدد‬', '‫غرفتين‬', '‫غرفتان‬']

splited_description = re.split(' ', description)

des_length = len(splited_description)

numbers = [int(s) for s in splited_description if s.isdigit()]

# print(numbers[0])

result = {}

for num in numbers:
    try:
        indexOfNumber = splited_description.index(str(num))

        if (indexOfNumber+1 == des_length):
            checkNextIndex = indexOfNumber - 1
        else:
            checkNextIndex = indexOfNumber + 1

        checkText = splited_description[checkNextIndex]

        # check the output, encoding problem
        # second output is False instead of being True
        print(room_texts[0], checkText, room_texts[0] == checkText)

        if checkText in price_texts:
            result['price'] = (str(num) + " " + checkText)
            del splited_description[indexOfNumber]
            continue

        if checkText in age_texts:
            result['age'] = (str(num) + " " + checkText)
            del splited_description[indexOfNumber]
            continue

        if checkText in area_texts:
            result['area'] = (str(num) + " " + checkText)
            del splited_description[indexOfNumber]
            continue

        if checkText in room_texts:
            result['room'] = (str(num) + " " + checkText)
            del splited_description[indexOfNumber]
            continue


    except:
        continue


print(result)

