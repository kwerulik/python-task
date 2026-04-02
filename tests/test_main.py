import pytest
from pydantic import ValidationError
from src.models import User
from src.analyzer import UserAnalyzer


def test_user_valid_data():
    """Test if valid data creates a User object without errors."""
    user = User(name="Anna", age=25, city="Warsaw")
    assert user.name == "Anna"
    assert user.age == 25
    assert user.city == "Warsaw"

def test_user_city_normalization():
    """Test if cities are correctly normalized (stripped of whitespaces and title-cased)."""
    user = User(name="Jan", age=30, city="  krakow  ")
    assert user.city == "Krakow"

def test_user_invalid_age():
    """Test if Pydantic rejects negative age and age over 150."""
    with pytest.raises(ValidationError):
        User(name="Marek", age=-5, city="Lodz")

    with pytest.raises(ValidationError):
        User(name="Marek", age=151, city="Lodz")

def test_user_empty_name():
    """Test if records with an empty name are rejected."""
    with pytest.raises(ValidationError):
        User(name="", age=30, city="Gdansk")

@pytest.fixture
def sample_analyzer():
    """Fixture providing a ready-to-use UserAnalyzer object with mock data for statistics testing."""
    analyzer = UserAnalyzer("dummy_path.json")
    analyzer.users = [
        User(name="Anna", age=25, city="Warsaw"),
        User(name="Jan", age=30, city="Krakow"),
        User(name="Maria", age=20, city="Warsaw"),
    ]
    return analyzer

def test_calculate_statistics(sample_analyzer):
    """Test the logic for calculating average age, city counts, and finding extreme ages."""
    stats = sample_analyzer.calculate_statistics()

    assert stats["average_age"] == 25  # (25 + 30 + 20) / 3
    assert stats["city_counts"] == {"Warsaw": 2, "Krakow": 1}
    assert stats["oldest"].name == "Jan"
    assert stats["oldest"].age == 30
    assert stats["youngest"].name == "Maria"
    assert stats["youngest"].age == 20

def test_calculate_statistics_empty():
    """Test if the application safely handles an empty list of users."""
    analyzer = UserAnalyzer("dummy_path.json")
    stats = analyzer.calculate_statistics()
    assert stats == {}
