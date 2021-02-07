# vacinometro

Coleta dados da vacinação em Feira de Santana 💉

Fonte: http://www.feiradesantana.ba.gov.br/coronavirus/vacinometro/

Os dados coletados são publicados em uma planilha online (Google Spreadsheets).

## Desenvolvimento

Crie um _virtual environment_ com `python -m venv venv` e ative com
`source venv/bin/activate`.

Então instale as dependências com:

```
pip install -r requirements.txt
```

Execute o raspador com:

```
scrapy crawl vaccines
```

## Configuração para a planilha

Para ativar a integração com uma planilha real você precisará
configurar a integração com a API do Google Spreadsheet e também
do ID da spreedsheet onde deseja fazer o upload das informações.

Configure essas informações nas variáveis de ambiente `GOOGLE_CREDENTIALS` e `GOOGLE_SHEET_ID`.
Caso elas não estejam configuradas o raspador assumirá que você
está em um ambiente de desenvolvimento e as informações serão mostradas
no terminal apenas.
