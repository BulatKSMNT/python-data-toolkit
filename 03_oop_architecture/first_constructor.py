import sys
class Research:
    def __init__(self, name = 'test.csv'):
        self.name = name

    def file_reader(self):
        try:
            with open(self.name, 'r') as file:
                lines = file.readlines()
            if not lines:
                raise Exception("Empty file")
            lines = [line.strip() for line in lines]

            if len(lines[0].split(",")) != 2:
                raise Exception("Invalid header")
            lines = lines[1:]
            for i, line in enumerate(lines, 1):
                if not line:
                    continue
                data = line.split(',')
                if len(data) != 2:
                    raise Exception(f"Invalid format in {i + 1} line")
                for value in data:
                    if value not in ['0', '1']:
                        raise Exception(f"Invalid value '{value}' in  {i + 1} line. 0 or 1.")
            return '\n'.join(lines)

        except FileNotFoundError:
             return f"Error: File {self.name} not found."
        except Exception as e:
            raise e


if __name__=="__main__":
    if len(sys.argv) != 2:
        print("Invalid command: python first_constructor <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]

    try:
        research = Research(file_path)
        print(research.file_reader())
    except Exception as e:
        print(f"Ошибка: {e}")
        sys.exit(1)