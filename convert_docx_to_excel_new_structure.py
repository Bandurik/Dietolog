import pandas as pd
from docx import Document

def docx_to_csv_new_structure(docx_path, csv_path):
    doc = Document(docx_path)
    data = []
    current_week = None
    current_day = None
    meal_types = ["Завтрак", "Перекус", "Обед", "Перекус2", "Ужин"]
    week_data = []

    for para in doc.paragraphs:
        text = para.text.strip()
        if text.startswith("Неделя"):
            if week_data:
                data.append(week_data)
            current_week = text
            week_data = [current_week]
        elif text.startswith("День"):
            if current_day:
                week_data.append(current_day)
            current_day = text + ":\n"
        elif any(text.startswith(meal) for meal in meal_types):
            meal, description = text.split(':', 1)
            current_day += f"{meal.strip()}: {description.strip()}\n"
        elif text:
            if current_day:
                current_day += f"{text.strip()}\n"

    if current_day:
        week_data.append(current_day)
    if week_data:
        data.append(week_data)

    df = pd.DataFrame(data)
    df.to_csv(csv_path, index=False, encoding='utf-8-sig')

def csv_to_excel(csv_path, excel_path):
    df = pd.read_csv(csv_path)
    df.to_excel(excel_path, index=False)

if __name__ == "__main__":
    docx_path = 'C:/Mytradingapp/меню 5 приемов С 8УТРА.docx'  # путь к вашему docx файлу
    csv_path = 'menu_new_structure.csv'
    excel_path = 'menu_new_structure.xlsx'

    docx_to_csv_new_structure(docx_path, csv_path)
    csv_to_excel(csv_path, excel_path)
