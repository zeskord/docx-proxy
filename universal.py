from docxtpl import DocxTemplate
from docx import Document
import uuid

def universal_template(doc, data, subtemplate_key):
    subdoc_template = Document()
    subdoc_template.add_paragraph(data[subtemplate_key])
    output_file = f'temp/{str(uuid.uuid4())}.docx'
    subdoc_template.save(output_file)
    subdoc = DocxTemplate(output_file)
    subdoc.render(data)
    subdoc.save(output_file)
    final = doc.new_subdoc(output_file)
    return final
