import sqlite3
import sys
from typing import List, Tuple, Optional
from datetime import datetime

class NBADatabase:

    def __init__(self, db_path: str = "datasets/NBA_stats.sqlite"):
        
        try:
            self.conn = sqlite3.connect(db_path)
            self.cursor = self.conn.cursor()
            print(f"✓ Connected to database: {db_path}\n")
        except sqlite3.Error as e:
            print(f"✗ Error connecting to database: {e}")
            sys.exit(1)

    def close(self):

        if self.conn:
            self.conn.close()
            print("\n✓ Database connection closed")

    def get_player_info(self, player_id: str) -> Optional[Tuple]:

        query = """
            SELECT PlayerID, PlayerName, BornDate, Height, Weight
            FROM PLAYER
            WHERE PlayerID = ?
        """
        self.cursor.execute(query, (player_id,))
        return self.cursor.fetchone()
    
    def search_player_by_name(self, name_pattern: str) -> List[Tuple]:
        
        query = """
            SELECT PlayerID, PlayerName, BornDate, Height, Weight
            FROM PLAYER
            WHERE PlayerName LIKE ?
            ORDER BY PlayerName
        """
        self.cursor.execute(query, (f"%{name_pattern}%",))
        return self.cursor.fetchall()
    
    def get_players_by_position(self, position: str) -> List[Tuple]:
        
        query = """
            SELECT DISTINCT p.PlayerID, p.PlayerName, pt.position, t.TeamName
            FROM PLAYER p
            JOIN PLAYER_TEAM pt ON p.PlayerID = pt.PlayerID
            JOIN TEAM t ON pt.TeamID = t.TeamID
            WHERE pt.position = ?
            ORDER BY p.PlayerName
        """
        self.cursor.execute(query, (position,))
        return self.cursor.fetchall()
    
    def get_player_career_stats(self, player_id: str) -> Optional[Tuple]:
    
        query = """
            SELECT p.PlayerName, 
                   SUM(s.Points) as CareerPoints, 
                   SUM(s.Rebounds) as CareerRebounds, 
                   SUM(s.Assist) as CareerAssists,
                   SUM(s.Steals) as CareerSteals,
                   SUM(s.Blocks) as CareerBlocks
            FROM PLAYER p
            JOIN STATISTICS s ON p.PlayerID = s.PlayerID
            WHERE p.PlayerID = ?
            GROUP BY p.PlayerID, p.PlayerName
        """
        self.cursor.execute(query, (player_id,))
        return self.cursor.fetchone()
    
    def get_player_season_stats(self, player_id: str, season_id: str) -> Optional[Tuple]:
        
        query = """
            SELECT p.PlayerName, ps.Team, s.Points, s.Rebounds, s.Assist, s.Steals, s.Blocks
            FROM PLAYER p
            JOIN PLAYER_SEASON ps ON p.PlayerID = ps.PlayerID
            LEFT JOIN STATISTICS s ON p.PlayerID = s.PlayerID AND ps.SeasonID = s.SeasonID
            WHERE p.PlayerID = ? AND ps.SeasonID = ?
        """
        self.cursor.execute(query, (player_id, season_id))
        return self.cursor.fetchone()
    
    def get_player_awards(self, player_id: str) -> List[Tuple]:
        
        query = """
            SELECT a.AwardName, pa.AwardYear
            FROM AWARD a
            JOIN PLAYER_AWARD pa ON a.AwardID = pa.AwardID
            WHERE pa.PlayerID = ?
            ORDER BY pa.AwardYear DESC
        """
        self.cursor.execute(query, (player_id,))
        return self.cursor.fetchall()
    
    def get_player_allstar_selections(self, player_id: str) -> List[Tuple]:
    
        query = """
            SELECT asp.SelectionYear, asp.Team, als.WinningTeam
            FROM ALL_STAR_PLAYER asp
            JOIN ALL_STAR als ON asp.AllStarID = als.AllStarID
            WHERE asp.PlayerID = ?
            ORDER BY asp.SelectionYear DESC
        """
        self.cursor.execute(query, (player_id,))
        return self.cursor.fetchall()
    
    
    def get_team_info(self, team_id: str) -> Optional[Tuple]:
        
        query = """
            SELECT TeamID, TeamName, City, ArenaName
            FROM TEAM
            WHERE TeamID = ?
        """
        self.cursor.execute(query, (team_id,))
        return self.cursor.fetchone()
    
    def get_all_teams(self) -> List[Tuple]:
        
        query = """
            SELECT TeamID, TeamName, City, ArenaName
            FROM TEAM
            ORDER BY TeamName
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def get_team_roster(self, team_id: str) -> List[Tuple]:
        
        query = """
            SELECT p.PlayerID, p.PlayerName, pt.position
            FROM PLAYER p
            JOIN PLAYER_TEAM pt ON p.PlayerID = pt.PlayerID
            WHERE pt.TeamID = ?
            ORDER BY p.PlayerName
        """
        self.cursor.execute(query, (team_id,))
        return self.cursor.fetchall()
    
    def get_team_wins_by_season(self, team_id: str, year: str) -> Optional[int]:
        
        query = """
            SELECT COUNT(g.GameID) as Wins
            FROM GAME g
            WHERE g.Winner = ? AND strftime('%Y', g.GameDate) = ?
        """
        self.cursor.execute(query, (team_id, year))
        result = self.cursor.fetchone()
        return result[0] if result else 0
    
    def get_team_games(self, team_id: str, year: str) -> List[Tuple]:
     
        query = """
            SELECT g.GameID, g.GameDate, 
                   ht.TeamName as HomeTeam, 
                   at.TeamName as AwayTeam, 
                   g.HomeScore, g.AwayScore, g.Winner
            FROM GAME g
            JOIN TEAM ht ON g.HomeTeamID = ht.TeamID
            JOIN TEAM at ON g.AwayTeamID = at.TeamID
            WHERE (g.HomeTeamID = ? OR g.AwayTeamID = ?) 
              AND strftime('%Y', g.GameDate) = ?
            ORDER BY g.GameDate
        """
        self.cursor.execute(query, (team_id, team_id, year))
        return self.cursor.fetchall()
    
    
    def get_top_scorers(self, season_id: str, limit: int = 10) -> List[Tuple]:
        
        query = """
            SELECT p.PlayerID, p.PlayerName, ps.Team, SUM(s.Points) as TotalPoints
            FROM PLAYER p
            JOIN STATISTICS s ON p.PlayerID = s.PlayerID
            JOIN PLAYER_SEASON ps ON p.PlayerID = ps.PlayerID AND s.SeasonID = ps.SeasonID
            WHERE ps.SeasonID = ?
            GROUP BY p.PlayerID, p.PlayerName, ps.Team
            ORDER BY TotalPoints DESC
            LIMIT ?
        """
        self.cursor.execute(query, (season_id, limit))
        return self.cursor.fetchall()
    
    def get_top_assisters(self, season_id: str, limit: int = 10) -> List[Tuple]:
       
        query = """
            SELECT p.PlayerID, p.PlayerName, ps.Team, SUM(s.Assist) as TotalAssists
            FROM PLAYER p
            JOIN STATISTICS s ON p.PlayerID = s.PlayerID
            JOIN PLAYER_SEASON ps ON p.PlayerID = ps.PlayerID AND s.SeasonID = ps.SeasonID
            WHERE ps.SeasonID = ?
            GROUP BY p.PlayerID, p.PlayerName, ps.Team
            ORDER BY TotalAssists DESC
            LIMIT ?
        """
        self.cursor.execute(query, (season_id, limit))
        return self.cursor.fetchall()
    
    def get_top_rebounders(self, season_id: str, limit: int = 10) -> List[Tuple]:
    
        query = """
            SELECT p.PlayerID, p.PlayerName, ps.Team, SUM(s.Rebounds) as TotalRebounds
            FROM PLAYER p
            JOIN STATISTICS s ON p.PlayerID = s.PlayerID
            JOIN PLAYER_SEASON ps ON p.PlayerID = ps.PlayerID AND s.SeasonID = ps.SeasonID
            WHERE ps.SeasonID = ?
            GROUP BY p.PlayerID, p.PlayerName, ps.Team
            ORDER BY TotalRebounds DESC
            LIMIT ?
        """
        self.cursor.execute(query, (season_id, limit))
        return self.cursor.fetchall()
    
    def get_season_standings(self, year: str) -> List[Tuple]:
       
        query = """
            SELECT t.TeamName, COUNT(g.GameID) as Wins
            FROM TEAM t
            JOIN GAME g ON t.TeamID = g.Winner
            WHERE strftime('%Y', g.GameDate) = ?
            GROUP BY t.TeamID, t.TeamName
            ORDER BY Wins DESC
        """
        self.cursor.execute(query, (year,))
        return self.cursor.fetchall()
    
    
    def get_draft_picks_by_year(self, year: int) -> List[Tuple]:
        
        query = """
            SELECT dp.OverallPick, p.PlayerName, p.PlayerID
            FROM DRAFT_PICK dp
            JOIN SEASON s ON dp.SeasonID = s.SeasonID
            JOIN PLAYER p ON dp.PlayerID = p.PlayerID
            WHERE s.YearStart = ?
            ORDER BY dp.OverallPick
        """
        self.cursor.execute(query, (year,))
        return self.cursor.fetchall()
    
    
    def get_allstar_by_year(self, year: int) -> List[Tuple]:
        
        query = """
            SELECT p.PlayerName, asp.Team
            FROM PLAYER p
            JOIN ALL_STAR_PLAYER asp ON p.PlayerID = asp.PlayerID
            WHERE asp.SelectionYear = ?
            ORDER BY p.PlayerName
        """
        self.cursor.execute(query, (year,))
        return self.cursor.fetchall()
    
    def get_allstar_winners(self) -> List[Tuple]:
        
        query = """
            SELECT als.AllStarID, t.TeamName, s.YearStart
            FROM ALL_STAR als
            JOIN TEAM t ON als.WinningTeam = t.TeamID
            JOIN SEASON s ON als.AllStarID = 'AS_' || s.SeasonID
            ORDER BY s.YearStart DESC
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    
    def trade_player(self, player_id: str, old_team: str, new_team: str) -> bool:
        """Trade a player from one team to another"""
        try:
           
            self.cursor.execute("""
                UPDATE PLAYER_TEAM
                SET Traded = 1
                WHERE PlayerID = ? AND TeamID = ?
            """, (player_id, old_team))
            
            
            self.cursor.execute("""
                INSERT OR IGNORE INTO PLAYER_TEAM (PlayerID, TeamID, Traded)
                VALUES (?, ?, 1)
            """, (player_id, new_team))
            
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error trading player: {e}")
            self.conn.rollback()
            return False
    
    def add_player_stats(self, player_id: str, season_id: str, team_id: str, 
                        points: int, rebounds: int, assists: int, 
                        steals: int, blocks: int) -> bool:
      
        try:
            stats_id = f"STATS_{player_id}_{season_id}_{datetime.now().timestamp()}"
            self.cursor.execute("""
                INSERT INTO STATISTICS 
                (StatsID, PlayerID, SeasonID, TeamID, Points, Rebounds, Assist, Steals, Blocks)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (stats_id, player_id, season_id, team_id, points, rebounds, assists, steals, blocks))
            
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error adding statistics: {e}")
            self.conn.rollback()
            return False
    
    def get_traded_players(self) -> List[Tuple]:
        
        query = """
            SELECT p.PlayerName, COUNT(pt.TeamID) as TeamsPlayedFor
            FROM PLAYER p
            JOIN PLAYER_TEAM pt ON p.PlayerID = pt.PlayerID
            WHERE pt.Traded = 1
            GROUP BY p.PlayerID, p.PlayerName
            HAVING TeamsPlayedFor > 1
            ORDER BY TeamsPlayedFor DESC, p.PlayerName
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()

