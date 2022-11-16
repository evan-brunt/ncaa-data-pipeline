from web_scraper_helper import *


def scrape_drive_data(game_id):
    plays = f"https://www.espn.com/college-football/playbyplay/_/gameId/{game_id}"
    drives = []
    soup = get_soup(plays)
    for num, drive in enumerate(soup.findAll('div', {'class': 'accordion-header'}), start=1):
        team_img = drive.find('img')
        if team_img is None:
            continue
        offense_team_id = get_team_id_from_img(team_img)
        drive_span = drive.find('span', {'class': 'drives'})
        result = drive_span.contents[0].getText()
        drive_info = drive_span.contents[1].getText()
        drive_info = drive_info.split(',')
        if len(drive_info) == 3:
            time_of_poss = drive_info[2].strip()
        else:
            time_of_poss = '0:00'
        drives.append({'game_id': game_id, 'drive_num': num, 'offense_id': int(offense_team_id), 'result': result.lower(),
             'num_plays': int(drive_info[0].split(" ")[0]), 'yards': int(drive_info[1].strip().split(" ")[0]),
             'time_of_poss': time_of_poss})
    return drives
