
from docxtpl import DocxTemplate

def questions(doc, data):
    sd = doc.new_subdoc()
    for question_data in data["ВопросыСудьи"]:
        par = sd.add_paragraph(f'Вопрос {question_data["Номер"]}: {question_data["Текст"]}')
    sd.render(data)
    return sd

    
