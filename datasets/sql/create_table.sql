-- Enable foreign key constraints
PRAGMA foreign_keys = ON;

-- PLAYER table (central entity)
CREATE TABLE IF NOT EXISTS PLAYER (
    PlayerID TEXT PRIMARY KEY,
    PlayerName TEXT NOT NULL,
    BornDate TEXT,
    Height INTEGER,
    Weight INTEGER
);

-- TEAM table
CREATE TABLE IF NOT EXISTS TEAM (
    TeamID TEXT PRIMARY KEY,
    TeamName TEXT NOT NULL,
    City TEXT,
    ArenaName TEXT
);

-- SEASON table
CREATE TABLE IF NOT EXISTS SEASON (
    SeasonID TEXT PRIMARY KEY,
    YearStart INTEGER,
    YearEnd INTEGER,
    SeasonTeam TEXT
);

-- AWARD table
CREATE TABLE IF NOT EXISTS AWARD (
    AwardID TEXT PRIMARY KEY,
    AwardName TEXT NOT NULL
);

-- ALL_STAR table (stores All-Star game information)
CREATE TABLE IF NOT EXISTS ALL_STAR (
    AllStarID TEXT PRIMARY KEY,
    WinningTeam TEXT,
    FOREIGN KEY (WinningTeam) REFERENCES TEAM(TeamID)
);

-- GAME table
CREATE TABLE IF NOT EXISTS GAME (
    GameID TEXT PRIMARY KEY,
    GameDate TEXT,
    HomeTeamID TEXT,
    AwayTeamID TEXT,
    HomeScore INTEGER,
    AwayScore INTEGER,
    Winner TEXT,
    FOREIGN KEY (HomeTeamID) REFERENCES TEAM(TeamID),
    FOREIGN KEY (AwayTeamID) REFERENCES TEAM(TeamID)
);

-- STATISTICS table (has stats relationship with PLAYER)
CREATE TABLE IF NOT EXISTS STATISTICS (
    StatsID TEXT PRIMARY KEY,
    PlayerID TEXT NOT NULL,
    SeasonID TEXT NOT NULL,
    TeamID TEXT NOT NULL,
    Points INTEGER,
    Rebounds INTEGER,
    Assist INTEGER,
    Steals INTEGER,
    Blocks INTEGER,
    FOREIGN KEY (PlayerID) REFERENCES PLAYER(PlayerID),
    FOREIGN KEY (TeamID) REFERENCES TEAM(TeamID)
);

-- PLAYER_TEAM junction table (plays for relationship)
CREATE TABLE IF NOT EXISTS PLAYER_TEAM (
    PlayerID TEXT NOT NULL,
    TeamID TEXT NOT NULL,
    position TEXT,
    Traded INTEGER DEFAULT 0,
    PRIMARY KEY (PlayerID, TeamID),
    FOREIGN KEY (PlayerID) REFERENCES PLAYER(PlayerID),
    FOREIGN KEY (TeamID) REFERENCES TEAM(TeamID)
);

-- PLAYER_SEASON junction table (plays season relationship)
CREATE TABLE IF NOT EXISTS PLAYER_SEASON (
    PlayerID TEXT NOT NULL,
    SeasonID TEXT NOT NULL,
    Team TEXT,
    Age INTEGER,
    Experience INTEGER,
    position TEXT,
    PRIMARY KEY (PlayerID, SeasonID),
    FOREIGN KEY (PlayerID) REFERENCES PLAYER(PlayerID),
    FOREIGN KEY (SeasonID) REFERENCES SEASON(SeasonID)
);

-- DRAFT_PICK table (includes Draft Pick relationship with SEASON)
CREATE TABLE IF NOT EXISTS DRAFT_PICK (
    DraftPickID TEXT PRIMARY KEY,
    SeasonID TEXT NOT NULL,
    OverallPick INTEGER,
    PlayerID TEXT,
    FOREIGN KEY (SeasonID) REFERENCES SEASON(SeasonID),
    FOREIGN KEY (PlayerID) REFERENCES PLAYER(PlayerID)
);

-- ALL_STAR_PLAYER junction table (Selected for relationship)
CREATE TABLE IF NOT EXISTS ALL_STAR_PLAYER (
    AllStarID TEXT NOT NULL,
    PlayerID TEXT NOT NULL,
    SelectionYear INTEGER,
    Team TEXT,
    PRIMARY KEY (AllStarID, PlayerID),
    FOREIGN KEY (AllStarID) REFERENCES ALL_STAR(AllStarID),
    FOREIGN KEY (PlayerID) REFERENCES PLAYER(PlayerID)
);

-- PLAYERAWARD junction table (awarded relationship)
CREATE TABLE IF NOT EXISTS PLAYER_AWARD (
    AwardID TEXT NOT NULL,
    PlayerID TEXT NOT NULL,
    AwardYear INTEGER,
    PRIMARY KEY (AwardID, PlayerID, AwardYear),
    FOREIGN KEY (AwardID) REFERENCES AWARD(AwardID),
    FOREIGN KEY (PlayerID) REFERENCES PLAYER(PlayerID)
);

-- Additional indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_player_team_player ON PLAYER_TEAM(PlayerID);
CREATE INDEX IF NOT EXISTS idx_player_team_team ON PLAYER_TEAM(TeamID);
CREATE INDEX IF NOT EXISTS idx_player_season_player ON PLAYER_SEASON(PlayerID);
CREATE INDEX IF NOT EXISTS idx_player_season_season ON PLAYER_SEASON(SeasonID);
CREATE INDEX IF NOT EXISTS idx_statistics_player ON STATISTICS(PlayerID);
CREATE INDEX IF NOT EXISTS idx_draft_season ON DRAFT_PICK(SeasonID);
CREATE INDEX IF NOT EXISTS idx_allstar_player ON ALL_STAR_PLAYER(PlayerID);
CREATE INDEX IF NOT EXISTS idx_playeraward_player ON PLAYER_AWARD(PlayerID);
