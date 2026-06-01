import sys
import logging
import config
from analytics import Research, Analytics


def main():
    logging.info("Starting make_report program")
    if len(sys.argv) != 2:
        logging.error("Invalid number of arguments provided")
        print("Invalid argument: python make_report.py <path_the_file>")
        sys.exit(1)

    file_path = sys.argv[1]
    logging.info(f"Processing file: {file_path}")
    try:
        research = Research(file_path)
        data = research.file_reader()

        analytics = Analytics(data)

        heads, tails = analytics.counts_value()

        heads_percent, tails_percent = analytics.fractions([heads, tails])

        predictions = analytics.predict_random(config.num_of_steps)

        predicted_heads, predicted_tails = analytics.count_predictions(predictions)

        total_observations = analytics.get_observations_count()

        report = config.report_template.format(
            observations=total_observations,
            heads=heads,
            tails=tails,
            heads_percent=heads_percent,
            tails_percent=tails_percent,
            steps=config.num_of_steps,
            predicted_heads=predicted_heads,
            predicted_tails=predicted_tails
        )

        print(report)

        analytics.save_file(report, "report", "txt")
        logging.info("Report created successfully")
        Research.send_report_to_telegramm(research,True)

    except Exception as e:
        logging.error(f"Error during report creation: {str(e)}")
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
