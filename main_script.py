#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
import argparse
import json
from docxtpl import DocxTemplate
import lib
from app3_subdoc import app3_subdoc
from volumes import volumes
from universal import universal_template

# Инициализация входных параметров.
def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('inputfile', type=str)
    parser.add_argument('data', type=str)
    parser.add_argument('otputfile', type=str)
    return parser

def createDoc(inputfile, jsondata, otputfile):
    # Чтение документа-исходника.
    doc = DocxTemplate(inputfile)

    # Чтение входящих параметров.
    data = json.load(open(jsondata, encoding='utf-8-sig'))

    НомераВопросов = ["1", "2", "3", "4"]
    for НомерВопроса in НомераВопросов:
        if data[f'Вопрос{НомерВопроса}_Заполнен']:
            data[f'Вопрос{НомерВопроса}'] = universal_template(doc, data, f'Вопрос{НомерВопроса}_Шаблон')
            data[f'ОтветНаВопрос{НомерВопроса}'] = universal_template(doc, data, f'ОтветНаВопрос{НомерВопроса}_Шаблон')

    data["ВедомостьВидовИОбъемовРабот"] =  volumes(data, doc)

    data["ПриложениеА"] = lib.tiled_pictures_subdoc(data["КартинкиПриложенияА"], doc)
    data["АктПрисутствияЗаинтересованныхСторон"] = lib.picture_subdoc(doc, data["АктПрисутствияЗаинтересованныхСторон"], 160, 200)
    
    НомераЛистовДоверености = ["1", "2", "3", "4"]
    for НомерЛиста in НомераЛистовДоверености:
        if data[f"ДоверенностьПредставителяЗастройщика{НомерЛиста}_Используется"]:
            data[f"ДоверенностьПредставителяЗастройщика{НомерЛиста}"] = lib.picture_subdoc(doc, data[f"ДоверенностьПредставителяЗастройщика{НомерЛиста}"], 160, 200)
    
    data["ПриложениеВ"] = app3_subdoc(data, doc)

    data["ПриложениеГ"] = lib.tiled_pictures_subdoc(data["КартинкиПриложенияГ"], doc)
    data["ОбмерныйПлан"] = lib.picture_subdoc(doc, data["ОбмерныйПлан"], 160, 200)
    doc.render(data)
    
    # Сохраним документ.
    doc.save(otputfile)

# Основное действие.
if __name__ == '__main__':
    
    # Парсер параметров.
    parser = createParser()
    arguments = parser.parse_args(sys.argv[1:])

    # Главная процедура.
    createDoc(arguments.inputfile, arguments.data, arguments.otputfile)

