import pandas as pd
import os


def get_input(file):
    data = pd.read_csv(file, index_col=False)
    return data


def clean_data(match):
    data = get_input(match)
    data.set_index("player", inplace=True)
    del data["shirtnumber"]
    del data["nationality"]
    del data["age"]
    return data


def out_to_csv(team, match):
    data = clean_data(f"{team}/{match}")
    data.to_csv(f"{team}/cleaned_{match}")


teams = os.listdir()
teams = [
    i for i in teams if "." not in i and i != "footystatsenv"
]  # Don't want to pick up any files, just the team folders

for team in teams:
    matches = os.listdir(team)
    for match in matches:
        # print(f'{team}/{match}')
        try:
            out_to_csv(team, match)
        except KeyError:
            pass  # We have already cleaned this file...
            print(team, match)

for team in teams:
    matches = os.listdir(team)
    for match in matches:
        if "cleaned" not in match:
            os.remove(f"{team}/{match}")
