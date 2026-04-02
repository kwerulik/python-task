import json
from typing import Optional, List
from pydantic import BaseModel, ValidationError

class User(BaseModel):
    name: str
    age: int
    city: Optional[str] = None

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
            print(f"Błąd: Nie znaleziono pliku: {self.file_path}")
        except json.JSONDecodeError:
            print(
                f"Błąd: Plik {self.file_path} nie ma poprawnego formatu JSON.")
        except Exception as e:
            print(f"Wystąpił nieoczekiwany błąd: {e}")

    def display_loading_summary(self):
        print(f"Pomyślnie załadowano {len(self.users)} poprawnych użytkowników.")
        if self.errors:
            print(f"Odrzucono {len(self.errors)} błędnych rekordów.")


if __name__ == "__main__":
    analyzer = UserAnalyzer("data/Users.json")
    analyzer.load_data()
    analyzer.display_loading_summary()
