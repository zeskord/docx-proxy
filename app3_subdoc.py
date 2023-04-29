# Возвращает поддокумент приложения В.
import base64
from docx.shared import Inches, Mm, Pt
from docx.enum.table import WD_ALIGN_VERTICAL
from docx.enum.text import WD_ALIGN_PARAGRAPH
import io

def picture(run, pic_data):
    max_width = 75
    max_height = 100
    file_base64 = pic_data["ДанныеФайла"]
    image = base64.b64decode(file_base64)
    stream = io.BytesIO(image)
    # par = sd.add_paragraph()
    # Небольшая возня с размерами.
    width = pic_data["Ширина"]
    height = pic_data["Высота"]
    k = width / height # Отношение сторон картинки.
    k2 = max_width / max_height
    if k < k2:
        # Это широкая картинка, ее нужно привести к максимальной ширине
        run.add_picture(stream, width=None, height=Mm(max_height))
    else:
        run.add_picture(stream, width=Mm(max_width), height=None)
    
    # par.alignment = WD_ALIGN_PARAGRAPH.CENTER

def app3_subdoc(data, doc):
    sd = doc.new_subdoc()
    
    picture_group_counter = 0
    for picture_group in data["КартинкиПриложенияВ"]:
        
        picture_group_counter += 1

        table = sd.add_table(rows=0, cols=2)

        counter = 0
        picture_group_length = len(picture_group["ДанныеФайлов"])
        for file_entry in picture_group["ДанныеФайлов"]:
            counter = counter + 1
            is_last_pic = counter == (picture_group_length)
            if counter % 2 != 0:
                row_pictures = table.add_row()
                row_pictures.height = Mm(100)
                row_descriptions = table.add_row()
            else:
                row_pictures = table.rows[len(table.rows) - 2]
                row_descriptions = table.rows[len(table.rows) - 1]

            # Добавляем картинку в файл.
            current_col_id = 1 if counter % 2 == 0 else 0
            cell_pictures = row_pictures.cells[current_col_id]
            # Если это последняя картинка и она нечетная, то нужно объединить последние ячейки.
            if is_last_pic and current_col_id == 0:
                cell_pictures.merge(row_pictures.cells[current_col_id + 1])
                # print(f'is_last_pic row_pictures: {is_last_pic}')
                # a, b = row_pictures.cells[:2]
                # a.merge(b)
            cell_pictures.vertical_alignment = WD_ALIGN_VERTICAL.BOTTOM
            picture_paragraph = cell_pictures.paragraphs[0]
            picture_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
            picture_paragraph.paragraph_format.space_after = Pt(0)
            run = picture_paragraph.add_run()
            if file_entry["ДанныеКартинки"]["ИспользоватьПлейсхолдер"] == False:
                picture(run, file_entry["ДанныеКартинки"])
            # picture = run.add_picture(stream, width=Mm(75), height=None)

            cell_descriptions = row_descriptions.cells[current_col_id]
            if is_last_pic and current_col_id == 0:
                # print(f'is_last_pic row_descriptions: {is_last_pic}')
                # a, b = row_descriptions.cells[:2]
                # a.merge(b)
                cell_descriptions.merge(row_descriptions.cells[current_col_id + 1])
            description = file_entry["Описание"]
            par_description = cell_descriptions.paragraphs[0]
            par_description.alignment = WD_ALIGN_PARAGRAPH.CENTER
            description_run = par_description.add_run(description)
            description_run.font.size = Pt(12)
        
        par = sd.add_paragraph(f'Рисунок {picture_group_counter}: {picture_group["ОписаниеРисунка"]}')
        par.alignment = WD_ALIGN_PARAGRAPH.CENTER
    return sd
