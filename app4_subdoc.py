import base64
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Inches, Mm, Pt

def app4_subdoc(data, doc):
    # sd = doc.new_subdoc()

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
        
        file_entry["Картинка"] = InlineImage(doc, filename, width=Mm(100)),
        
