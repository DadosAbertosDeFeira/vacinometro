# vacinometro

Coleta dados da vacinação em Feira de Santana 💉

Fonte: http://www.feiradesantana.ba.gov.br/coronavirus/vacinometro/

## Desenvolvimento

Para utilizar o scrapy em Python, você precisará do Poetry. Instale as dependências com:

```
poetry install
```

Execute o raspador com:

```
poetry run scrapy crawl vaccines
```

Para utilizar o scrapy em R, as dependências são instaladas automaticamente:


Para executar, você deve rodar o comando:

```
Rscript scraper.R
```

Um arquivo .csv será gerado automaticamente.
