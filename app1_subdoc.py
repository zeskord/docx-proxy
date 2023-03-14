import base64
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Inches, Mm, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from app2_subdoc import picture_subdoc

def app1_subdoc(data, doc, output_file):
    subdoc_template = DocxTemplate(f'templates/{data["ИмяШаблона_ПриложениеА"]}')
    for file_entry in data["КартинкиПриложенияА"]:
        file_entry["Картинка"] = picture_subdoc(subdoc_template, file_entry, 160, 200)

    subdoc_template.render(data)
    temp_output_file = f'{output_file}_приложениеА.docx'
    subdoc_template.save(temp_output_file)
    final = doc.new_subdoc(temp_output_file)
    return final