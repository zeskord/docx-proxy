
from docxtpl import DocxTemplate

def questions(doc, data, output_file):
    subdoc_template = DocxTemplate()
    for question_data in data["ВопросыСудьи"]:
        par = subdoc_template.add_paragraph(f'Вопрос {question_data["Номер"]}: {question_data["Текст"]}')
    subdoc_template.save(output_file)
    subdoc = DocxTemplate(output_file)
    subdoc.render(data)
    return subdoc
