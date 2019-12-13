# Traffic accident map

### notebooks/vk_parser.ipynb - parsing news from the group
### to work you need a file notebooks/vk_api.txt with the vk api key
### notebooks/extract_address.ipynb - extract addresses from the text of the news
### flask/map.py - server that rendering an incident map for a specified period of time
### to work you need a file flask/api_key.txt with the yandex JavaScript and HTTP geocoder api key
### yandex geocoder gives coordinates to the entered address

```bash
docker-compose build - собрать
docker-compose up - запустить
```

### map.html a result of the program. The map shows all the accidents in the last year.