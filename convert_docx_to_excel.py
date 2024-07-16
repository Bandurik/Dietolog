import pandas as pd
from docx import Document

def docx_to_csv(docx_path, csv_path):
    doc = Document(docx_path)
    data = []
    current_day = None
    current_week = None
    meal_types = ["Завтрак", "Перекус", "Обед", "Перекус2", "Ужин"]
    last_meal_type = None

    for para in doc.paragraphs:
        text = para.text.strip()
        if text.startswith("Неделя"):
            current_week = text
        elif text.startswith("День"):
            if current_day:
                data.append(current_day)
            current_day = {"Неделя": current_week, "День": text}
            last_meal_type = None
        elif any(text.startswith(meal) for meal in meal_types):
            meal, description = text.split(':', 1)
            current_day[meal.strip()] = description.strip()
            last_meal_type = meal.strip()
        elif text:
            # Обработка строк без разделителя ":"
            if current_day and last_meal_type:
                if last_meal_type in current_day:
                    current_day[last_meal_type] += f" {text.strip()}"
                else:
                    current_day[last_meal_type] = text.strip()

    if current_day:
        data.append(current_day)

    df = pd.DataFrame(data)
    df.to_csv(csv_path, index=False, encoding='utf-8-sig')

def csv_to_excel(csv_path, excel_path):
    df = pd.read_csv(csv_path)
    df.to_excel(excel_path, index=False)

if __name__ == "__main__":
    docx_path = 'C:/Mytradingapp/меню 5 приемов С 8УТРА.docx'  # путь к вашему docx файлу
    csv_path = 'menu.csv'
    excel_path = 'menu.xlsx'

    docx_to_csv(docx_path, csv_path)
    csv_to_excel(csv_path, excel_path)
