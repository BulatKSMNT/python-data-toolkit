#!/bin/bash

INPUT_FILE="../ex03/hh_positions.csv"
if [ ! -f $INPUT_FILE ]; then
  echo "Ошибка, файл не найден"
  exit 1
fi

awk -F',' '
  BEGIN {
      J = 0
      M = 0
      S = 0
  }
  NR>1 {
    if( $3 ~ /Junior/)
      J++
    if( $3 ~ /Middle/)
      M++
    if( $3 ~ /Senior/)
      S++
  }
  END {
    print S ",\"Senior\""
    print J ",\"Junior\""
    print M ",\"Middle\""
  }

' "$INPUT_FILE" | sort -t',' -k1,1nr | awk -F',' '
  BEGIN {
    print "\"name\",\"count\""
  }
  {
    print $2 "," $1
  }
' > hh_uniq_positions.csv

if [ $? -ne 0 ]; then
  echo "Произошла ошибка"
  exit 1
else
  echo "Данные сохранены"
fi