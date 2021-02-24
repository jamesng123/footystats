import fbrefscraper
import cleandata
import requests
from bs4 import BeautifulSoup
import os


def get_team_list(url):
    return fbrefscraper.get_comp_teams(url)


# Data is only from 17/18 onwards
seasons = {
    "https://fbref.com/en/comps/20/3248/2019-2020-Bundesliga-Stats": "19_20",
    "https://fbref.com/en/comps/11/1640/2017-2018-Serie-A-Stats": "17_18",
    "https://fbref.com/en/comps/11/1896/2018-2019-Serie-A-Stats": "18_19",
    "https://fbref.com/en/comps/11/3260/2019-2020-Serie-A-Stats": "19_20",
    "https://fbref.com/en/comps/13/1632/2017-2018-Ligue-1-Stats": "17_18",
    "https://fbref.com/en/comps/13/2104/2018-2019-Ligue-1-Stats": "18_19",
    "https://fbref.com/en/comps/13/3243/2019-2020-Ligue-1-Stats": "19_20",
    "https://fbref.com/en/comps/12/1652/2017-2018-La-Liga-Stats": "17_18",
    "https://fbref.com/en/comps/12/1886/2018-2019-La-Liga-Stats": "18_19",
    "https://fbref.com/en/comps/12/3239/2019-2020-La-Liga-Stats": "19_20",
}


def main(year, team_list: list):
    broken_urls = []
    captured_urls = []
    precaptured_urls = fbrefscraper.clean_up_urls()
    datadir = "data"
    os.makedirs(datadir, exist_ok=True)
    os.makedirs(f"{datadir}/{year}", exist_ok=True)

    for team in team_list:
        print(team)
        soup, html = fbrefscraper.get_data(team)
        for i in fbrefscraper.get_fixtures(team, html)[1]:
            if i not in precaptured_urls and i not in captured_urls:
                soup, html = fbrefscraper.get_data(i)
                try:
                    home, away = fbrefscraper.get_teams(soup)
                    print("Home: ", home, "Away: ", away)
                    os.makedirs(f"{datadir}/{year}/{home}", exist_ok=True)
                    os.makedirs(f"{datadir}/{year}/{away}", exist_ok=True)

                    home_df = fbrefscraper.get_home_outfield_team_data(i, "")
                    home_df.to_csv(f"{datadir}/{year}/{home}/home_{home}-vs-{away}.csv")
                    away_df = fbrefscraper.get_away_outfield_team_data(i, "")
                    away_df.to_csv(f"{datadir}/{year}/{away}/away_{home}-vs-{away}.csv")

                except:
                    broken_urls.append(i)

                captured_urls.append(i)
            else:
                pass
                # print(f"This url, {i}, has already been scraped")

    if len(broken_urls) > 0:
        print("BROKEN URLS: ", broken_urls)
        fbrefscraper.record_broken_urls(broken_urls)

    fbrefscraper.clean_up_urls()


# for i in seasons.items():
#     print(i[0], i[1])
#     main(i[1], get_team_list(i[0]))

main('18_19_copy', get_team_list('https://fbref.com/en/comps/12/1886/2018-2019-La-Liga-Stats'))