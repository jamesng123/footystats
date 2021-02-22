import fbrefscraper
import cleandata

def get_team_list(url):
    return fbrefscraper.get_comp_teams(url)

def main(year, team_list):
    fbrefscraper.main(year, team_list)
    # cleandata.clean()

# Data is only from 17/18 onwards

main("18_19", get_team_list('https://fbref.com/en/comps/9/1889/2018-2019-Premier-League-Stats'))