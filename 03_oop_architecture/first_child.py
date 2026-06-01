import sys
from random import randint
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
            print(lines)
            return lines

        except FileNotFoundError:
            return f"Error: File {self.name} not found."
        except Exception as e:
            raise e
    class Calculations:
        def __init__(self, data):
            self.data = data

        def counts_value(self):
            if not self.data:
                return [0,0]
            heads = 0
            tails = 0
            for row in self.data:
                values = row.split(',')
                if values[0] == '1':
                    heads += 1
                if values[1] == '1':
                    tails += 1

            return [heads, tails]

        def fractions(self,count):
            if sum(count) == 0:
                raise ValueError("Error: Cannot calculate fractions - sum is zero")
            return [count[0] / sum(count) * 100, count[1] / sum(count) * 100]
class Analytics(Research.Calculations):

    def predict_random(self, steps):
        predictions = []
        for _ in range(steps):
            random_value = randint(0, 1)
            if random_value == 0:
                predictions.append([1, 0])
            else:
                predictions.append([0, 1])

        return predictions
    def predict_last(self):
        if not self.data:
            raise Exception("Don't have a data to the predictions")
        return self.data[-1]


if __name__=="__main__":
    if len(sys.argv) != 2:
        print("Invalid command: python first_constructor <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]

    try:
        research = Research(file_path)
        data = research.file_reader()
        print(data)

        calc = Research.Calculations(data)
        print("test")
        counts = calc.counts_value()
        print(f"{counts[0]} , {counts[1]}")

        fhead, ftail = calc.fractions(counts)
        print(f"{fhead} , {ftail}")
        print("test")
        analytics = Analytics(data)

        random_predictions = analytics.predict_random(3)
        print(random_predictions)

        last_prediction = analytics.predict_last()
        print(last_prediction)

    except Exception as e:
        print(f"Ошибка: {e}")
        sys.exit(1)

