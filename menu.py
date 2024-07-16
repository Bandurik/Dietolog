import pandas as pd
from config import MENU_XLSX_PATH_NEW_STRUCTURE

class MenuLoaderNewStructure:
    def __init__(self):
        self.menu = self.load_menu()
        print(f"Loaded menu: {self.menu}")  # Отладочное сообщение

    def load_menu(self):
        df = pd.read_excel(MENU_XLSX_PATH_NEW_STRUCTURE)
        menu = {}
        for index, row in df.iterrows():
            week = row[0]
            days = row[1:]
            menu[week] = days.to_list()
        return menu

    def get_menu_for_week(self, week):
        print(f"Requesting menu for {week}")  # Отладочное сообщение
        if week in self.menu:
            return self.menu[week]
        return "Меню не найдено."
