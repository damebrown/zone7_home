import pandas as pd

# MAGIC NUMBERS ####
GAME_DAY_TITLE = "Game Day"
DAYS_BEFORE = "Days Before Match"
DAYS_AFTER = "Days After Match"
ID = "id"
DATE = "Date"

YES_GAME_DAY = 1
NOT_GAME_DAY = 0


def compute_days_before(p_training_dates, p_matches_dates):
    training_dates = list((pd.to_datetime(p_training_dates[DATE])).values)
    matches_dates = pd.to_datetime(p_matches_dates[DATE])
    i = 0
    for match in matches_dates.values:
        training_dates = training_dates[i:]
        subt = (pd.to_datetime(match) - pd.to_datetime(training_dates)).days
        answer = [val for val in subt if val > 0]
        print(answer)
        i = pd.DataFrame(subt).lt(0).idxmax()[0]
        # print("MATCH: ", match)
        # print("TRAINING DATES:", training_dates.values)
        # print("SUBTRACTION: ", subt)
    return


def compute_days_after():
    return


training_sessions = pd.read_csv("training_sessions.csv")
training_sessions[GAME_DAY_TITLE] = NOT_GAME_DAY
training_sessions[DAYS_BEFORE], training_sessions[DAYS_AFTER] = '?', '?'

match_days = pd.read_csv("match_days.csv")
match_days[GAME_DAY_TITLE] = YES_GAME_DAY
match_days[DAYS_BEFORE], match_days[DAYS_AFTER] = 0, 0

data = pd.concat([match_days, training_sessions], ignore_index = True, sort = True)

matches_by_id = match_days.sort_values([ID, DATE]).groupby(ID)
training_by_id = training_sessions.sort_values([ID, DATE]).groupby(ID)
id_groups = data.sort_values([ID, DATE]).groupby(ID)
# iterating over the players: each one is a group gotten from the pd.groupby() function
for player in id_groups.groups:
    print("PLAYER ID: ", player)
    # fetching the player's matches
    p_matches = matches_by_id.get_group(player)
    # fetching the player's trainings
    p_training = training_by_id.get_group(player)

    # player_dates = pd.to_datetime(pd.to_datetime(p_training['Date']).values[0] - pd.to_datetime(p_matches['Date']).values).day
    compute_days_before(p_training, p_matches)

    # Psuedo code:
    # player[DAYS_BEFORE] = argmin(match_id_groups[date] - training_id_groups[date]) s.t. > 0
    # player[DAYS_AFTER] = abs (argmin(match_id_groups[date] - training_id_groups[date]) s.t. < 0)
