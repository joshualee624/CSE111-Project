from .NBADatabase import NBADatabase


class NBAApp:
    def __init__(self):
        self.db = NBADatabase()
        self.running = True
        # Simple in-memory auth state and credentials for protected actions
        self._auth_ok = False
        self._auth_user = "admin"
        self._auth_pass = "password"
    
    def clear_screen(self):
    
        print("\033c", end="")
    
    def print_header(self, title: str):
        
        print("=" * 70)
        print(f"  {title}")
        print("=" * 70)
    
    def print_separator(self):
        
        print("-" * 70)
    
    def display_main_menu(self):
        
        self.clear_screen()
        self.print_header("NBA DATABASE MANAGEMENT SYSTEM")
        print("\nPLAYER OPERATIONS")
        print("  1. Search Player by Name")
        print("  2. View Player Information")
        print("  3. View Player Career Statistics")
        print("  4. View Player Season Statistics")
        print("  5. View Player Awards")
        print("  6. View Player All-Star Selections")
        print("  7. View Players by Position")
        
        print("\n TEAM OPERATIONS")
        print("  8. View All Teams")
        print("  9. View Team Information")
        print(" 10. View Team Roster")
        print(" 11. View Team Season Record")
        print(" 12. View Team Games")
        
        print("\n STATISTICS & RANKINGS")
        print(" 13. Top Scorers by Season")
        print(" 14. Top Assist Leaders by Season")
        print(" 15. Top Rebounders by Season")
        print(" 16. Season Standings")
        
        print("\n DRAFT & ALL-STAR")
        print(" 17. View Draft Picks by Year")
        print(" 18. View All-Star Selections by Year")
        print(" 19. View All-Star Game Winners")
        
        print("\n DATABASE UPDATES")
        print(" 20. Trade Player")
        print(" 21. Add Player Statistics")
        print(" 22. View Traded Players")
        
        print("\n EXIT")
        print("  0. Exit Application")
        
        self.print_separator()


    def get_user_choice(self) -> str:
       
        return input("\nEnter your choice: ").strip()
    
    def wait_for_enter(self):
        
        input("\nPress Enter to continue...")
    
    def require_auth(self) -> bool:
        """
        Prompt for credentials before running protected operations.
        Stores the session in memory so the user doesn't have to re-enter
        credentials after a successful login.
        """
        if self._auth_ok:
            return True
        
        print("\n Administrator access required.")
        username = input("Username: ").strip()
        password = input("Password: ").strip()
        
        if username == self._auth_user and password == self._auth_pass:
            self._auth_ok = True
            print("\n Access granted.")
            return True
        
        print("\n Access denied. Returning to main menu.")
        self.wait_for_enter()
        return False
    
    
    def handle_search_player(self):
    
        self.print_header("SEARCH PLAYER BY NAME")
        name = input("Enter player name (or part of name): ").strip()
        
        if not name:
            print(" Please enter a name to search")
            self.wait_for_enter()
            return
        
        results = self.db.search_player_by_name(name)
        
        if not results:
            print(f"\n No players found matching '{name}'")
        else:
            print(f"\n✓ Found {len(results)} player(s):\n")
            print(f"{'ID':<12} {'Name':<25} {'Birth Date':<12} {'Height':<8} {'Weight'}")
            self.print_separator()
            for row in results:
                player_id, player_name, birth, height, weight = row
                print(f"{player_id:<12} {player_name:<25} {birth or 'N/A':<12} {height or 'N/A':<8} {weight or 'N/A'}")
        
        self.wait_for_enter()
    
    def handle_player_info(self):
        
        self.print_header("VIEW PLAYER INFORMATION")
        player_id = input("Enter Player ID: ").strip()
        
        result = self.db.get_player_info(player_id)
        
        if not result:
            print(f"\n No player found with ID: {player_id}")
        else:
            player_id, name, birth, height, weight = result
            print(f"\n Player Information:")
            print(f"  Player ID:   {player_id}")
            print(f"  Name:        {name}")
            print(f"  Birth Date:  {birth or 'N/A'}")
            print(f"  Height:      {height or 'N/A'} inches")
            print(f"  Weight:      {weight or 'N/A'} lbs")
        
        self.wait_for_enter()

    def handle_player_career_stats(self):
        
        self.print_header("VIEW PLAYER CAREER STATISTICS")
        player_id = input("Enter Player ID: ").strip()
        
        result = self.db.get_player_career_stats(player_id)
        
        if not result:
            print(f"\n No career statistics found for player: {player_id}")
        else:
            name, pts, reb, ast, stl, blk = result
            print(f"\n Career Statistics for {name}:")
            print(f"  Points:   {pts or 0:,}")
            print(f"  Rebounds: {reb or 0:,}")
            print(f"  Assists:  {ast or 0:,}")
            print(f"  Steals:   {stl or 0:,}")
            print(f"  Blocks:   {blk or 0:,}")
        
        self.wait_for_enter()

    def handle_player_season_stats(self):
    
        self.print_header("VIEW PLAYER SEASON STATISTICS")
        player_id = input("Enter Player ID: ").strip()
        season_id = input("Enter Season ID (e.g., 2023): ").strip()
        
        result = self.db.get_player_season_stats(player_id, season_id)
        
        if not result:
            print(f"\n No statistics found for player {player_id} in season {season_id}")
        else:
            name, team, pts, reb, ast, stl, blk = result
            print(f"\n {season_id} Season Statistics for {name}:")
            print(f"  Team:    {team or 'N/A'}")
            print(f"  Points:   {pts or 0:,}")
            print(f"  Rebounds: {reb or 0:,}")
            print(f"  Assists:  {ast or 0:,}")
            print(f"  Steals:   {stl or 0:,}")
            print(f"  Blocks:   {blk or 0:,}")
        
        self.wait_for_enter()
    
    def handle_player_awards(self):
    
        self.print_header("VIEW PLAYER AWARDS")
        player_id = input("Enter Player ID: ").strip()
        
        results = self.db.get_player_awards(player_id)
        
        if not results:
            print(f"\n No awards found for player: {player_id}")
        else:
            print(f"\n Awards for {player_id}:\n")
            print(f"{'Award Name':<40} {'Year'}")
            self.print_separator()
            for award_name, year in results:
                print(f"{award_name:<40} {year}")
        
        self.wait_for_enter()
    
    def handle_player_allstar(self):
    
        self.print_header("VIEW PLAYER ALL-STAR SELECTIONS")
        player_id = input("Enter Player ID: ").strip()
        
        results = self.db.get_player_allstar_selections(player_id)
        
        if not results:
            print(f"\n No All-Star selections found for player: {player_id}")
        else:
            print(f"\n All-Star Selections for {player_id}:\n")
            print(f"{'Year':<8} {'Team':<8} {'Winning Team'}")
            self.print_separator()
            for year, team, winner in results:
                print(f"{year:<8} {team:<8} {winner or 'N/A'}")
        
        self.wait_for_enter()
    
    def handle_players_by_position(self):
        
        self.print_header("VIEW PLAYERS BY POSITION")
        print("Positions: PG (Point Guard), SG (Shooting Guard), SF (Small Forward),")
        print("           PF (Power Forward), C (Center)")
        position = input("\nEnter Position: ").strip().upper()
        
        results = self.db.get_players_by_position(position)
        
        if not results:
            print(f"\n No players found for position: {position}")
        else:
            print(f"\n Found {len(results)} player(s) at position {position}:\n")
            print(f"{'ID':<12} {'Name':<25} {'Position':<10} {'Team'}")
            self.print_separator()
            for player_id, name, pos, team in results:
                print(f"{player_id:<12} {name:<25} {pos:<10} {team}")
        
        self.wait_for_enter()
    
    def handle_all_teams(self):
        
        self.print_header("ALL NBA TEAMS")
        results = self.db.get_all_teams()
        
        if not results:
            print("\n No teams found")
        else:
            print(f"\n Total Teams: {len(results)}\n")
            print(f"{'ID':<6} {'Team Name':<25} {'City':<20} {'Arena'}")
            self.print_separator()
            for team_id, name, city, arena in results:
                print(f"{team_id:<6} {name:<25} {city or 'N/A':<20} {arena or 'N/A'}")
        
        self.wait_for_enter()
    
    def handle_team_info(self):
        
        self.print_header("VIEW TEAM INFORMATION")
        team_id = input("Enter Team ID (e.g., LAL, GSW): ").strip().upper()
        
        result = self.db.get_team_info(team_id)
        
        if not result:
            print(f"\n No team found with ID: {team_id}")
        else:
            team_id, name, city, arena = result
            print(f"\n Team Information:")
            print(f"  Team ID:     {team_id}")
            print(f"  Team Name:   {name}")
            print(f"  City:        {city or 'N/A'}")
            print(f"  Arena:       {arena or 'N/A'}")
        
        self.wait_for_enter()
    
    def handle_team_roster(self):
       
        self.print_header("VIEW TEAM ROSTER")
        team_id = input("Enter Team ID: ").strip().upper()
        
        results = self.db.get_team_roster(team_id)
        
        if not results:
            print(f"\n No players found for team: {team_id}")
        else:
            print(f"\n Roster for {team_id} ({len(results)} players):\n")
            print(f"{'ID':<12} {'Name':<30} {'Position'}")
            self.print_separator()
            for player_id, name, position in results:
                print(f"{player_id:<12} {name:<30} {position or 'N/A'}")
        
        self.wait_for_enter()
    
    def handle_team_record(self):
        
        self.print_header("VIEW TEAM SEASON RECORD")
        team_id = input("Enter Team ID: ").strip().upper()
        year = input("Enter Year (e.g., 2023): ").strip()
        
        wins = self.db.get_team_wins_by_season(team_id, year)
        
        print(f"\n✓ {team_id} had {wins} win(s) in {year}")
        
        self.wait_for_enter()
    
    def handle_team_games(self):
        
        self.print_header("VIEW TEAM GAMES")
        team_id = input("Enter Team ID: ").strip().upper()
        year = input("Enter Year (e.g., 2023): ").strip()
        
        results = self.db.get_team_games(team_id, year)
        
        if not results:
            print(f"\n No games found for {team_id} in {year}")
        else:
            print(f"\n Games for {team_id} in {year} ({len(results)} games):\n")
            print(f"{'Date':<12} {'Home Team':<20} {'Away Team':<20} {'Score':<12} {'Winner'}")
            self.print_separator()
            for game_id, date, home, away, home_score, away_score, winner in results:
                score = f"{home_score}-{away_score}" if home_score and away_score else "N/A"
                print(f"{date[:10]:<12} {home:<20} {away:<20} {score:<12} {winner or 'N/A'}")
        
        self.wait_for_enter()

    def handle_top_scorers(self):
       
        self.print_header("TOP SCORERS BY SEASON")
        season_id = input("Enter Season ID (e.g., 2023): ").strip()
        limit = input("Enter number of players to display (default 10): ").strip()
        limit = int(limit) if limit.isdigit() else 10
        
        results = self.db.get_top_scorers(season_id, limit)
        
        if not results:
            print(f"\n No statistics found for season: {season_id}")
        else:
            print(f"\n Top {len(results)} Scorers in {season_id}:\n")
            print(f"{'Rank':<6} {'ID':<12} {'Name':<25} {'Team':<6} {'Points'}")
            self.print_separator()
            for i, (player_id, name, team, pts) in enumerate(results, 1):
                print(f"{i:<6} {player_id:<12} {name:<25} {team or 'N/A':<6} {pts:,}")
        
        self.wait_for_enter()
    
    def handle_top_assisters(self):
        
        self.print_header("TOP ASSIST LEADERS BY SEASON")
        season_id = input("Enter Season ID (e.g., 2023): ").strip()
        limit = input("Enter number of players to display (default 10): ").strip()
        limit = int(limit) if limit.isdigit() else 10
        
        results = self.db.get_top_assisters(season_id, limit)
        
        if not results:
            print(f"\n No statistics found for season: {season_id}")
        else:
            print(f"\n Top {len(results)} Assist Leaders in {season_id}:\n")
            print(f"{'Rank':<6} {'ID':<12} {'Name':<25} {'Team':<6} {'Assists'}")
            self.print_separator()
            for i, (player_id, name, team, ast) in enumerate(results, 1):
                print(f"{i:<6} {player_id:<12} {name:<25} {team or 'N/A':<6} {ast:,}")
        
        self.wait_for_enter()
    
    def handle_top_rebounders(self):
        
        self.print_header("TOP REBOUNDERS BY SEASON")
        season_id = input("Enter Season ID (e.g., 2023): ").strip()
        limit = input("Enter number of players to display (default 10): ").strip()
        limit = int(limit) if limit.isdigit() else 10
        
        results = self.db.get_top_rebounders(season_id, limit)
        
        if not results:
            print(f"\n No statistics found for season: {season_id}")
        else:
            print(f"\n Top {len(results)} Rebounders in {season_id}:\n")
            print(f"{'Rank':<6} {'ID':<12} {'Name':<25} {'Team':<6} {'Rebounds'}")
            self.print_separator()
            for i, (player_id, name, team, reb) in enumerate(results, 1):
                print(f"{i:<6} {player_id:<12} {name:<25} {team or 'N/A':<6} {reb:,}")
        
        self.wait_for_enter()
    
    def handle_season_standings(self):
    
        self.print_header("SEASON STANDINGS")
        year = input("Enter Year (e.g., 2023): ").strip()
        
        results = self.db.get_season_standings(year)
        
        if not results:
            print(f"\n No standings found for year: {year}")
        else:
            print(f"\n {year} Season Standings:\n")
            print(f"{'Rank':<6} {'Team Name':<30} {'Wins'}")
            self.print_separator()
            for i, (team_name, wins) in enumerate(results, 1):
                print(f"{i:<6} {team_name:<30} {wins}")
        
        self.wait_for_enter()
    
    def handle_draft_picks(self):
       
        self.print_header("VIEW DRAFT PICKS BY YEAR")
        year = input("Enter Draft Year (e.g., 2023): ").strip()
        
        if not year.isdigit():
            print("\n Please enter a valid year")
            self.wait_for_enter()
            return
        
        results = self.db.get_draft_picks_by_year(int(year))
        
        if not results:
            print(f"\n No draft picks found for year: {year}")
        else:
            print(f"\n Draft Picks for {year} ({len(results)} picks):\n")
            print(f"{'Pick #':<8} {'Player Name':<30} {'Player ID'}")
            self.print_separator()
            for pick, name, player_id in results:
                print(f"{pick:<8} {name:<30} {player_id}")
        
        self.wait_for_enter()
    
    def handle_allstar_by_year(self):
        
        self.print_header("VIEW ALL-STAR SELECTIONS BY YEAR")
        year = input("Enter Year (e.g., 2023): ").strip()
        
        if not year.isdigit():
            print("\n Please enter a valid year")
            self.wait_for_enter()
            return
        
        results = self.db.get_allstar_by_year(int(year))
        
        if not results:
            print(f"\n No All-Star selections found for year: {year}")
        else:
            print(f"\n All-Star Selections for {year} ({len(results)} players):\n")
            print(f"{'Player Name':<35} {'Team'}")
            self.print_separator()
            for name, team in results:
                print(f"{name:<35} {team or 'N/A'}")
        
        self.wait_for_enter()
    
    def handle_allstar_winners(self):
       
        self.print_header("ALL-STAR GAME WINNERS")
        results = self.db.get_allstar_winners()
        
        if not results:
            print("\n No All-Star game winners found")
        else:
            print(f"\n✓ All-Star Game Winners ({len(results)} games):\n")
            print(f"{'All-Star ID':<15} {'Winning Team':<30} {'Year'}")
            self.print_separator()
            for allstar_id, team, year in results:
                print(f"{allstar_id:<15} {team:<30} {year}")
        
        self.wait_for_enter()
    
    def handle_trade_player(self):
        
        if not self.require_auth():
            return
        
        self.print_header("TRADE PLAYER")
        player_id = input("Enter Player ID: ").strip()
        old_team = input("Enter Current Team ID: ").strip().upper()
        new_team = input("Enter New Team ID: ").strip().upper()
        
        confirm = input(f"\nConfirm trade of {player_id} from {old_team} to {new_team}? (y/n): ").strip().lower()
        
        if confirm == 'y':
            if self.db.trade_player(player_id, old_team, new_team):
                print(f"\n Successfully traded {player_id} from {old_team} to {new_team}")
            else:
                print("\n Failed to trade player")
        else:
            print("\n Trade cancelled")
        
        self.wait_for_enter()
    
    def handle_add_stats(self):
        
        if not self.require_auth():
            return
        
        self.print_header("ADD PLAYER STATISTICS")
        player_id = input("Enter Player ID: ").strip()
        season_id = input("Enter Season ID: ").strip()
        team_id = input("Enter Team ID: ").strip().upper()
        
        try:
            points = int(input("Enter Points: ").strip())
            rebounds = int(input("Enter Rebounds: ").strip())
            assists = int(input("Enter Assists: ").strip())
            steals = int(input("Enter Steals: ").strip())
            blocks = int(input("Enter Blocks: ").strip())
            
            if self.db.add_player_stats(player_id, season_id, team_id, points, rebounds, assists, steals, blocks):
                print(f"\n Successfully added statistics for {player_id}")
            else:
                print("\n Failed to add statistics")
        except ValueError:
            print("\n Invalid input. Please enter numbers for statistics.")
        
        self.wait_for_enter()
    
    def handle_traded_players(self):
        
        self.print_header("VIEW TRADED PLAYERS")
        results = self.db.get_traded_players()
        
        if not results:
            print("\n No traded players found")
        else:
            print(f"\n Players with Multiple Teams ({len(results)} players):\n")
            print(f"{'Player Name':<35} {'# of Teams'}")
            self.print_separator()
            for name, teams in results:
                print(f"{name:<35} {teams}")
        
        self.wait_for_enter()
    
    def run(self):
        
        while self.running:
            self.display_main_menu()
            choice = self.get_user_choice()
            
            if choice == '0':
                self.running = False
                print("\n Thank you for using the NBA Database System!")
            elif choice == '1':
                self.handle_search_player()
            elif choice == '2':
                self.handle_player_info()
            elif choice == '3':
                self.handle_player_career_stats()
            elif choice == '4':
                self.handle_player_season_stats()
            elif choice == '5':
                self.handle_player_awards()
            elif choice == '6':
                self.handle_player_allstar()
            elif choice == '7':
                self.handle_players_by_position()
            elif choice == '8':
                self.handle_all_teams()
            elif choice == '9':
                self.handle_team_info()
            elif choice == '10':
                self.handle_team_roster()
            elif choice == '11':
                self.handle_team_record()
            elif choice == '12':
                self.handle_team_games()
            elif choice == '13':
                self.handle_top_scorers()
            elif choice == '14':
                self.handle_top_assisters()
            elif choice == '15':
                self.handle_top_rebounders()
            elif choice == '16':
                self.handle_season_standings()
            elif choice == '17':
                self.handle_draft_picks()
            elif choice == '18':
                self.handle_allstar_by_year()
            elif choice == '19':
                self.handle_allstar_winners()
            elif choice == '20':
                self.handle_trade_player()
            elif choice == '21':
                self.handle_add_stats()
            elif choice == '22':
                self.handle_traded_players()
            else:
                print("\n Invalid choice. Please try again.")
                self.wait_for_enter()
        
        self.db.close()

