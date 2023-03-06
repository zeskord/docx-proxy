
from docxtpl import DocxTemplate

def questions(doc, data, output_file):
    sd = doc.new_subdoc()
    for question_data in data["ВопросыСудьи"]:
        par = sd.add_paragraph(f'Вопрос {question_data["Номер"]}: {question_data["Текст"]}')
    sd.save(output_file)
    subdoc = DocxTemplate(output_file)
    subdoc.render(data)
    return subdoc
