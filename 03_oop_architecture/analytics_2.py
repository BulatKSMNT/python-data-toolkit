from random import randint
import logging
import requests
import json
import config

logging.basicConfig(
    filename=config.log_file,
    level=logging.INFO,
    format=config.log_format,
    datefmt='%Y-%m-%d %H:%M:%S'
)

class Research:
    def __init__(self, name = 'test.csv'):
        self.name = name
        logging.info(f"Initializing Research with path: {name}")

    def file_reader(self, has_header = True):
        logging.info(f"Starting file reading from {self.name}, has_header={has_header}")
        try:
            with open(self.name, 'r') as file:
                lines = file.readlines()
            if not lines:
                logging.error("File is empty")
                raise Exception("Empty file")

            lines = [line.strip() for line in lines]
            logging.info(f"Read {len(lines)} lines from file")

            if len(lines[0].split(",")) != 2:
                logging.error(f"Invalid header data format")
                raise Exception("Invalid header")
            lines = lines[1:]
            for i, line in enumerate(lines, 1):
                if not line:
                    continue
                data = line.split(',')
                if len(data) != 2:
                    logging.error(f"Invalid data format at line {i + 1}")
                    raise Exception(f"Invalid format in {i + 1} line")
                for value in data:
                    if value not in ['0', '1']:
                        logging.error(f"Invalid value {value} at line {i + 1}")
                        raise Exception(f"Invalid value '{value}' in  {i + 1} line. 0 or 1.")
            return lines

        except FileNotFoundError:
            logging.error(f"File not found: {self.name}")
            return f"Error: File {self.name} not found."
        except Exception as e:
            logging.error(f"Error in file_reader: {str(e)}")
            raise e

    class Calculations:
        def __init__(self, data):
            logging.info(f"Initializing Calculations with {len(data)} data points")
            self.data = data

        def counts_value(self):
            logging.info("Calculating the counts of heads and tails")
            if not self.data:
                logging.info(f"Don't have the data")
                return [0,0]
            heads = 0
            tails = 0
            for row in self.data:
                values = row.split(',')
                if values[0] == '1':
                    heads += 1
                if values[1] == '1':
                    tails += 1
            logging.info(f"Counts calculated: {heads} heads, {tails} tails")
            return [heads, tails]

        def fractions(self,count):
            logging.info(f"Calculating fractions for {count[0]} heads and {count[1]} tails")
            if sum(count) == 0:
                logging.warning("Total count is zero, returning 0% for both")
                raise ValueError("Error: Cannot calculate fractions - sum is zero")
            logging.info(f"Fractions calculated: {count[0]:.2f}% heads, {count[1]:.2f}% tails")
            return [count[0] / sum(count) * 100, count[1] / sum(count) * 100]
    def send_report_to_telegramm(self, success):
        message = ("The report has been successfully created" if success else "The report hasn’t been created due to an error")
        payload = {
            "chat_id": 1251634923,
            "text": message
        }
        try:
            response = requests.post(
                config.TELEGRAM_WEBHOOK_URL,
                data=json.dumps(payload),
                headers={"Content-Type": "application/json"}
            )
            if response.status_code != 200:
                logging.error(f"Failed to send message: {response.text}")
            else:
                logging.info(f"Success to send message from telegram-bot")
        except Exception as e:
            logging.error(f"Error sending to Telegram: {e}")

class Analytics(Research.Calculations):

    def predict_random(self, steps):
        logging.info(f"Generating {steps} random predictions")
        predictions = []
        for _ in range(steps):
            random_value = randint(0, 1)
            if random_value == 0:
                predictions.append([1, 0])
            else:
                predictions.append([0, 1])
        logging.info(f"Generated {len(predictions)} random predictions")
        return predictions
    def predict_last(self):
        logging.info("Getting last prediction from data")
        if not self.data:
            logging.error("No data available for last prediction")
            raise Exception("Don't have a data to the predictions")
        logging.info(f"Last prediction: {self.data[-1]}")
        return self.data[-1]

    def save_file(self, data, filename, extension):
        full_filename = f"{filename}.{extension}"
        logging.info(f"Saving data to file: {full_filename}")
        try:
            with open(full_filename, 'w', encoding='utf-8') as file:
                file.write(str(data))
            logging.info(f"Data successfully saved to {full_filename}")
        except Exception as e:
            logging.error(f"Error saving file {full_filename}: {str(e)}")
            raise Exception(f"Fail for save file: {e}")

    def count_predictions(self, predictions):
        logging.info(f"Counting predictions for {len(predictions)} items")
        heads = 0
        tails = 0

        for prediction in predictions:
            if prediction[0] == 1:
                tails += 1
            else:
                heads += 1
        logging.info(f"Prediction counts: {heads} heads, {tails} tails")
        return heads, tails

    def get_observations_count(self):
        logging.info(f"Total observations count: {len(self.data)}")
        return len(self.data)
