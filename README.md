A simple Python CLI application that reads user data from a JSON file, validates it, calculates basic statistics, and exports the results (CSV + Bar Chart).

## Quick Setup

1. Create and activate a virtual environment:
    * **Windows:**
      `python -m venv venv`
      `.\venv\Scripts\activate`
    * **macOS/Linux:**
      `python -m venv venv`
      `source venv/bin/activate`

2. Install dependencies:
    `pip install -r requirements.txt`

## Usage

Run the app with the default sample data:
`python -m src.main`

Run with age filtering (e.g., users between 20 and 40 years old):
`python -m src.main --min-age 20 --max-age 40`

Run with your own custom JSON file:
`python -m src.main -f path/to/your/file.json`

## Features
* **Validation:** Uses Pydantic to drop bad records (e.g., negative age) and fix formatting (capitalizes city names).
* **Advanced Filtering:** Ability to filter users by age range via CLI arguments.
* **Stats:** Calculates average age, min/max age, and user count per city.
* **Exports:** Automatically generates `statistics.csv` and `statistics_chart.png` using Matplotlib.
## Testing

Run the pytest suite to verify the logic and data validation:
    `python -m pytest`
