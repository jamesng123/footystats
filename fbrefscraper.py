import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import re
import sys, getopt
import csv
import os

summary = [
    "player",
    "shirtnumber",
    "nationality",
    "position",
    "age",
    "minutes",
    "goals",
    "assists",
    "pens_made",
    "pens_att",
    "shots_total",
    "shots_on_target",
    "cards_yellow",
    "cards_red",
    "touches",
    "pressures",
    "tackles",
    "interceptions",
    "blocks",
    "xg",
    "npxg",
    "xa",
    "sca",
    "gca",
    "passes_completed",
    "passes",
    "passes_pct",
    "progressive_passes",
    "carries",
    "progressive_carries",
    "dribbles_completed",
    "dribbles",
]
passing3 = [
    "player",
    "shirtnumber",
    "nationality",
    "position",
    "age",
    "minutes",
    "passes_completed",
    "passes",
    "passes_pct",
    "passes_total_distance",
    "passes_progressive_distance",
    "passes_completed_short",
    "passes_short",
    "passes_pct_short",
    "passes_completed_medium",
    "passes_medium",
    "passes_pct_medium",
    "passes_completed_long",
    "passes_long",
    "passes_pct_long",
    "assists",
    "xa",
    "assisted_shots",
    "passes_into_final_third",
    "passes_into_penalty_area",
    "crosses_into_penalty_area",
    "progressive_passes",
]
passing_types3 = [
    "player",
    "shirtnumber",
    "nationality",
    "position",
    "age",
    "minutes",
    "passes",
    "passes_live",
    "passes_dead",
    "passes_free_kicks",
    "through_balls",
    "passes_pressure",
    "passes_switches",
    "crosses",
    "corner_kicks",
    "corner_kicks_in",
    "corner_kicks_out",
    "corner_kicks_straight",
    "passes_ground",
    "passes_low",
    "passes_high",
    "passes_left_foot",
    "passes_right_foot",
    "passes_head",
    "throw_ins",
    "passes_other_body",
    "passes_completed",
    "passes_offsides",
    "passes_oob",
    "passes_intercepted",
    "passes_blocked",
]
defense3 = [
    "player",
    "shirtnumber",
    "nationality",
    "position",
    "age",
    "minutes",
    "tackles",
    "tackles_won",
    "tackles_def_3rd",
    "tackles_mid_3rd",
    "tackles_att_3rd",
    "dribble_tackles",
    "dribbles_vs",
    "dribble_tackles_pct",
    "dribbled_past",
    "pressures",
    "pressure_regains",
    "pressure_regain_pct",
    "pressures_def_3rd",
    "pressures_mid_3rd",
    "pressures_att_3rd",
    "blocks",
    "blocked_shots",
    "blocked_shots_saves",
    "blocked_passes",
    "interceptions",
    "tackles_interceptions",
    "clearances",
    "errors",
]
possession3 = [
    "player",
    "shirtnumber",
    "nationality",
    "position",
    "age",
    "minutes",
    "touches",
    "touches_def_pen_area",
    "touches_def_3rd",
    "touches_mid_3rd",
    "touches_att_3rd",
    "touches_att_pen_area",
    "touches_live_ball",
    "dribbles_completed",
    "dribbles",
    "dribbles_completed_pct",
    "players_dribbled_past",
    "nutmegs",
    "carries",
    "carry_distance",
    "carry_progressive_distance",
    "progressive_carries",
    "carries_into_final_third",
    "carries_into_penalty_area",
    "miscontrols",
    "dispossessed",
    "pass_targets",
    "passes_received",
    "passes_received_pct",
    "progressive_passes_received",
]
misc3 = [
    "player",
    "shirtnumber",
    "nationality",
    "position",
    "age",
    "minutes",
    "cards_yellow",
    "cards_red",
    "cards_yellow_red",
    "fouls",
    "fouled",
    "offsides",
    "crosses",
    "interceptions",
    "tackles_won",
    "pens_won",
    "pens_conceded",
    "own_goals",
    "ball_recoveries",
    "aerials_won",
    "aerials_lost",
    "aerials_won_pct",
]
gk = [
    "player",
    "nationality",
    "age",
    "minutes",
    "shots_on_target_against",
    "goals_against_gk",
    "saves",
    "save_pct",
    "psxg_gk",
    "passes_completed_launched_gk",
    "passes_launched_gk",
    "passes_pct_launched_gk",
    "passes_gk",
    "passes_throws_gk",
    "pct_passes_launched_gk",
    "passes_length_avg_gk",
    "goal_kicks",
    "pct_goal_kicks_launched",
    "goal_kick_length_avg",
    "crosses_gk",
    "crosses_stopped_gk",
    "crosses_stopped_pct_gk",
    "def_actions_outside_pen_area_gk",
    "avg_distance_def_actions_gk",
]


def get_match_tables(url):
    res = requests.get(url)
    ## The next two lines get around the issue with comments breaking the parsing.
    comm = re.compile("<!--|-->")
    soup = BeautifulSoup(comm.sub("", res.text), "lxml")
    all_tables = soup.findAll("tbody")

    home_summary_table = all_tables[0]
    home_passing_table = all_tables[1]
    home_passtypes_table = all_tables[2]
    home_defence_table = all_tables[3]
    home_possession_table = all_tables[4]
    home_misc_table = all_tables[5]
    home_gk_table = all_tables[6]

    away_summary_table = all_tables[7]
    away_passing_table = all_tables[8]
    away_passtypes_table = all_tables[9]
    away_defence_table = all_tables[10]
    away_possession_table = all_tables[11]
    away_misc_table = all_tables[12]
    away_gk_table = all_tables[13]

    return (
        home_summary_table,
        home_passing_table,
        home_passtypes_table,
        home_defence_table,
        home_possession_table,
        home_misc_table,
        home_gk_table,
        away_summary_table,
        away_passing_table,
        away_passtypes_table,
        away_defence_table,
        away_possession_table,
        away_misc_table,
        away_gk_table,
    )


def get_team_frame(features, player_table):
    pre_df_player = dict()
    features_wanted_player = features
    rows_player = player_table.find_all("tr")
    for row in rows_player:
        if row.find("th", {"scope": "row"}) != None:
            for f in features_wanted_player:
                if f == "player":
                    cell = row.find("th", {"data-stat": f})
                else:
                    cell = row.find("td", {"data-stat": f})
                a = cell.text.strip().encode()
                text = a.decode("utf-8")
                if text == "":
                    text = "0"
                if (
                    (f != "player")
                    & (f != "nationality")
                    & (f != "position")
                    & (f != "squad")
                    & (f != "age")
                    & (f != "birth_year")
                ):
                    text = float(text.replace(",", ""))
                if f in pre_df_player:
                    pre_df_player[f].append(text)
                else:
                    pre_df_player[f] = [text]
    df_player = pd.DataFrame.from_dict(pre_df_player)
    return df_player


def frame_for_match_category(category, top, end, features, table):
    url = top + category + end
    if table[:4] == "home":
        if table[5:12] == "summary":
            table = get_match_tables(url)[0]
        elif table[5:12] == "passing":
            table = get_match_tables(url)[1]
        elif table[5:14] == "passtypes":
            table = get_match_tables(url)[2]
        elif table[5:12] == "defence":
            table = get_match_tables(url)[3]
        elif table[5:15] == "possession":
            table = get_match_tables(url)[4]
        elif table[5:9] == "misc":
            table = get_match_tables(url)[5]
        # elif table [5:7] == "gk":
        #     table = get_match_tables(url)[6]
    elif table[:4] == "away":
        if table[5:12] == "summary":
            table = get_match_tables(url)[7]
        elif table[5:12] == "passing":
            table = get_match_tables(url)[8]
        elif table[5:14] == "passtypes":
            table = get_match_tables(url)[9]
        elif table[5:12] == "defence":
            table = get_match_tables(url)[10]
        elif table[5:15] == "possession":
            table = get_match_tables(url)[11]
        elif table[5:9] == "misc":
            table = get_match_tables(url)[12]
        # elif table [5:7] == "gk":
        #     table = get_match_tables(url)[13]

    df_player = get_team_frame(features, table)
    return df_player


def get_home_outfield_team_data(top, end):
    df1 = frame_for_match_category("stats", top, end, summary, "home_summary_table")
    df2 = frame_for_match_category("passing", top, end, passing3, "home_passing_table")
    df3 = frame_for_match_category(
        "passing types", top, end, passing_types3, "home_passtypes_table"
    )
    df4 = frame_for_match_category("defence", top, end, defense3, "home_defence_table")
    df5 = frame_for_match_category(
        "possession", top, end, possession3, "home_possession_table"
    )
    df6 = frame_for_match_category("misc", top, end, misc3, "home_misc_table")
    # df7 = frame_for_match_category('gk',top,end,gk, 'home_gk_table')

    df = pd.concat([df1, df2, df3, df4, df5, df6], axis=1)
    df = df.loc[:, ~df.columns.duplicated()]
    return df


def get_away_outfield_team_data(top, end):
    df1 = frame_for_match_category("stats", top, end, summary, "away_summary_table")
    df2 = frame_for_match_category("passing", top, end, passing3, "away_passing_table")
    df3 = frame_for_match_category(
        "passing types", top, end, passing_types3, "away_passtypes_table"
    )
    df4 = frame_for_match_category("defence", top, end, defense3, "away_defence_table")
    df5 = frame_for_match_category(
        "possession", top, end, possession3, "away_possession_table"
    )
    df6 = frame_for_match_category("misc", top, end, misc3, "away_misc_table")
    # df7 = frame_for_match_category('gk',top,end,gk, 'away_gk_table')

    df = pd.concat([df1, df2, df3, df4, df5, df6], axis=1)
    df = df.loc[:, ~df.columns.duplicated()]
    return df


def get_fixtures(url):
    # Need to fix to get all seasons

    team = url[url.rfind("/") + 1 : -6]

    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    html = list(soup.children)[3]
    body = list(html.children)[3]
    p = list(body.children)[1]
    main = list(p.children)[-6]

    try:
        fixtures = list(main.children)[17].find_all("a", href=True)
    except:
        print(url)

    # Seems as if domestic cups dont have the same level of detail
    domestic_cup_fixture_urls = set(
        [
            p["href"]
            for p in fixtures
            if team in p["href"] and "History" not in p["href"] and "Cup" in p["href"]
        ]
    )
    other_fixture_urls = set(
        [
            p["href"]
            for p in fixtures
            if team in p["href"]
            and "History" not in p["href"]
            and "Cup" not in p["href"]
        ]
    )
    domestic_cup_fixture_urls = [
        f"https://fbref.com{i}" for i in domestic_cup_fixture_urls
    ]
    other_fixture_urls = [f"https://fbref.com{i}" for i in other_fixture_urls]

    with open("urls.txt", "a") as myfile:
        for i in other_fixture_urls:
            myfile.write(f"{i}\n")

    return domestic_cup_fixture_urls, other_fixture_urls


def get_scraped_urls():
    urls = []
    with open("urls.txt", "r") as myfile:
        for i in myfile:
            urls.append(i.strip())
    return urls


def clean_up_urls():
    captured_urls = set(get_scraped_urls())
    print(len(captured_urls))

    with open("urls.txt", "w"):
        pass

    with open("urls.txt", "a") as myfile:
        for i in captured_urls:
            myfile.write(f"{i}\n")

    return captured_urls


def get_teams(url):

    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    html = list(soup.children)[3]
    main = soup.find_all("title")
    teams = soup.find_all("a")
    # 46 is the competition
    # 47 is the home team
    # 51 is the away team

    home_team = teams[47].get_text().lower().split()
    away_team = teams[51].get_text().lower().split()
    home_team = "_".join(home_team)
    away_team = "_".join(away_team)

    # Sometimes the away team appears as "prev-match"
    if away_team == "prev_match":
        away_team = teams[50].get_text().lower().split()
        away_team = "_".join(away_team)

    return home_team, away_team

def get_comp_teams(url):

    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    html = list(soup.children)[3]
    main = soup.find_all('title')
    refs = soup.find_all('a', href=True)

    for i in range(len(refs)):
        if refs[i]['href'] == "#all_rank_key":
            teams_index = i
    teams = refs[teams_index+1:teams_index+21]
    teams = [f'https://fbref.com/{i["href"]}' for i in teams]

    return teams

def main(year, team_list):
    broken_urls = []
    captured_urls = []
    precaptured_urls = clean_up_urls()
    datadir = "data"
    os.makedirs(datadir, exist_ok=True)
    os.makedirs(f'{datadir}/{year}', exist_ok=True)

    for team in team_list:
        for i in get_fixtures(team)[1]:
            if i not in precaptured_urls and i not in captured_urls:
                try:
                    home, away = get_teams(i)
                    print("Home: ", home)
                    os.makedirs(f'{datadir}/{year}/{home}', exist_ok=True)
                    os.makedirs(f'{datadir}/{year}/{away}', exist_ok=True)

                    home_df = get_home_outfield_team_data(i, "")
                    home_df.to_csv(
                        f"{datadir}/{year}/{home}/home_{home}-vs-{away}.csv"
                    )
                    away_df = get_away_outfield_team_data(i, "")
                    away_df.to_csv(
                        f"{datadir}/{year}/{away}/away_{home}-vs-{away}.csv"
                    )

                except:
                    broken_urls.append(i)

                captured_urls.append(i)
            else:
                print(f"This url, {i}, has already been scraped")

    if len(broken_urls) > 0:
        print("BROKEN URLS: ", broken_urls)

    clean_up_urls()