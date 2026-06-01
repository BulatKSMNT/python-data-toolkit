#!/bin/bash

if [ -z "$1" ]; then
  echo "Используй: $0 \"название_вакансии\""
  exit 1
fi

VACANCY="$1"
PER_PAGE=20

echo "Начало обработки..."

curl -s "https://api.hh.ru/vacancies?text=$(echo $VACANCY | sed 's/ /%20/g')&per_page=$PER_PAGE&page=0" |
jq -r -f filter.jq > hh.csv

# Проверяем, успешно ли выполнен запрос
if [ $? -ne 0 ]; then
  echo "Ошибка: Не удалось получить или обработать данные с API"
  exit 1
fi

echo "Данные сохранены в hh.csv"