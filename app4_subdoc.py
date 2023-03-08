import base64
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Inches, Mm, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

def app4_subdoc(data, doc, output_file):
    subdoc_template = DocxTemplate(f'templates/{data["ИмяШаблона_ПриложениеГ"]}')
    for file_entry in data["КартинкиПриложенияГ"]:
        file_guid = file_entry["ИмяФайла"]
        file_extension = file_entry["Расширение"]
        file_base64 = file_entry["ДанныеФайла"]
        image = base64.b64decode(file_base64)
        filename = f'temp/{file_guid}.{file_extension}'
        with open(filename, "wb") as file:
            file.write(image)

        sd = subdoc_template.new_subdoc()
        par = sd.add_paragraph()
        par.add_run().add_picture(filename, width=None, height=Mm(200))
        par.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        file_entry["Картинка"] = sd

    subdoc_template.render(data)
    temp_output_file = f'{output_file}_приложениеГ.docx'
    subdoc_template.save(temp_output_file)
    final = doc.new_subdoc(temp_output_file)
    return final