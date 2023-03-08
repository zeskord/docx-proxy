import base64
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Inches, Mm, Pt
import jinja2

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


    jinja_env = jinja2.Environment(autoescape=True)

    subdoc_template.render(data, jinja_env)
    temp_output_file = f'{output_file}_приложениеГ.docx'
    subdoc_template.save(temp_output_file)
    final = doc.new_subdoc(temp_output_file)
    return final