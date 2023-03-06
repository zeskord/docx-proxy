from docxtpl import DocxTemplate

def my_subdoc(doc_tenplate, subdoc_template_file, data, output_file):
    doc_tenplate = DocxTemplate(subdoc_template_file)
    doc_tenplate.render(data)
    doc_tenplate.save(output_file)
    subdoc = doc_tenplate.new_subdoc(output_file)
    return subdoc
