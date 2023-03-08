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
from app3_subdoc import app3_subdoc
from app4_subdoc import app4_subdoc
from questions import questions
from question import question

# Инициализация входных параметров.
def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('inputfile', type=str)
    parser.add_argument('data', type=str)
    parser.add_argument('otputfile', type=str)
    return parser

# Основное действие.
if __name__ == '__main__':
    
    # Парсер параметров.
    parser = createParser()
    arguments = parser.parse_args(sys.argv[1:])

    # Чтение документа-исходника.
    doc = DocxTemplate(arguments.inputfile)

    # Чтение входящих параметров.
    data = json.load(open(arguments.data, encoding='utf-8-sig'))

    if data["ИмяШаблона_ВопросыСудьи"] != "":
        output_file = f'{arguments.otputfile}_вопросы'
        data["Поддокумент_ВопросыСудьи"] = questions(doc, data, output_file)

        data["Вопросы"] = []
        for question_row_data in data["ВопросыСудьи"]:
            output_file = f'{arguments.otputfile}_вопрос{len(data["Вопросы"])}'
            # data[f'Вопрос{counter}'] = question(doc, data, output_file, question_row_data)
            data["Вопросы"].append(question(doc, data, output_file, question_row_data))

    data["ПриложениеВ"] = app3_subdoc(data, doc)

    app4_subdoc(data, doc)

    doc.render(data)
    
    # Сохраним документ.
    doc.save(arguments.otputfile)

