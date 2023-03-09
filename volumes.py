
import json
from docx.shared import Inches, Mm, Pt
from docx.enum.table import WD_ALIGN_VERTICAL
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx import Document
from docxtpl import DocxTemplate

def volumes(data, doc):
    sd = doc.new_subdoc()
    return generate_table(data, sd)

def generate_table(data, doc):

    table = doc.add_table(rows=0, cols=4)
    table.style = "Table Grid"
    table.columns[0].width = Mm(15)
    table.columns[1].width = Mm(110)
    table.columns[2].width = Mm(20)
    table.columns[3].width = Mm(20)

    row_header = table.add_row()

    row_header.cells[0].paragraphs[0].add_run("№ п/п")
    row_header.cells[1].paragraphs[0].add_run("Наименование")
    row_header.cells[2].paragraphs[0].add_run("Ед.изм.")
    row_header.cells[3].paragraphs[0].add_run("Кол.")

    for item in data["ВедомостьВидовИОбъемовРабот"]:
        # subdoc = doc.new_subdoc()
        row = table.add_row()
        par = row.cells[0].paragraphs[0]
        run = par.add_run(item["Номер"])
        par.alignment = WD_ALIGN_PARAGRAPH.CENTER
        if item["Наименование"] == "":
            run.bold = True
            row.cells[0].merge(row.cells[3])
        else:
            row.cells[1].paragraphs[0].add_run(item["Наименование"])
            row.cells[1].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            row.cells[2].paragraphs[0].add_run(item["ЕдИзм"])
            row.cells[2].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            row.cells[3].paragraphs[0].add_run(item["Количество"])
            row.cells[3].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    return doc

if __name__ == '__main__':
    my_list = json.load(open("tests/volumes.json", encoding='utf-8-sig'))
    data = {"ВедомостьВидовИОбъемовРабот": my_list}
    doc = Document()
    generate_table(data, doc)
    doc.save("temp/volumes.docx")  
