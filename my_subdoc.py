from docxtpl import DocxTemplate

def my_subdoc(doc_tenplate, subdoc_template_file, data):
    subdoc = doc_tenplate.new_subdoc(subdoc_template_file)
    subdoc.render(data)
    return subdoc
