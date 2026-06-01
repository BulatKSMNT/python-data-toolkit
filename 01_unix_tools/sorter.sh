#!/bin/bash

if [ ! -f "../ex01/hh.csv" ]; then
  echo "Ошибка, файл не найден"
  exit 1
fi

head -n 1 ../ex01/hh.csv > hh_sorted.csv
tail -n +2 ../ex01/hh.csv |sort -t',' -k 2 | sort -t',' -k 1 >> hh_sorted.csv

if [ $? -ne 0 ]; then
  echo "Не удалось выполнить сортировку"
  exit 1
else
  echo "Данные сохранены в sorted_hh.csv"
fi