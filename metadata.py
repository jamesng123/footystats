from fbrefscraper import get_data

soup, html = get_data("https://fbref.com/en/matches/7c21232e/Manchester-United-Aston-Villa-September-25-2021-Premier-League")

def get_scores(html):
    
    body = list(html.children)[3]
    p = list(body.children)[1]
    main = list(p.children)[-6]

    scoresheet = list(main.children)[5]

    scores = scoresheet.find_all("div", {"class": "score"})
    home_score = scores[0].contents[0]
    away_score = scores[1].contents[0]

    xgs = scoresheet.find_all("div", {"class": "score_xg"})
    home_xg = xgs[0].contents[0]
    away_xg = xgs[1].contents[0]

    return home_score, home_xg, away_score, away_xg

def get_scorebox_data(html):
    body = list(html.children)[3]
    p = list(body.children)[1]
    main = list(p.children)[-6]

    data = list(main.children)[5]

    time_data = data.find_all("div", {"class": "scorebox_meta"})

    data_new = [list(i.children) for i in time_data]

    date = data_new[0][1].span["data-venue-date"]
    time = data_new[0][1].span["data-venue-time"]

    referee = data_new[0][7].span.text.strip("(Referee)")

    attendance = int(data_new[0][5].text.strip("Attendance: ").replace(",", ""))

    return date, time, referee, attendance

def get_date(html):
    return get_scorebox_data(html)[0]

def get_ko_time(html):
    return get_scorebox_data(html)[1]

def get_referee():
    return get_scorebox_data(html)[2]

def get_attendance(html):
    return get_scorebox_data(html)[3]

print(get_scores(html), get_scorebox_data(html))