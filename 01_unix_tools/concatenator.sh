#!/bin/bash

OUTPUT_FILE="Merge.csv"

# Проверяем, есть ли CSV-файлы для объединения
if ! ls *.csv 1> /dev/null 2>&1; then
    echo "Ошибка"
    exit 1
fi


HEADER_FILE=$(mktemp)

FIRST_FILE=$(ls *.csv | head -n 1)
echo $FIRST_FILE
head -n 1 "$FIRST_FILE" > "$HEADER_FILE"
cat "$HEADER_FILE" > "$OUTPUT_FILE"

for file in *.csv; do
    if [ "$file" != "$OUTPUT_FILE" ]; then
        tail -n +2 "$file" >> "$OUTPUT_FILE"
    fi
done

#rm "$HEADER_FILE"

