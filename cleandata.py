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
    del data["Unnamed: 0"]
    return data


def out_to_csv(team, match):
    data = clean_data(f"data/{team}/{match}")
    data.to_csv(f"data/{team}/cleaned_{match}")


data = os.listdir()
data = [
    i for i in data if "." not in i and i != "footystatsenv" and i != "TODO"
]  # Don't want to pick up any files, just the team folders

for i in data:
    teams = os.listdir(i)
    for team in teams:
        matches = os.listdir(f'{i}/{team}')
        for match in matches:
            # print(f'{team}/{match}')
            try:
                out_to_csv(team, match)
            except KeyError:
                pass  # We have already cleaned this file...
                print(team, match)

for i in data:
    teams = os.listdir(i)
    for team in teams:
        matches = os.listdir(f'{i}/{team}')
        for match in matches:
            print(team, match)
            if "cleaned" not in match:
                os.remove(f"{i}/{team}/{match}")
