from gamecast import *
from drives import *
from team_statistics import *
from file_generator import *
from pathlib import Path

if __name__ == '__main__':
    base_filepath = '/Users/ebrunt/Desktop/ncaa-data/'
    years = [2022]
    weeks = [9, 10]
    teams = {}
    game_data = []
    scoreboard_data = []
    team_stats = []
    drive_data = []
    for year in years:
        for week in weeks:
            game_ids = get_game_ids(year, week)
            for game_id in game_ids:
                game_info = scrape_gamecast_information(year, week, game_id)
                if game_info['game']['status'] != 'Final':
                    continue
                game_stats = scrape_team_stats_data(game_id)
                drives = scrape_drive_data(game_id)
                if game_info['home_team']['team_id'] not in teams.keys():
                    teams[game_info['home_team']['team_id']] = game_info['home_team']
                if game_info['away_team']['team_id'] not in teams.keys():
                    teams[game_info['away_team']['team_id']] = game_info['away_team']
                game_data.append(game_info['game'])
                scoreboard_data.append(game_info['away_scoreboard'])
                scoreboard_data.append(game_info['home_scoreboard'])
                team_stats.extend(game_stats)
                drive_data.extend(drives)

            path = base_filepath + f'/{year}/{week}/'
            Path(path).mkdir(parents=True, exist_ok=True)
            for data, filename in [(team_stats, 'team-stats.json'), (drive_data, 'drives.json'),
                                   (teams, 'teams.json'), (scoreboard_data, 'scoreboards.json'),
                                   (game_data, 'games.json')]:
                if type(data) == dict:
                    add_list_to_file(data.values(), path + filename)
                else:
                    add_list_to_file(data, path + filename)
                data.clear()


