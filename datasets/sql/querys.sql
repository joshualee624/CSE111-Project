-- 30 SQL Queries based on the NBA Stats Database Schema
-- Use Case 1: Update Player Roster Mid-Season (Administrator functionality for trades)
-- Use Case 2: View information based on specific actions (User queries for stats, awards, etc.)

-- Use Case 1: Update Queries for Player Trades

-- 1. Update a player's team in PLAYER_TEAM table (mark as traded and update team)
UPDATE PLAYER_TEAM
SET TeamID = 'NEW_TEAM_ID', Traded = 1
WHERE PlayerID = 'PLAYER_ID' AND TeamID = 'OLD_TEAM_ID';

-- 2. Insert new PLAYER_SEASON record for the traded player in the new season
INSERT INTO PLAYER_SEASON (PlayerID, SeasonID, Team, Age, Experience, position)
VALUES ('PLAYER_ID', 'SEASON_ID', 'NEW_TEAM_ID', 25, 5, 'POSITION');

-- 3. Update PLAYER_SEASON to reflect the trade (change team mid-season)
UPDATE PLAYER_SEASON
SET Team = 'NEW_TEAM_ID'
WHERE PlayerID = 'PLAYER_ID' AND SeasonID = 'SEASON_ID';

-- 4. Add a new PLAYER_TEAM relationship for the traded player
INSERT INTO PLAYER_TEAM (PlayerID, TeamID, position, Traded)
VALUES ('PLAYER_ID', 'NEW_TEAM_ID', 'POSITION', 1);

-- 5. Update STATISTICS to associate with new team (create new stats record)
INSERT INTO STATISTICS (StatsID, PlayerID, Points, Rebounds, Assist, Steals, Blocks)
VALUES ('NEW_STATS_ID', 'PLAYER_ID', 20, 10, 5, 2, 1);

-- Use Case 2: Select Queries for Viewing Information

-- 6. Get basic player information
SELECT PlayerID, PlayerName, BornDate, Height, Weight
FROM PLAYER
WHERE PlayerID = 'jamesle01';

-- 7. Get all players on a specific team
SELECT p.PlayerName, pt.position
FROM PLAYER p
JOIN PLAYER_TEAM pt ON p.PlayerID = pt.PlayerID
WHERE pt.TeamID = 'ATL';

-- 8. Get player statistics for a specific season
SELECT s.Points, s.Rebounds, s.Assist, s.Steals, s.Blocks
FROM STATISTICS s
JOIN PLAYER_SEASON ps ON s.PlayerID = ps.PlayerID AND s.SeasonID = ps.SeasonID
WHERE ps.PlayerID = 'jamesle01' AND ps.SeasonID = '2023';;

-- 9. Get all awards won by a player
SELECT a.AwardName, pa.AwardYear
FROM AWARD a
JOIN PLAYERAWARD pa ON a.AwardID = pa.AwardID
WHERE pa.PlayerID = 'jamesle01'
ORDER BY pa.AwardYear DESC;

-- 10. Get All-Star selections for a player
SELECT asp.SelectionYear, asp.Team, als.WinningTeam
FROM ALL_STAR_PLAYER asp
JOIN ALL_STAR als ON asp.AllStarID = als.AllStarID
WHERE asp.PlayerID = 'jamesle01'
ORDER BY asp.SelectionYear DESC;

-- 11. Get team information
SELECT TeamID, TeamName, City, ArenaName
FROM TEAM
WHERE TeamID = 'ATL';

-- 12. Get games played by a team in a season
SELECT g.GameID, g.GameDate, g.HomeTeamID, g.AwayTeamID, g.HomeScore, g.AwayScore, g.Winner
FROM GAME g
WHERE (g.HomeTeamID = 'ATL' OR g.AwayTeamID = 'ATL')
  AND strftime('%Y', g.GameDate) = '2023'
ORDER BY g.GameDate;

-- 13. Get top scorers in a season
SELECT p.PlayerName, SUM(s.Points) as TotalPoints
FROM PLAYER p
JOIN STATISTICS s ON p.PlayerID = s.PlayerID
JOIN PLAYER_SEASON ps ON p.PlayerID = ps.PlayerID AND s.SeasonID = ps.SeasonID
WHERE ps.SeasonID = '2023'
GROUP BY p.PlayerID, p.PlayerName
ORDER BY TotalPoints DESC
LIMIT 10;

-- 14. Get players who have been traded
SELECT p.PlayerName, COUNT(pt.TeamID) as TeamsPlayedFor
FROM PLAYER p
JOIN PLAYER_TEAM pt ON p.PlayerID = pt.PlayerID
WHERE pt.Traded = 1
GROUP BY p.PlayerID, p.PlayerName
HAVING TeamsPlayedFor > 1;

-- 15. Get draft picks for a specific year
SELECT dp.DraftPickID, dp.OverallPick, s.YearStart
FROM DRAFT_PICK dp
JOIN SEASON s ON dp.SeasonID = s.SeasonID
WHERE s.YearStart = 2023;

-- 16. Get all players drafted in a specific year
SELECT p.PlayerName, dp.OverallPick
FROM PLAYER p
JOIN DRAFT_PICK dp ON p.PlayerID = dp.PlayerID
JOIN SEASON s ON dp.SeasonID = s.SeasonID
WHERE s.YearStart = 2023
ORDER BY dp.OverallPick;

-- 17. Get season information
SELECT SeasonID, YearStart, YearEnd
FROM SEASON
WHERE SeasonID = '2023';

-- 18. Get player age and experience for a season
SELECT p.PlayerName, ps.Age, ps.Experience
FROM PLAYER p
JOIN PLAYER_SEASON ps ON p.PlayerID = ps.PlayerID
WHERE ps.SeasonID = '2023';

-- 19. Get awards from last year
SELECT a.AwardName, p.PlayerName, pa.AwardYear
FROM AWARD a
JOIN PLAYERAWARD pa ON a.AwardID = pa.AwardID
JOIN PLAYER p ON pa.PlayerID = p.PlayerID
WHERE pa.AwardYear = 2024
ORDER BY a.AwardName;

-- 20. Get All-Star game winners
SELECT als.AllStarID, t.TeamName, s.YearStart
FROM ALL_STAR als
JOIN TEAM t ON als.WinningTeam = t.TeamID
JOIN SEASON s ON als.AllStarID = 'AS_' || s.SeasonID
ORDER BY s.YearStart DESC;

-- 21. Get player with most assists in a season
SELECT p.PlayerName, SUM(s.Assist) as TotalAssists
FROM PLAYER p
JOIN STATISTICS s ON p.PlayerID = s.PlayerID
JOIN PLAYER_SEASON ps ON p.PlayerID = ps.PlayerID AND s.SeasonID = ps.SeasonID
WHERE ps.SeasonID = '2023'
GROUP BY p.PlayerID, p.PlayerName
ORDER BY TotalAssists DESC
LIMIT 1;

-- 22. Get teams with most wins in a season
SELECT t.TeamName, COUNT(g.GameID) as Wins
FROM TEAM t
JOIN GAME g ON t.TeamID = g.Winner
WHERE strftime('%Y', g.GameDate) = '2023'
GROUP BY t.TeamID, t.TeamName
ORDER BY Wins DESC;

-- 23. Get player career totals
SELECT p.PlayerName, SUM(s.Points) as CareerPoints, SUM(s.Rebounds) as CareerRebounds, SUM(s.Assist) as CareerAssists
FROM PLAYER p
JOIN STATISTICS s ON p.PlayerID = s.PlayerID
GROUP BY p.PlayerID, p.PlayerName;

-- 24. Get players by position
SELECT p.PlayerName, pt.position
FROM PLAYER p
JOIN PLAYER_TEAM pt ON p.PlayerID = pt.PlayerID
WHERE pt.position = 'PG';

-- 25. Get games on a specific date
SELECT g.GameID, ht.TeamName as HomeTeam, at.TeamName as AwayTeam, g.HomeScore, g.AwayScore
FROM GAME g
JOIN TEAM ht ON g.HomeTeamID = ht.TeamID
JOIN TEAM at ON g.AwayTeamID = at.TeamID
WHERE g.GameDate LIKE '2023-04-09%';

-- 26. Get player height and weight
SELECT PlayerName, Height, Weight
FROM PLAYER
WHERE PlayerID = 'jamesle01';

-- 27. Get seasons a player played
SELECT DISTINCT s.SeasonID, s.YearStart, s.YearEnd
FROM SEASON s
JOIN PLAYER_SEASON ps ON s.SeasonID = ps.SeasonID
WHERE ps.PlayerID = 'jamesle01'
ORDER BY s.YearStart;

-- 28. Get all awards available
SELECT AwardID, AwardName
FROM AWARD
ORDER BY AwardName;

-- 29. Get players selected for All-Star in a year
SELECT p.PlayerName, asp.Team
FROM PLAYER p
JOIN ALL_STAR_PLAYER asp ON p.PlayerID = asp.PlayerID
WHERE asp.SelectionYear = 2023;

-- 30. Get team arena information
SELECT TeamName, ArenaName
FROM TEAM
WHERE TeamID = 'ATL';
