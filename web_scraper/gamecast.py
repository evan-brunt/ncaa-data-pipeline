from web_scraper_helper import *


def get_team_scores(soup, index):
    scoreboard = []
    for column in soup.find('table', {'class': 'miniTable'}).findAll("tr")[index].findAll('td'):
        scoreboard.append(column.getText())
    return scoreboard


def get_team_id(soup, class_name):
    team_div = soup.find('div', {'class': class_name})
    team_id = get_team_id_from_soup(team_div)
    return team_id


def scrape_team_information(soup, class_name):
    team_div = soup.find('div', {'class': class_name})
    team_id = get_team_id_from_soup(team_div)
    team = {'long_name': team_div.find('span', {'class': 'long-name'}).getText(),
            'short_name': team_div.find('span', {'class': 'short-name'}).getText(),
            'abbrev': team_div.find('span', {'class': 'abbrev'}).getText()}
    conference_info = get_conference_information(team_id).split(' - ')
    team['conference'] = conference_info[0]
    team['division'] = conference_info[1] if len(conference_info) == 2 else None
    team['team_id'] = team_id
    return team


def scrape_quarter_scores(soup, game_id, class_name):
    if class_name == 'team away':
        index = 1
    else:
        index = 2
    team_id = get_team_id_from_soup(soup.find('div', {'class': class_name}))
    scoreboard = get_team_scores(soup, index)
    return {'game_id': game_id, 'team_id': team_id, 'first_quarter': scoreboard[1],
            'second_quarter': scoreboard[2], 'third_quarter': scoreboard[3],
            'fourth_quarter': scoreboard[4], 'total': scoreboard[-1],
            'overtime': scoreboard[-2] if len(scoreboard) == 7 else None}


def scrape_gamecast_information(year, week, game_id):
    gamecast = f"https://www.espn.com/college-football/game/_/gameId/{game_id}"
    away_class = 'team away'
    home_class = 'team home'
    soup = get_soup(gamecast)
    date = soup.find('div', {'class': 'game-date-time'}).span['data-date']
    status = soup.find('span', {'class': 'game-time status-detail'}).getText()
    away_team = scrape_team_information(soup, away_class)
    home_team = scrape_team_information(soup, home_class)
    if status == 'Final':
        away_scoreboard = scrape_quarter_scores(soup, game_id, away_class)
        home_scoreboard = scrape_quarter_scores(soup, game_id, home_class)
    else:
        away_scoreboard = {}
        home_scoreboard = {}
    return {
        'game': {'year': year, 'week': week, 'game_id': game_id, 'away_team_id': away_team['team_id'],
                 'home_team_id': home_team['team_id'], 'date': date, 'status': status},
        'away_scoreboard': away_scoreboard,
        'home_scoreboard': home_scoreboard,
        'away_team': away_team,
        'home_team': home_team
    }
