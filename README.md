PACOTES UTILIZADOS:
  - scrapyd
  - python-scrapyd-api
  - googlefinance
  - wikipedia
  - pandas-datareader

Antes de fazer o makemigrations:
  - Comentar a linha 52 a 58 do urls.py, pra ele não começar a importar os dados (O django executa o server quando faz migração)
  - python manage.py makemigrations
  - python manage.py migrate
  - Descomentar a linha

Antes de rodar o servidor, verificar:
  - Porta no settings.py está correta?
  - Postgresql está rodando?
  - Apagar a pasta dbs dentro do scraper
  - Colocar para rodar o scrapyd na pasta do scraper no siteApp

Em seguida rodar o servidor.
