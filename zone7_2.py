import pandas as pd

# MAGIC NUMBERS ####
GAME_DAY_TITLE = 'Game Day'
DAYS_BEFORE = 'Days Before Match'
DAYS_AFTER = 'Days After Match'
YES_GAME_DAY = 1
NOT_GAME_DAY = 0
INDEX_INDEX = 0
DATA_INDEX = 1
DATE_INDEX = 0
MATCH_ID_INDEX = 3
TRAINING_ID_INDEX = 19
DAYS_BEFORE_INDEX = 21
DAYS_AFTER_INDEX = 22

training_sessions = pd.read_csv("training_sessions.csv")
training_sessions[GAME_DAY_TITLE] = NOT_GAME_DAY
training_sessions[DAYS_BEFORE], training_sessions[DAYS_AFTER] = '?', '?'

match_days = pd.read_csv("match_days.csv")
match_days[GAME_DAY_TITLE] = YES_GAME_DAY
match_days[DAYS_BEFORE], match_days[DAYS_AFTER] = 0, 0

data = pd.concat([match_days, training_sessions], ignore_index = True, sort=True)

data = data.sort_values(["id", "Date"])
match_id = match_days.sort_vaslues(["id", "Date"]).groupby("id")
training_id = training_sessions.sort_values(["id", "Date"]).groupby("id")
id_groups = data.groupby("id")
for player in match_id.groups:
    p_matches = match_id.get_group(player)
    p_training = training_id.get_group(player)
    player_dates = p_matches['Date'] - p_training['Date']

    # player[DAYS_BEFORE] = argmin(match_id_groups[date] - training_id_groups[date]) s.t. > 0
    # player[DAYS_AFTER] = abs (argmin(match_id_groups[date] - training_id_groups[date]) s.t. < 0)
    print(player)
print(id_groups)
