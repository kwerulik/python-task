import json
import csv
from typing import List
from collections import Counter
from pydantic import ValidationError
from src.models import User
import matplotlib.pyplot as plt

class UserAnalyzer:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.users: List[User] = []
        self.errors: List[dict] = []

    def load_data(self):
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                raw_data = json.load(file)
                for item in raw_data:
                    try:
                        user = User(**item)
                        self.users.append(user)
                    except ValidationError as e:
                        self.errors.append({"data": item, "error": str(e)})

        except FileNotFoundError:
            print(f"Error: File not found: {self.file_path}")
        except json.JSONDecodeError:
            print(f"Error: File {self.file_path} is not a valid JSON format.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def display_loading_summary(self):
        print(f"Successfully loaded {len(self.users)} valid users.")
        if self.errors:
            print(f"Rejected {len(self.errors)} invalid records.")

    def calculate_statistics(self) -> dict:
        if not self.users:
            return {}

        total_age = sum(user.age for user in self.users)
        average_age = total_age / len(self.users)

        cities = [user.city for user in self.users if user.city]
        city_counts = dict(Counter(cities))

        oldest = max(self.users, key=lambda u: u.age)
        youngest = min(self.users, key=lambda u: u.age)

        return {
            "average_age": round(average_age),
            "city_counts": city_counts,
            "oldest": oldest,
            "youngest": youngest
        }

    def print_statistics(self, stats: dict):
        if not stats:
            print("No data available to display statistics.")
            return

        print(f"Average age: {stats['average_age']}")

        print("Users in cities:")
        for city, count in stats['city_counts'].items():
            print(f" - {city}: {count}")

        print(f"Oldest: {stats['oldest'].name} ({stats['oldest'].age})")
        print(f"Youngest: {stats['youngest'].name} ({stats['youngest'].age})")

    def save_statistics_to_csv(self, stats: dict, output_file: str = "statistics.csv"):
        if not stats:
            print("No data available to save.")
            return

        try:
            with open(output_file, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)

                writer.writerow(["Metric", "Value"])
                writer.writerow(["Average Age", stats['average_age']])
                writer.writerow(
                    ["Oldest User", f"{stats['oldest'].name} ({stats['oldest'].age})"])
                writer.writerow(
                    ["Youngest User", f"{stats['youngest'].name} ({stats['youngest'].age})"])
                writer.writerow([])

                writer.writerow(["City", "User Count"])
                for city, count in stats['city_counts'].items():
                    writer.writerow([city, count])

            print(f"Statistics successfully saved to {output_file}")

        except Exception as e:
            print(f"Failed to save statistics to CSV: {e}")

    def plot_statistics(self, stats: dict, output_file: str = "statistics_chart.png"):
        """Generates and saves a bar chart of users per city."""
        if not stats or not stats.get('city_counts'):
                print("No data available to plot.")
                return
        try:
            cities = list(stats['city_counts'].keys())
            counts = list(stats['city_counts'].values())

            plt.figure(figsize=(8, 5))
            plt.bar(cities, counts, color='#4CAF50')

            plt.title('Number of Users per City', fontsize=14)
            plt.xlabel('City', fontsize=12)
            plt.ylabel('Number of Users', fontsize=12)

            plt.yticks(range(0, max(counts) + 2))
            plt.tight_layout() 
            plt.savefig(output_file)
            print(f"Chart successfully saved to {output_file}")

        except Exception as e:
            print(f"Failed to generate chart: {e}")


    def filter_users_by_age(self, min_age: int = None, max_age: int = None) -> None:
        """Filters the loaded users list based on provided age boundaries."""
        original_count = len(self.users)

        if min_age is not None:
            self.users = [user for user in self.users if user.age >= min_age]

        if max_age is not None:
            self.users = [user for user in self.users if user.age <= max_age]

        filtered_count = len(self.users)

        if original_count != filtered_count:
            print(
                f"Applied age filters. Users remaining: {filtered_count} out of {original_count}.")
