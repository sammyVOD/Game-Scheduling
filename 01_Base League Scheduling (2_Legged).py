# IMPORT REQUIRED MODULES
import pandas as pd
import numpy as np
import string
import random
from datetime import timedelta, date

# How many teams do you want to build a schedule for
number_of_teams = input('How many teams make up this tournament: ')
if int(number_of_teams) % 4 != 0:
    raise Exception("Invalid number. Please enter a number divisible by 4")

number_of_teams = int(number_of_teams)

# USE ALPHABETS TO REPRESENT THESE TEAMS
teams = string.ascii_uppercase[:number_of_teams]
number_of_teams = len(teams)

# MAP THE TEAMS AGAINST EACH OTHER
game_unsorted = []

for i in teams:
    for j in teams:
        if i != j:
            game_unsorted.append(i + ' vs ' + j)

# pick the games randomly
game_unsorted = random.sample(game_unsorted, len(game_unsorted))

# see samples
print('randomly picked games (5 samples):', game_unsorted[:5])

# Determine number of games per week and total game week possible
games_per_week = int(number_of_teams/2)
print(games_per_week)
games_per_day = int(games_per_week/2)
print(games_per_day)
total_gameweeks = int(len(game_unsorted)/games_per_week)
print(total_gameweeks)

# Define the gameweeks
game_wk_no = []
gameweek = []
for i in np.arange(total_gameweeks) + 1:
    game_wk_no.append(i)

game_wk_no = game_wk_no * games_per_week
# arrange the gameweeks
game_wk_no.sort()

for i in game_wk_no:
    gameweek.append('Gw' + str(i))


# DEFINE WHEN YOU WANT THIS LEAGUE TO START
start_date = input('Start Date in the format MM/DD/YYYY: ')
# convert to appropriate data type
start_date = pd.to_datetime(start_date)

game_dates = []
# Pull only weekends
weekends = [5,6]
totaldays = total_gameweeks * 7
for i in range(totaldays):
    if((start_date + timedelta(i)).weekday()) in weekends:
        game_dates.append(start_date + timedelta(i))

game_dates = game_dates * games_per_day
# arrange the game_dates
game_dates.sort()

# ARRANGE THE GAMES PER WEEK SO THAT EACH TEAM ONLY PLAYS ONCE IN A GAMEWEEK
game_schedule = []
games = game_unsorted.copy()

while len(games) > 0:  # A LOOP THAT KEEPS RUNNING TILL ALL POSSIBLE GAME COMBINATIONS ARE EXHAUSTED
    team_list = list(teams)
    if len(team_list) > 0:  # INSTANTIATE A LOOP THAT RUNS TILL ALL TEAMS HAVE BEEN CONSIDERED EACH WEEK
        allotted_team = []
        allotted_schedule = []
        for i in games:
            if len(team_list) == number_of_teams:  # PICK THE FIRST SCHEDULE IN NEW LOOP
                team_list.remove(i[0])
                team_list.remove(i[-1])
                game_schedule.append(i)
                allotted_schedule.append(i)
                allotted_team.append(i[0])
                allotted_team.append(i[-1])
            elif (i[0] not in allotted_team) and (i[-1] not in allotted_team):  # CHECK FOR THE OTHER SCHEDULES
                team_list.remove(i[0])
                team_list.remove(i[-1])
                game_schedule.append(i)
                allotted_schedule.append(i)
                allotted_team.append(i[0])
                allotted_team.append(i[-1])

        games = [ele for ele in games if ele not in allotted_schedule]  # EXCLUDE THE ALLOTTED SCHEDULE FROM THE UNSCHEDULED GAME COMBINATIONS

game_schedule


# TRANSFORMING ALL THE ABOVE TO A DATAFRAME
# starting with a dictionary
game_table = {'GameWeek': gameweek,
              'MatchDay': game_dates,
              'Game': game_schedule
              }

game_table = pd.DataFrame(game_table)
print(game_table.head())

# EXTRACT HOME TEAM AND AWAY TEAM
col_split = game_table['Game'].str.split(' vs ', expand=True)

game_table['HomeTeam'] = col_split[0]
game_table['AwayTeam'] = col_split[1]

print(game_table)
