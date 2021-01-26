import re

import scrapy


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

        return {
            "total": int(total.replace(".", "")),
            "total_de_vacinados": int(total_vaccinated.replace(".", "")),
            "total_de_vacinados_hoje": int(total_vaccinated_today.replace(".", "")),
            "data": last_vaccinated_date,
            "vacinas": vaccines,
        }
