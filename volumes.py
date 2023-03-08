
import json
from docx.shared import Inches, Mm, Pt
from docx.enum.table import WD_ALIGN_VERTICAL
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx import Document
from docxtpl import DocxTemplate

def generate_table(data, doc):

    table = doc.add_table(rows=0, cols=4)
    for item in data["volumes"]:
        # subdoc = doc.new_subdoc()
        row_pictures = table.add_row()
        row_pictures.cells[0].paragraphs[0].add_run(item["Номер"])
        row_pictures.cells[1].paragraphs[0].add_run(item["Наименование"])
        row_pictures.cells[2].paragraphs[0].add_run(item["ЕдИзм"])
        row_pictures.cells[3].paragraphs[0].add_run(item["Количество"]) 
    doc.save("temp/volumes.docx")    

if __name__ == '__main__':
    my_list = json.load(open("tests/volumes.json", encoding='utf-8-sig'))
    data = {"volumes": my_list}
    doc = Document()
    generate_table(data, doc)
