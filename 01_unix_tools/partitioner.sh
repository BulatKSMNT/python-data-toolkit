#!/bin/bash

INPUT_FILE="../ex03/hh_positions.csv"

if [ ! -f "$INPUT_FILE" ]; then
    echo "Error: Input file '$INPUT_FILE' not found"
    exit 1
fi

awk -F',' '
  BEGIN {OFS=","}
  NR==1 { header = $0 }
  NR > 1{
      gsub(/"/, "", $2)
      split($2, datetime, "T")
      date = datetime[1]
      $2 = "\"" $2 "\""
      if (!(date in files_created)) {
          print header > (date ".csv")
          files_created[date] = 1
      }
      output = $1
      for (i = 2; i <= NF; i++) {
        if ($i != "") {
            output = output OFS $i
        }
      }
      print output >> (date ".csv")
      close(date ".csv")
  }
' "$INPUT_FILE"

echo "Partitioning complete. Files created:"
ls *.csv | grep -v "$(basename "$INPUT_FILE")"