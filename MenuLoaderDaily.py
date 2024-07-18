import pandas as pd

class MenuLoaderDaily:
    def __init__(self, file_path):
        self.menu_data = pd.read_excel(file_path)

    def get_menu_for_day(self, day):
        try:
            menu_for_day = self.menu_data[self.menu_data['День'] == day].iloc[0].to_dict()
            return menu_for_day
        except IndexError:
            return {}
