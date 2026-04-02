import argparse
from src.analyzer import UserAnalyzer


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Analyze user data from a JSON file.")

    parser.add_argument(
        '-f', '--file',
        type=str,
        default='data/Users.json',
        help='Path to the JSON file containing user data'
    )

    args = parser.parse_args()

    analyzer = UserAnalyzer(args.file)
    analyzer.load_data()
    analyzer.display_loading_summary()
    stats = analyzer.calculate_statistics()
    analyzer.print_statistics(stats)
    analyzer.save_statistics_to_csv(stats)
