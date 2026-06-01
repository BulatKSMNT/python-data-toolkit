#!/bin/bash

if [ -z "$1" ]; then
  echo "Используй: $0 \"название_вакансии\""
  exit 1
fi

VACANCY=$1
PER_PAGE=20

echo "Начало обработки..."
echo "Количество выводимых вакансий: $PER_PAGE"
curl -s "https://api.hh.ru/vacancies?text=$(echo $VACANCY | sed 's/ /%20/g')&per_page=$PER_PAGE&page=0" | \
jq -r '
  # Выводим метаданные
  "{",
  " page: \(.page)",
  " found: \(.found)",
  " clusters: \(.clusters)",
  " arguments: \(.arguments)",
  " per_page: \(.per_page)",
  " pages: \(.pages)",
  " items: [",
  # Обрабатываем массив items
  (.items | to_entries[] |
    "    {",
    "     \"apply_alternate_url\": \"\(.value.apply_alternate_url)\",",
    "     \"address\": {",
    "        \"id\": \"\(.value.address.id)\",",
    "       \"lat\": \(.value.address.lat // "null"),",
    "       \"metro\": {",
    "         \"station_id\": \"\(.value.address.metro.station_id // "null")\",",
    "         \"line_name\": \"\(.value.address.metro.line_name // "null")\",",
    "         \"lng\": \(.value.address.metro.lng // "null"),",
    "         \"line_id\": \"\(.value.address.metro.line_id // "null")\",",
    "         \"station_name\": \"\(.value.address.metro.station_name // "null")\",",
    "         \"lat\": \(.value.address.metro.lat // "null")",
    "       },",
    "       \"street\": \"\(.value.address.street // "null")\",",
    "       \"lng\": \(.value.address.lng // "null"),",
    "       \"metro_stations\": [",
    "         {",
    "           \"line_name\": \"\(.value.address.metro_stations[0].line_name // "null")\",",
    "           \"station_id\": \"\(.value.address.metro_stations[0].station_id // "null")\",",
    "           \"lng\": \(.value.address.metro_stations[0].lng // "null"),",
    "           \"line_id\": \"\(.value.address.metro_stations[0].line_id // "null")\",",
    "           \"lat\": \(.value.address.metro_stations[0].lat // "null"),",
    "           \"station_name\": \"\(.value.address.metro_stations[0].station_name // "null")\"",
    "         }",
    "       ]",
    "     },",
    "     \"building\": \"\(.value.building // "null")\",",
    "     \"city\": \"\(.value.city // "null")\",",
    "     \"description\": \"\(.value.description | tostring)\",",
    "     \"raw\": \"\(.value.raw // "null")\"",
    "   }" + (if .key == (length - 1) then "" else "," end)
  ),
  "  ]",
  "}"

' > hh.json

if [ $? -ne 0 ]; then
  echo "Не удалось получить данные с API"
  exit 1
fi

echo "Данные сохранены в hh.json"