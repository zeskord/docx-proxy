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
from my_subdoc import my_subdoc

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

    print(arguments.inputfile)
    print(arguments.data)
    print(arguments.otputfile)

    # Чтение документа-исходника.
    # doc = docx.Document(arguments.inputfile)
    doc = DocxTemplate(arguments.inputfile)

    # Чтение входящих параметров.
    # data = json.load(open(arguments.data, encoding='utf-8'))
    data = json.load(open(arguments.data, encoding='utf-8-sig'))

    if data["ИмяШаблона_ВопросыСудьи"] != "":
        output_file = f'{arguments.otputfile}1'
        data["Поддокумент_ВопросыСудьи"] = my_subdoc(doc, f'templates/{data["ИмяШаблона_ВопросыСудьи"]}', data, output_file)

    doc.render(data)
    
    # Сохраним документ.
    doc.save(arguments.otputfile)

