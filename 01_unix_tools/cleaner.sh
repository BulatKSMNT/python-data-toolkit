#!/bin/bash

INPUT_FILE="../ex02/hh_sorted.csv"
if [ ! -f $INPUT_FILE ]; then
  echo "Ошибка, файл не найден"
  exit 1
fi

awk -F',' '
  BEGIN {OFS=","}
  NR==1 {print $0}
  NR>1 {
    if ($4 ~ /false|true/)
      original_name = $3
    else
    {
      original_name = $3 $4
      $4 = " "
    }
    new_name = ""
    if (original_name ~ /Junior|junior/) {
      new_name = new_name "Junior"
    }
    if (original_name ~ /Middle|middle/) {
      new_name = new_name (new_name == "" ? "Middle" : "/Middle")
    }
    if (original_name ~ /Senior|senior/) {
      new_name = new_name (new_name == "" ? "Senior" : "/Senior")
    }

    if (new_name == "") {
      $3 = "\"-\""
    } else {
      $3 = "\"" new_name "\""
    }
    output = $1
    for (i = 2; i <= NF; i++) {
        if ($i != "") {
            output = output OFS $i
        }
    }
    print output
  }
' "$INPUT_FILE" > hh_positions.csv
if [ $? -ne 0 ]; then
  echo "Не удалось выполнить программу"
  exit 1
else
  echo "Данные сохранены"
fi