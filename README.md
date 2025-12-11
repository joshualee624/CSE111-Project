# NBA Database Management System

A Python-based command-line application for managing and querying NBA player, team, and game statistics.

## Features

- **Player Operations**: Search players, view info, career/season stats, awards, All-Star selections
- **Team Operations**: View teams, rosters, records, games
- **Statistics & Rankings**: Top scorers, assist leaders, rebounders, season standings
- **Draft & All-Star**: View draft picks and All-Star selections/winners
- **Database Updates**: Trade players, add statistics, view traded players

## Requirements

- Python 3.x
- SQLite3

## Setup

1. Ensure Python 3.x is installed
2. Run the database creation script:
   ```bash
   python datasets/create_sql.py
   ```
3. This will create the SQLite database from the CSV files

## Usage

Run the main application:
```bash
python nba_app.py
```

Follow the on-screen menu to navigate through different options.

## Database Schema

The application uses an SQLite database (`datasets/NBA_stats.sqlite`) with tables for:
- Players
- Teams
- Games
- Statistics
- Awards
- Draft picks
- All-Star selections

## Files

- `nba_app.py`: Main entry point
- `NBAApp.py`: Application logic and user interface
- `NBADatabase.py`: Database operations
- `datasets/`: CSV data files and SQL scripts

## Author

- Joshua Lee
- Nicola Cisbani
- Yiannis Karydis