import base64
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Inches, Mm, Pt

def app4_subdoc(data, doc, output_file):
    subdoc_template = DocxTemplate(f'templates/{data["ИмяШаблона_ПриложениеГ"]}')
    counter = 0
    for file_entry in data["КартинкиПриложенияГ"]:
        counter = counter + 1

        file_guid = file_entry["ИмяФайла"]
        file_extension = file_entry["Расширение"]
        file_base64 = file_entry["ДанныеФайла"]
        image = base64.b64decode(file_base64)
        filename = f'temp/{file_guid}.{file_extension}'
        with open(filename, "wb") as file:
            file.write(image)
        
        file_entry["Картинка"] = InlineImage(subdoc_template, filename, width=Mm(100)),
        
    subdoc_template.render(data, autoescape=True)
    temp_ourput_file = f'{output_file}_приложениеГ_{counter}.docx'
    subdoc_template.save(temp_ourput_file)
    final = doc.new_subdoc(temp_ourput_file)
    return final