# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from oauth2client.service_account import ServiceAccountCredentials
import gspread
import os
import json


class VacinometroPipeline:
    def process_item(self, item, spider):
        return item


class SyncVaccinesDataToGoogleSheetsPipeline:
    def __init__(self, *args, **kwargs):
        scope = [
            "https://www.googleapis.com/auth/drive",
            "https://spreadsheets.google.com/feeds"
        ]
        key_file_dict = json.loads(os.getenv("GOOGLE_CREDENTIALS"))
        credentials = ServiceAccountCredentials.from_json_keyfile_dict(key_file_dict, scope)

        gc = gspread.authorize(credentials)
        self.worksheet = gc.open_by_key(os.getenv("GOOGLE_SHEET_ID")).sheet1

        super().__init__(*args, **kwargs)

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        last_vaccinated_date = adapter.get('data')
        total = adapter.get('total')
        total_vaccinated = adapter.get('total_de_vacinados')
        total_vaccinated_today = adapter.get('total_de_vacinados_hoje')
        vaccines = adapter.get('vacinas')
        self.update_sheet_headers(vaccines)
        row = [last_vaccinated_date, total, total_vaccinated, total_vaccinated_today]
        row.extend([value for vaccine in vaccines for value in vaccine.values()])
        self.worksheet.append_row(row)

    def update_sheet_headers(self, vaccines):
        self.worksheet.update_cell(1, 1, 'Data')
        self.worksheet.update_cell(1, 2, 'Total de Vacinas')
        self.worksheet.update_cell(1, 3, 'Total de Vacinados')
        self.worksheet.update_cell(1, 4, 'Total de Vacinados no Dia')
        offset = 1
        for vaccine in vaccines:
            vaccine_name = list(vaccine.keys())[0]
            vaccine_name = vaccine_name.split("_")
            vaccine_name = " ".join(list(map(lambda text: text.title(), vaccine_name)))
            self.worksheet.update_cell(1, 4 + offset, vaccine_name)
            offset += 1
