#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
import argparse
import json
from docxtpl import DocxTemplate
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT, WD_TAB_ALIGNMENT, WD_LINE_SPACING
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml import OxmlElement, ns
from docx.shared import Cm, Pt
from app1_subdoc import app1_subdoc
from app2_subdoc import picture_subdoc
from app3_subdoc import app3_subdoc
from app4_subdoc import app4_subdoc
from questions import questions
from question import question
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
    data["ПриложениеА"] = app1_subdoc(data, doc, jsondata)
    data["АктПрисутствияЗаинтересованныхСторон"] = picture_subdoc(doc, data["АктПрисутствияЗаинтересованныхСторон"], 160, 200)
    
    НомераЛистовДоверености = ["1", "2", "3", "4"]
    for НомерЛиста in НомераЛистовДоверености:
        if data[f"ДоверенностьПредставителяЗастройщика{НомерЛиста}_Используется"]:
            data[f"ДоверенностьПредставителяЗастройщика{НомерЛиста}"] = picture_subdoc(doc, data[f"ДоверенностьПредставителяЗастройщика{НомерЛиста}"], 160, 200)
    
    data["ПриложениеВ"] = app3_subdoc(data, doc)

    data["ПриложениеГ"] = app4_subdoc(data, doc, jsondata)
    data["ОбмерныйПлан"] = picture_subdoc(doc, data["ОбмерныйПлан"], 160, 200)
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

