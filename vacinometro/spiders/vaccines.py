import re
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import scrapy
import json
import os


class VaccinesSpider(scrapy.Spider):
    name = "vaccines"
    allowed_domains = ["http://www.feiradesantana.ba.gov.br/coronavirus/vacinometro/"]
    start_urls = ["http://www.feiradesantana.ba.gov.br/coronavirus/vacinometro/"]

    def parse(self, response):
        shots = response.css("div h2 ::text").getall()
        total = shots[0]
        total_vaccinated = shots[-2]
        total_vaccinated_today = shots[-1]
        last_vaccinated_date = response.css("div h4 ::text").getall()[-1]

        last_vaccinated_date = re.findall(r"\d{2}\/\d{2}\/\d+", last_vaccinated_date)[0]

        vaccines = []
        for shot in shots:
            if "doses" in shot:
                shot = shot.strip()
                shot = shot.split()
                vaccines.append(
                    {f"{shot[-1].lower()}_quantidade": int(shot[0].replace(".", ""))}
                )

        total = int(total.replace(".", ""))
        total_vaccinated = int(total_vaccinated.replace(".", ""))
        total_vaccinated_today = int(total_vaccinated_today.replace(".", ""))

        sheet = get_gsheet()
        update_sheet_headers(sheet, vaccines)
        row = [last_vaccinated_date, total, total_vaccinated, total_vaccinated_today]
        row.extend([value for vaccine in vaccines for value in vaccine.values()])
        sheet.append_row(row)

        return {
            "total": total,
            "total_de_vacinados": total_vaccinated,
            "total_de_vacinados_hoje": total_vaccinated_today,
            "data": last_vaccinated_date,
            "vacinas": vaccines,
        }


def get_gsheet():
    scope = [
        "https://www.googleapis.com/auth/drive",
        "https://spreadsheets.google.com/feeds"
    ]
    key_file_dict = json.loads(os.getenv("GOOGLE_CREDENTIALS"))
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(key_file_dict, scope)

    gc = gspread.authorize(credentials)
    return gc.open_by_key(os.getenv("GOOGLE_SHEET_ID")).sheet1


def update_sheet_headers(sheet, vaccines):
    sheet.update_cell(1, 1, 'Data')
    sheet.update_cell(1, 2, 'Total de Vacinas')
    sheet.update_cell(1, 3, 'Total de Vacinados')
    sheet.update_cell(1, 4, 'Total de Vacinados no Dia')
    offset = 1
    for vaccine in vaccines:
        vaccine_name = list(vaccine.keys())[0]
        vaccine_name = vaccine_name.split("_")
        vaccine_name = " ".join(list(map(lambda text: text.title(), vaccine_name)))
        sheet.update_cell(1, 4 + offset, vaccine_name)
        offset += 1
