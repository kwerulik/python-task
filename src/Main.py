import json
from typing import Optional, List
from collections import Counter
from pydantic import BaseModel, ValidationError, field_validator


class User(BaseModel):
    name: str
    age: int
    city: Optional[str] = None

    @field_validator('city')
    @classmethod
    def normalize_city(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            return v.strip().title()
        return v
    

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


if __name__ == "__main__":
    analyzer = UserAnalyzer("data/Users.json")
    analyzer.load_data()
    analyzer.display_loading_summary()
    stats = analyzer.calculate_statistics()
    analyzer.print_statistics(stats)
