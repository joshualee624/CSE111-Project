import sqlite3
import pandas as pd
import os

# Database and schema paths
DB_PATH = './NBA_stats.sqlite'
SCHEMA_PATH = './sql/create_table.sql'

def execute_schema(conn):
    """Execute the schema SQL file to create tables with PKs and FKs"""
    if os.path.exists(SCHEMA_PATH):
        print(f"Executing schema from {SCHEMA_PATH}...")
        with open(SCHEMA_PATH, 'r') as f:
            schema_sql = f.read()
        conn.executescript(schema_sql)
        print("Schema created successfully with PKs and FKs!")
    else:
        print(f"Warning: Schema file not found at {SCHEMA_PATH}")

def load_players(conn):
    """Load PLAYER table with PlayerID as PK"""
    print("Loading PLAYER table...")
    df = pd.read_csv('./nba/Player Career Info.csv')
    # Map CSV columns to schema columns
    player_data = df[['player_id', 'player', 'birth_date', 'ht_in_in', 'wt']].copy()
    player_data.columns = ['PlayerID', 'PlayerName', 'BornDate', 'Height', 'Weight']
    player_data.to_sql('PLAYER', conn, if_exists='append', index=False)
    print(f"  Loaded {len(player_data)} players")

def load_teams(conn):
    """Load TEAM table with TeamID as PK"""
    print("Loading TEAM table...")
    # Load all team info from comprehensive CSV
    df_team = pd.read_csv('./basketball/team_complete.csv')
    if 'abbreviation' in df_team.columns and 'full_name' in df_team.columns:
        team_data = df_team[['abbreviation', 'full_name', 'city']].drop_duplicates()
        team_data.columns = ['TeamID', 'TeamName', 'City']
        team_data['ArenaName'] = None
        team_data.to_sql('TEAM', conn, if_exists='append', index=False)
        print(f"  Loaded {len(team_data)} teams from team_complete.csv")
    
    # Update ArenaName from Team Summaries.csv (most recent season)
    df_summaries = pd.read_csv('./nba/Team Summaries.csv')
    if 'abbreviation' in df_summaries.columns and 'arena' in df_summaries.columns:
        # Get the most recent arena for each team (first occurrence in the file)
        arena_data = df_summaries[['abbreviation', 'arena']].drop_duplicates(subset=['abbreviation'], keep='first')
        for _, row in arena_data.iterrows():
            conn.execute("UPDATE TEAM SET ArenaName = ? WHERE TeamID = ?", (row['arena'], row['abbreviation']))
        print(f"  Updated arena info for {len(arena_data)} teams")

def load_seasons(conn):
    """Load SEASON table with SeasonID as PK"""
    print("Loading SEASON table...")
    df = pd.read_csv('./nba/Player Season Info.csv')
    # Extract unique seasons
    season_data = df[['season']].drop_duplicates().copy()
    season_data.columns = ['SeasonID']
    season_data['YearStart'] = season_data['SeasonID'].astype(str).str[:4].astype(int)
    season_data['YearEnd'] = season_data['YearStart'] + 1
    season_data['SeasonTeam'] = None
    season_data.to_sql('SEASON', conn, if_exists='append', index=False)
    print(f"  Loaded {len(season_data)} seasons")

def load_player_season(conn):
    """Load PLAYER_SEASON junction table (FK: PlayerID, SeasonID)"""
    print("Loading PLAYER_SEASON table...")
    df = pd.read_csv('./nba/Player Season Info.csv')
    # Filter out null player_ids
    df = df.dropna(subset=['player_id'])
    ps_data = df[['player_id', 'season', 'team', 'age', 'experience', 'pos']].copy()
    ps_data.columns = ['PlayerID', 'SeasonID', 'Team', 'Age', 'Experience', 'position']
    # Remove duplicates - keep first occurrence (some players appear multiple times per season due to trades)
    ps_data = ps_data.drop_duplicates(subset=['PlayerID', 'SeasonID'], keep='first')
    ps_data.to_sql('PLAYER_SEASON', conn, if_exists='append', index=False)
    print(f"  Loaded {len(ps_data)} player-season records")

def load_draft_picks(conn):
    """Load DRAFT_PICK table with FK to SEASON and PLAYER"""
    print("Loading DRAFT_PICK table...")
    # Get existing PlayerIDs to avoid FK violations
    cursor = conn.cursor()
    cursor.execute("SELECT PlayerID FROM PLAYER")
    existing_players = set(row[0] for row in cursor.fetchall())
    
    df = pd.read_csv('./nba/Draft Pick History.csv')
    # Create DraftPickID from season and overall_pick
    df['DraftPickID'] = df['season'].astype(str) + '_' + df['overall_pick'].astype(str)
    draft_data = df[['DraftPickID', 'season', 'overall_pick', 'player_id']].copy()
    draft_data.columns = ['DraftPickID', 'SeasonID', 'OverallPick', 'PlayerID']
    # Filter to only existing players
    draft_data = draft_data[draft_data['PlayerID'].isin(existing_players)]
    # Remove duplicates
    draft_data = draft_data.drop_duplicates(subset=['DraftPickID'], keep='first')
    draft_data.to_sql('DRAFT_PICK', conn, if_exists='append', index=False)
    print(f"  Loaded {len(draft_data)} draft picks")

def load_awards(conn):
    """Load AWARD table and PLAYERAWARD junction table"""
    print("Loading AWARD and PLAYERAWARD tables...")
    df = pd.read_csv('./nba/Player Award Shares.csv')
    
    # Load unique awards
    award_data = df[['award']].drop_duplicates().copy()
    award_data['AwardID'] = award_data['award']
    award_data.columns = ['AwardName', 'AwardID']
    award_data = award_data[['AwardID', 'AwardName']]
    award_data.to_sql('AWARD', conn, if_exists='append', index=False)
    print(f"  Loaded {len(award_data)} awards")
    
    # Load PLAYERAWARD junction (filter out null player_ids)
    pa_data = df[['award', 'player_id', 'season']].copy()
    pa_data = pa_data.dropna(subset=['player_id'])  # Remove rows with null PlayerID
    pa_data.columns = ['AwardID', 'PlayerID', 'AwardYear']
    pa_data.to_sql('PLAYER_AWARD', conn, if_exists='append', index=False)
    print(f"  Loaded {len(pa_data)} player-award records")

def load_all_star(conn):
    """Load ALL_STAR and ALL_STAR_PLAYER tables"""
    print("Loading ALL_STAR tables...")
    
    # Load winning teams from CSV
    df_winners = pd.read_csv('./nba/all_star_winners.csv')
    winning_teams = dict(zip(df_winners['season'], df_winners['winning_team']))
    
    df = pd.read_csv('./nba/All-Star Selections.csv')
    
    # Create ALL_STAR entries for each season
    allstar_data = df[['season']].drop_duplicates().copy()
    allstar_data['AllStarID'] = 'AS_' + allstar_data['season'].astype(str)
    allstar_data['WinningTeam'] = allstar_data['season'].map(winning_teams)
    allstar_data = allstar_data[['AllStarID', 'WinningTeam']]
    allstar_data.to_sql('ALL_STAR', conn, if_exists='append', index=False)
    print(f"  Loaded {len(allstar_data)} All-Star games")
    
    # Load ALL_STAR_PLAYER junction (filter out null player_ids)
    asp_data = df.copy()
    asp_data = asp_data.dropna(subset=['player_id'])  # Remove rows with null PlayerID
    asp_data['AllStarID'] = 'AS_' + asp_data['season'].astype(str)
    asp_data = asp_data[['AllStarID', 'player_id', 'season', 'team']].copy()
    asp_data.columns = ['AllStarID', 'PlayerID', 'SelectionYear', 'Team']
    asp_data.to_sql('ALL_STAR_PLAYER', conn, if_exists='append', index=False)
    print(f"  Loaded {len(asp_data)} All-Star selections")

def load_statistics(conn):
    """Load STATISTICS table with FK to PLAYER"""
    print("Loading STATISTICS table...")
    # Get existing PlayerIDs and TeamIDs to avoid FK violations
    cursor = conn.cursor()
    cursor.execute("SELECT TeamID FROM TEAM")
    existing_teams = set(row[0] for row in cursor.fetchall())
    
    df = pd.read_csv('./nba/Player Totals.csv')
    # Filter out null player_ids and TOT (total) rows to avoid double-counting
    df = df.dropna(subset=['player_id'])
    # Filter to only existing players and teams
    df = df[df['team'].isin(existing_teams)]
    # Create StatsID from player_id, season, and team to handle trades
    df['StatsID'] = df['player_id'] + '_' + df['season'].astype(str) + '_' + df['team'].astype(str)
    stats_data = df[['StatsID', 'player_id', 'season', 'team', 'pts', 'trb', 'ast', 'stl', 'blk']].copy()
    stats_data.columns = ['StatsID', 'PlayerID', 'SeasonID', 'TeamID', 'Points', 'Rebounds', 'Assist', 'Steals', 'Blocks']
    # Remove any remaining duplicates
    stats_data = stats_data.drop_duplicates(subset=['StatsID'], keep='first')
    stats_data.to_sql('STATISTICS', conn, if_exists='append', index=False)
    print(f"  Loaded {len(stats_data)} statistics records")

def load_games(conn):
    """Load GAME table"""
    print("Loading GAME table...")
    try:
        # Get existing TeamIDs to avoid FK violations
        cursor = conn.cursor()
        cursor.execute("SELECT TeamID FROM TEAM")
        existing_teams = set(row[0] for row in cursor.fetchall())
        
        df = pd.read_csv('./basketball/game.csv')
        game_data = df[['game_id', 'game_date', 'team_abbreviation_home', 'team_abbreviation_away', 'pts_home', 'pts_away', 'wl_home']].copy()
        game_data.columns = ['GameID', 'GameDate', 'HomeTeamID', 'AwayTeamID', 'HomeScore', 'AwayScore', 'wl_home']
        # Filter to only include games where both teams exist
        game_data = game_data[game_data['HomeTeamID'].isin(existing_teams) & game_data['AwayTeamID'].isin(existing_teams)]
        game_data['Winner'] = game_data.apply(lambda row: row['HomeTeamID'] if row['wl_home'] == 'W' else row['AwayTeamID'], axis=1)
        game_data = game_data[['GameID', 'GameDate', 'HomeTeamID', 'AwayTeamID', 'HomeScore', 'AwayScore', 'Winner']]
        game_data.to_sql('GAME', conn, if_exists='replace', index=False)
        print(f"  Loaded {len(game_data)} games")
    except Exception as e:
        print(f"  Warning: Could not load games - {e}")

def load_player_team(conn):
    """Load PLAYER_TEAM junction table (plays for relationship)"""
    print("Loading PLAYER_TEAM table...")
    # Get existing PlayerIDs and TeamIDs to avoid FK violations
    cursor = conn.cursor()
    cursor.execute("SELECT PlayerID FROM PLAYER")
    existing_players = set(row[0] for row in cursor.fetchall())
    cursor.execute("SELECT TeamID FROM TEAM")
    existing_teams = set(row[0] for row in cursor.fetchall())
    
    df = pd.read_csv('./nba/Player Season Info.csv')
    # Filter out null player_ids
    df = df.dropna(subset=['player_id'])
    pt_data = df[['player_id', 'team', 'pos']].copy()
    pt_data.columns = ['PlayerID', 'TeamID', 'position']
    # Filter to only existing players and teams
    pt_data = pt_data[pt_data['PlayerID'].isin(existing_players) & pt_data['TeamID'].isin(existing_teams)]
    # Remove duplicates - keep first occurrence per player-team
    pt_data = pt_data.drop_duplicates(subset=['PlayerID', 'TeamID'], keep='first')
    # Set position to None if 'NA'
    pt_data['position'] = pt_data['position'].replace('NA', None)
    # Set Traded based on whether player played for multiple teams
    player_team_counts = pt_data.groupby('PlayerID')['TeamID'].nunique()
    pt_data['Traded'] = pt_data['PlayerID'].map(lambda p: 1 if player_team_counts[p] > 1 else 0)
    pt_data.to_sql('PLAYER_TEAM', conn, if_exists='replace', index=False)
    print(f"  Loaded {len(pt_data)} player-team records")

def main():
    """Main function to create database with proper schema and load data"""
    conn = sqlite3.connect(DB_PATH)
    
    try:
        # Step 1: Create schema with PKs and FKs
        execute_schema(conn)
        
        # Step 2: Load base tables first (no FK dependencies)
        load_players(conn)
        load_teams(conn)
        load_seasons(conn)
        load_awards(conn)
        load_all_star(conn)
        
        # Step 3: Load junction/dependent tables (with FKs)
        load_player_season(conn)
        load_player_team(conn)
        load_draft_picks(conn)
        load_statistics(conn)
        load_games(conn)
        load_player_team(conn)
        
        conn.commit()
        print("\n✓ Database created successfully with all PKs and FKs!")
        print(f"✓ Database location: {os.path.abspath(DB_PATH)}")
        
    except Exception as e:
        conn.rollback()
        print(f"\n✗ Error: {e}")
        raise
    finally:
        conn.close()

if __name__ == '__main__':
    main()