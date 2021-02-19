import fbrefscraper
import cleandata

# Need to write a function to get these links programatically
premier_league_teams = [
    "https://fbref.com/en/squads/b8fd03ef/Manchester-City-Stats",
    "https://fbref.com/en/squads/19538871/Manchester-United-Stats",
    "https://fbref.com/en/squads/18bb7c10/Arsenal-Stats",
    "https://fbref.com/en/squads/1df6b87e/Sheffield-United-Stats",
    "https://fbref.com/en/squads/60c6b05f/West-Bromwich-Albion-Stats",
    "https://fbref.com/en/squads/fd962109/Fulham-Stats",
    "https://fbref.com/en/squads/943e8050/Burnley-Stats",
    "https://fbref.com/en/squads/b2b47a98/Newcastle-United-Stats",
    "https://fbref.com/en/squads/d07537b9/Brighton-and-Hove-Albion-Stats",
    "https://fbref.com/en/squads/8cec06e1/Wolverhampton-Wanderers-Stats",
    "https://fbref.com/en/squads/47c64c55/Crystal-Palace-Stats",
    "https://fbref.com/en/squads/33c895d4/Southampton-Stats",
    "https://fbref.com/en/squads/5bfb9659/Leeds-United-Stats",
    "https://fbref.com/en/squads/8602292d/Aston-Villa-Stats",
    "https://fbref.com/en/squads/361ca564/Tottenham-Hotspur-Stats",
    "https://fbref.com/en/squads/d3fd31cc/Everton-Stats",
    "https://fbref.com/en/squads/7c21e445/West-Ham-United-Stats",
    "https://fbref.com/en/squads/cff3d9bb/Chelsea-Stats",
    "https://fbref.com/en/squads/822bd0ba/Liverpool-Stats",
    "https://fbref.com/en/squads/a2d435b3/Leicester-City-Stats",
]

#Need to introduce the cleaning process within here too... still need to figure this out

def main(team_list):
    fbrefscraper.main(team_list)
    cleandata.clean()

main(premier_league_teams)