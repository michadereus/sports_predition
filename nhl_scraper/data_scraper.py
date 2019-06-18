from urllib.request import urlopen as open_url
from bs4 import BeautifulSoup as soup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from datetime import date
from numpy import array
import pandas as pd
import csv

# NHL
nhl_szn_url = "http://www.nhl.com/stats/team?reportType=season&seasonFrom=20182019&seasonTo=20182019&gameType=2&filter=gamesPlayed,gte,1&sort=points,wins"
nhl_daily_url = "http://www.nhl.com/stats/team?reportType=game&dateFrom={year}-{month}-{day}&dateTo={year}-{month}-{day}&gameType=2&filter=gamesPlayed,gte,1&sort=points,wins"
nhl_test_url = "http://www.nhl.com/stats/team?reportType=game&dateFrom=2018-10-10&dateTo=2018-10-10&gameType=2&filter=gamesPlayed,gte,1&sort=points,wins"
nhl_stats_home_url = "http://www.nhl.com/stats/team?reportType=game&dateFrom=2018-10-08&dateTo=2018-10-08&gameType=2&gameLocation={H or R}&filter=gamesPlayed,gte,1&sort=points,wins"
# ESPN
espn_team = "http://www.espn.com/nhl/statistics/{team}"
espn_rpi = "http://www.espn.com/nhl/stats/rpi/_/season/{year}"
espn_attendance = "http://www.espn.com/nhl/attendance/_/year/{year}"
espn_daily_lines = "http://www.espn.com/nhl/lines"
# CORSICA
corsica_line_stats = "http://corsica.hockey/line-stats/"
corsica_pairing_stats = "http://corsica.hockey/pairing-stats/"
# today format: 2018-30-12
today = date.today()
features = ['Date', 'Team', 'Game', 'Home/Away', 'W', 'L', 'OT', 'P', 'GF', 'GA', 'SF', 'SA', 'FOW%']
# teams and their abbr
nhl_teams_dict = {
    'AFM': "Atlanta Flames",
    'ANA': "Anaheim Ducks",
    'ARI': "Arizona Coyotes",
    'ATL': "Atlanta Thrashers",
    'BOS': "Boston Bruins",
    'BRK': "Brooklyn Americans",
    'BUF': "Buffalo Sabres",
    'CAR': "Carolina Hurricanes",
    'CGS': "California Golden Seals",
    'CGY': "Calgary Flames",
    'CHI': "Chicago Blackhawks",
    'CBJ': "Columbus Blue Jackets",
    'CLE': "Cleveland Barons",
    'CLR': "Colorado Rockies",
    'COL': "Colorado Avalanche",
    'DAL': "Dallas Stars",
    'DFL': "Detroit Falcons",
    'DCG': "Detroit Cougars",
    'DET': "Detroit Red Wings",
    'EDM': "Edmonton Oilers",
    'FLA': "Florida Panthers",
    'HAM': "Hamilton Tigers",
    'HFD': "Hartford Whalers",
    'KCS': "Kansas City Scouts",
    'LAK': "Los Angeles Kings",
    'MIN': "Minnesota Wild",
    'MMR': "Montreal Maroons",
    'MNS': "Minnesota North Stars",
    'MTL': "Montréal Canadiens",
    'MWN': "Montreal Wanderers",
    'NSH': "Nashville Predators",
    'NJD': "New Jersey Devils",
    'NYA': "New York Americans",
    'NYI': "New York Islanders",
    'NYR': "New York Rangers",
    'OAK': "Oakland Seals",
    'OTT': "Ottawa Senators",
    'PHI': "Philadelphia Flyers",
    'PHX': "Phoenix Coyotes",
    'PIR': "Pittsburgh Pirates",
    'PIT': "Pittsburgh Penguins",
    'QUA': "Philadelphia Quakers",
    'QUE': "Quebec Nordiques",
    'QBD': "Quebec Bulldogs",
    'SJS': "San Jose Sharks",
    'SLE': "St. Louis Eagles",
    'STL': "St. Louis Blues",
    'TAN': "Toronto Arenas",
    'TBL': "Tampa Bay Lightning",
    'TOR': "Toronto Maple Leafs",
    'TSP': "Toronto St. Patricks",
    'VAN': "Vancouver Canucks",
    'VGK': "Vegas Golden Knights",
    'WPG': "Winnipeg Jets",
    'WSH': "Washington Capitals"
}
home_away_dict = {
    "@": 'Away',
    "vs": 'Home'
}


def url_to_soup(url):
    # selenium driver setup
    driver = webdriver.Firefox()
    # get url
    driver.get(url)
    # create sauce using driver
    sauce = driver.page_source
    driver.close()
    url_soup = soup(sauce, 'lxml')
    return url_soup


def nhl_daily_data(year, month, day):
    nhl_daily = f"http://www.nhl.com/stats/team?reportType=game&dateFrom={year}-{month}-{day}&dateTo={year}-{month}-{day}&gameType=2&filter=gamesPlayed,gte,1&sort=points,wins"
    nhl_soup = url_to_soup(nhl_daily)
    # finding table data
    table_body = nhl_soup.find(attrs="rt-table").find(attrs='rt-tbody')
    # parsing and populating
    game_data = []
    for rows in table_body.find_all(attrs="rt-tr-group"):
        row_data = []
        # looping through row data
        for td in rows.find_all():
            row_data.append(td.text)
        game_date = f"{year}-{month}-{day}"
        # team name to abbr
        team_name = "-"
        for k, v in nhl_teams_dict.items():
            if row_data[3] == v:
                team_name = k
        # game_date = row_data[4][0:9].replace('/', '-')
        # away = '@' home = 'vs'
        home_away = row_data[4][11:14].strip()
        for n, i in home_away_dict.items():
            if row_data[4][11:14].strip() == n:
                home_away = i
        enemy_team = row_data[4][14:].lstrip()
        win = row_data[8]
        loss = row_data[9]
        over_time = row_data[11]
        points = row_data[12]
        goals_for = row_data[13]
        goals_against = row_data[14]
        shots_for = row_data[17]
        shots_against = row_data[18]
        power_play_goals_for = row_data[19]
        power_play_opportunities = row_data[20]
        power_play_percent = row_data[21]
        power_play_goals_against = row_data[23]
        penalty_kill_percent = row_data[24]
        faceoff_wins = row_data[25]
        faceoff_losses = row_data[26]
        faceoff_win_pct = row_data[27]
        row_data = [game_date, team_name, enemy_team, home_away, win, loss, over_time, points, goals_for,
                     goals_against, shots_for, shots_against, power_play_goals_for, power_play_opportunities, power_play_percent,
                    power_play_goals_against, penalty_kill_percent, faceoff_wins, faceoff_losses, faceoff_win_pct]
        game_data.append(row_data)
    return game_data


# collects all last season data- date format: string(year/month/day)
def batch_collection(start_date, end_date):
    season_dates = pd.date_range(start=start_date, end=end_date)
    for date in season_dates:
        print(date)
        year = date.year
        month = date.month
        day = date.day
        chart = array(nhl_daily_data(year, month, day))
        # print(chart)
        with open('2017-2018season.txt', "a") as output:
            writer = csv.writer(output, lineterminator='\n')
            writer.writerows(chart)


batch_collection('10/4/2017', '4/8/2018')


# full daily collection manager
def daily_collection():
    pass

# nfl_df = pd.DataFrame()
#
# def nhl_history_collection():
#
#     for year in range(2012, 2018):
#
#         url = espn_team.format(year=year)  # get the url
#
#         with open_url(url) as client:
#             client = open_url(url)
#             html = client.read()
#             data_soup = soup(html, "html.parser")
#
#         column_headers = [th.getText() for th in soup.findAll('thead', limit=1)[0].findAll('th')]
#
#         data_rows = soup.findAll('tbody', limit=1)[0].findAll('tr')[0:]
#
#         player_data = [[td.getText() for td in data_rows[i].findAll(['th', 'td'])]
#                        for i in range(len(data_rows))]
#
#         # Turn yearly data into a DataFrame
#
#         year_df = pd.DataFrame(player_data, columns=column_headers)
#
#         year_df = year_df[(year_df.Date != 'Playoffs') & (year_df.Week != 'WildCard') & (year_df.Week != 'Week')]
#
#         year_df = year_df.infer_objects().drop(['index'], axis=1).reset_index(drop=True)
#
#         results = year_df.loc[(year_df.iloc[:, 8] != '')]
#
#         winner_pts = np.array(results.iloc[:, 8], dtype=int)
#
#         loser_pts = np.array(results.iloc[:, 9], dtype=int)
#
#         spreads = winner_pts - loser_pts
#
#         winner_pf = stats.zscore(winner_pts)
#
#         loser_pf = stats.zscore(loser_pts)
#
#         points_pf = list(winner_pts) + list(loser_pts)
#
#         percentile = np.array([stats.norm.cdf(x) for x in stats.zscore(spreads)])
#
#         results_df = pd.concat([results,
#                                 pd.DataFrame(data=winner_pf, columns=['Winner Performance']),
#                                 pd.DataFrame(data=loser_pf, columns=['Loser Performance']),
#                                 pd.DataFrame(data=spreads, columns=['Spread']),
#                                 pd.DataFrame(data=percentile, columns=['Spread Prcntl']),
#                                 ], axis=1)
#
#         col_len = [x for x in range(results_df.shape[1])]
#
#         col_len.remove(7)
#
#         results_df = results_df.iloc[:, col_len]
#
#         results_df = results_df.rename(columns={list(results_df)[5]: 'H/A',
#                                                 list(results_df)[7]: 'Pts Scored',
#                                                 list(results_df)[8]: 'Pts Allowed',
#                                                 list(results_df)[9]: 'Yds Gained',
#                                                 list(results_df)[10]: 'TOs',
#                                                 list(results_df)[11]: 'Yds Allowed',
#                                                 list(results_df)[12]: 'Opp TOs',
#                                                 list(results_df)[13]: 'Tm Performance',
#                                                 list(results_df)[14]: 'Opp Performance'})
#
#         filename = 'NFL {year} Weekly Results.csv'.format(year=year)
#
#         results_df.to_csv(filename)
#
#         nfl_df = pd.concat([nfl_df, results_df], axis=0)
#
#         print(filename + ' has been saved.')
#
# print('All results from the specified timeframe have been saved.')
#
# nfl_df = nfl_df.reset_index(drop=True)
# # write html to file
# # with open('espn_html.txt', "w+") as file:
# #     file.write(str(espn_soup))


