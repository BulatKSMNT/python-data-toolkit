def core(input_name, output_name):
    with open(input_name, 'r') as csv_file:
        with open(output_name, 'w') as tsv_file:
            for line in csv_file:
                fields = []
                quotes = False
                field = []

                for char in line:
                    if char == '"':
                        quotes = not quotes
                    elif char == ',' and not quotes:
                        fields.append(''.join(field))
                        field = []
                    else:
                        field.append(char)
                fields.append(''.join(field))
                tsv_file.write('\t'.join(fields))


if __name__ == "__main__":
    core('ds.csv', 'ds.tsv')