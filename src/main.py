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

    parser.add_argument(
        '--min-age',
        type=int,
        default=None,
        help='Minimum age of users to include in statistics'
    )

    parser.add_argument(
        '--max-age',
        type=int,
        default=None,
        help='Maximum age of users to include in statistics'
    )

    args = parser.parse_args()
    analyzer = UserAnalyzer(args.file)
    analyzer.load_data()
    analyzer.display_loading_summary()
    analyzer.filter_users_by_age(min_age=args.min_age, max_age=args.max_age)
    stats = analyzer.calculate_statistics()
    analyzer.print_statistics(stats)
    analyzer.save_statistics_to_csv(stats)
    analyzer.plot_statistics(stats)
