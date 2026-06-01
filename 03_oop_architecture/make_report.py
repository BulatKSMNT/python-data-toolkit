import sys
import config
from analytics import Research, Analytics


def main():
    if len(sys.argv) != 2:
        print("Invalid argument: python make_report.py <path_the_file>")
        sys.exit(1)

    file_path = sys.argv[1]

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

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
