from docxtpl import DocxTemplate
from docx import Document
import uuid

def universal_template(doc, data, subtemplate_key):
    # subdoc_template = DocxTemplate(f'templates/Универсальный.docx')
    subdoc_template = Document()
    subdoc_template.add_paragraph(data[subtemplate_key])
    # mid = {"ЗаготовкаШаблона", data[subtemplate_key]}
    # mid = {"ЗаготовкаШаблона", "Тест"}
    # subdoc_template.render(mid, autoescape=True) # Отрендерели промежуточный шаблон.
    output_file = f'temp/{str(uuid.uuid4())}.docx'
    subdoc_template.save(output_file)
    subdoc = DocxTemplate(output_file)
    subdoc.render(data)
    subdoc.save(output_file)
    final = doc.new_subdoc(output_file)
    return final
