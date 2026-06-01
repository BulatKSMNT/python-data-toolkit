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

    def save_file(self, data, filename, extension):
        full_filename = f"{filename}.{extension}"
        try:
            with open(full_filename, 'w', encoding='utf-8') as file:
                file.write(str(data))
        except Exception as e:
            raise Exception(f"Fail for save file: {e}")

    def count_predictions(self, predictions):
        heads = 0
        tails = 0

        for prediction in predictions:
            if prediction[0] == 1:
                tails += 1
            else:
                heads += 1

        return heads, tails

    def get_observations_count(self):
        return len(self.data)



