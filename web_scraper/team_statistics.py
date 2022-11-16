from web_scraper_helper import *


def scrape_team_stats_data(game_id):
    team_stats_url = f"https://www.espn.com/college-football/matchup?gameId={game_id}"
    soup = get_soup(team_stats_url)
    team_imgs = soup.find('table', {'class': 'mod-data'}).thead.findAll('img')
    if len(team_imgs) != 2:
        print(game_id)
        return []
    team_1_id = get_team_id_from_img(team_imgs[0])
    team_2_id = get_team_id_from_img(team_imgs[1])
    team_1 = {'game_id': game_id, 'team_id': team_1_id}
    team_2 = {'game_id': game_id, 'team_id': team_2_id}
    for tr in soup.find('table', {'class': 'mod-data'}).findAll('tr', {'class': ['highlight', 'indent']}):
        attribute = tr['data-stat-attr']
        stats = tr.findAll('td')
        if len(stats) != 3:
            continue
        team_1[attribute] = stats[1].getText().strip()
        team_2[attribute] = stats[2].getText().strip()
    return [team_1, team_2]