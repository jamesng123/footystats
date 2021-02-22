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


def out_to_csv(year, team, match):
    data = clean_data(f"data/{year}/{team}/{match}")
    data.to_csv(f"data/{year}/{team}/cleaned_{match}")

def get_dir_data():
    data = os.listdir()
    data = [
        i for i in data if "." not in i and i != "footystatsenv" and i != "TODO" and i != "__pycache__"
    ]  # Don't want to pick up any files, just the team folders
    return data

def clean(year):
    data = get_dir_data()
    for i in data:
        teams = os.listdir(f'{i}/{year}')
        for team in teams:
            matches = os.listdir(f'{i}/{year}/{team}')
            for match in matches:
                # print(f'{team}/{match}')
                try:
                    out_to_csv(year, team, match)
                except KeyError:
                    pass  # We have already cleaned this file...
                    # print(team, match)

    for i in data:
        teams = os.listdir(f'{i}/{year}')
        for team in teams:
            matches = os.listdir(f'{i}/{year}/{team}')
            for match in matches:
                print(team, match)
                if "cleaned" not in match:
                    os.remove(f"{i}/{year}/{team}/{match}")


clean("19_20")