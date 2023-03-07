from docxtpl import DocxTemplate

def question(doc, data, output_file, question_row_data):
    subdoc_template = DocxTemplate(f'templates/{data["ИмяШаблона_ВопросСудьи"]}')
    subdoc_template.render(question_row_data, autoescape=True)
    subdoc_template.save(output_file)
    subdoc = DocxTemplate(output_file)
    subdoc.render(data)
    subdoc.save(output_file)
    final = doc.new_subdoc(output_file)
    return final