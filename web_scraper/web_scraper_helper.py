import requests
import re
from bs4 import BeautifulSoup


def get_team_id_from_soup(soup):
    return int(soup.find('a')['href'].split('/')[-2])


def get_team_id_from_img(img):
    return img['src'].split('/')[-1].split('.')[0]


def get_soup(url):
    html = requests.get(url)
    html_parser = 'html.parser'
    return BeautifulSoup(html.content, html_parser)


def get_game_ids(year, week):
    scoreboard = f"https://www.espn.com/college-football/scoreboard/_/week/{week}/year/{year}/seasontype/2/group/80"
    game_url = "/college-football/game/_/gameId/"
    soup = get_soup(scoreboard)
    game_ids = set()
    for link in soup.findAll('a', href=re.compile(game_url)):
        game_ids.add(link['href'].split('/')[-1])
    return game_ids


def get_conference_information(team_id):
    team_url = f"https://www.espn.com/college-football/team/_/id/{team_id}"
    soup = get_soup(team_url)
    class_name = "list flex ClubhouseHeader__Record n8 ml4"
    conference = soup.find('ul', {'class': class_name})
    if conference is None:
        return ""
    if len(conference.contents) == 1:
        return "FBS Independent"
    return conference.contents[1].getText().split(' in ')[1]
