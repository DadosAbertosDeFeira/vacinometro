from itemadapter import ItemAdapter
from oauth2client.service_account import ServiceAccountCredentials
import gspread
import os
import json
from datetime import datetime, timedelta, timezone


class FakeWorksheet:
    def update_cell(self, *args):
        print(f"[FakeWorksheet] update_cell: {args}")

    def append_row(self, *args):
        print(f"[FakeWorksheet] append_row: {args}")


class SyncVaccinesDataToGoogleSheetsPipeline:
    def __init__(self, *args, **kwargs):
        scope = [
            "https://www.googleapis.com/auth/drive",
            "https://spreadsheets.google.com/feeds",
        ]
        json_credentials = os.getenv("GOOGLE_CREDENTIALS")
        if json_credentials:
            key_file_dict = json.loads(json_credentials)
            credentials = ServiceAccountCredentials.from_json_keyfile_dict(
                key_file_dict, scope
            )
            gc = gspread.authorize(credentials)
            self.worksheet = gc.open_by_key(os.getenv("GOOGLE_SHEET_ID")).sheet1
        else:
            self.worksheet = FakeWorksheet()  # ambiente de testes

        super().__init__(*args, **kwargs)

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        crawl_datetime = (
            datetime.utcnow()
            .replace(tzinfo=timezone.utc)
            .astimezone(tz=timezone(offset=timedelta(hours=-3)))
            .strftime("%d/%m/%Y %H:%M:%S")
        )
        last_vaccinated_date = adapter.get("data")
        total = adapter.get("total")
        total_vaccinated = adapter.get("total_de_vacinados")
        total_vaccinated_today = adapter.get("total_de_vacinados_hoje")
        vaccines = adapter.get("vacinas")
        self.update_sheet_headers(vaccines)
        row = [
            crawl_datetime,
            last_vaccinated_date,
            total,
            total_vaccinated,
            total_vaccinated_today,
        ]
        row.extend([value for vaccine in vaccines for value in vaccine.values()])
        self.worksheet.append_row(row)

    def update_sheet_headers(self, vaccines):
        self.worksheet.update_cell(1, 1, "Data e Horário da Coleta")
        self.worksheet.update_cell(1, 2, "Data")
        self.worksheet.update_cell(1, 3, "Total de Vacinas")
        self.worksheet.update_cell(1, 4, "Total de Vacinados")
        self.worksheet.update_cell(1, 5, "Total de Vacinados no Dia")
        offset = 1
        for vaccine in vaccines:
            vaccine_name = list(vaccine.keys())[0]
            vaccine_name = vaccine_name.split("_")
            vaccine_name = " ".join(list(map(lambda text: text.title(), vaccine_name)))
            self.worksheet.update_cell(1, 5 + offset, vaccine_name)
            offset += 1
