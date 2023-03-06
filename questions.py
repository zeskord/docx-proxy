
from docxtpl import DocxTemplate

def questions(doc, data, output_file):
    subdoc_template = DocxTemplate(f'templates/{data["ИмяШаблона_ВопросыСудьи"]}')
    subdoc_template.render(data, autoescape=True)
    # for question_data in data["ВопросыСудьи"]:
    #     par = subdoc_template.add_paragraph(f'Вопрос {question_data["Номер"]}: {question_data["Текст"]}')
    subdoc_template.save(output_file)
    subdoc = DocxTemplate(output_file)
    subdoc.render(data)
    subdoc.save(output_file)
    final = doc.new_subdoc(output_file)
    return final
