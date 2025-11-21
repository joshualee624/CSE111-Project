-- Use Case 1: Update Queries for Player Trades

-- 1. Update a player's team in PLAYER_TEAM table (mark as traded and update team)
-- Example: LeBron James traded from CLE to LAL
UPDATE PLAYER_TEAM
SET TeamID = 'LAL', Traded = 1
WHERE PlayerID = 'jamesle01' AND TeamID = 'CLE';

-- Show the updated record
SELECT PlayerID, TeamID, position, Traded
FROM PLAYER_TEAM
WHERE PlayerID = 'jamesle01' AND TeamID = 'CLE';

-- 2. Insert new PLAYER_SEASON record for the traded player in the new season
-- Example: LeBron James joining LAL for 2018-19 season
INSERT OR REPLACE INTO PLAYER_SEASON (PlayerID, SeasonID, Team, Age, Experience, position)
VALUES ('jamesle01', '2019', 'CLE', 34, 16, 'SF');

-- Show the new season record
SELECT PlayerID, SeasonID, Team, Age, Experience, position
FROM PLAYER_SEASON
WHERE PlayerID = 'jamesle01' AND SeasonID = '2019';

-- 3. Update PLAYER_SEASON to reflect the trade (change team mid-season)
-- Example: Update James Harden's team mid-season from BKN to PHI
UPDATE PLAYER_SEASON
SET Team = 'PHI'
WHERE PlayerID = 'hardeja01' AND SeasonID = '2022';

-- Show the updated team assignment
SELECT PlayerID, SeasonID, Team, Age, Experience, position
FROM PLAYER_SEASON
WHERE PlayerID = 'hardeja01' AND SeasonID = '2022';

-- 4. Add a new PLAYER_TEAM relationship for the traded player
-- Example: Add Kevin Durant to PHX after trade from BKN
INSERT INTO PLAYER_TEAM (PlayerID, TeamID, position, Traded)
VALUES ('duranke01', 'PHX', 'PF', 1);

-- Show all teams Kevin Durant has played for
SELECT PlayerID, TeamID, position, Traded
FROM PLAYER_TEAM
WHERE PlayerID = 'duranke01';

-- 5. Update STATISTICS to associate with new team (create new stats record)
-- Example: Create new stats record for Anthony Davis with LAL
INSERT INTO STATISTICS (StatsID, PlayerID, SeasonID, TeamID, Points, Rebounds, Assist, Steals, Blocks)
VALUES ('STATS_davisan02_2020', 'davisan02', '2020', 'LAL', 26, 9, 3, 1, 2);

-- Show the new statistics record
SELECT StatsID, PlayerID, Points, Rebounds, Assist, Steals, Blocks
FROM STATISTICS
WHERE StatsID = 'STATS_davisan02_2020';