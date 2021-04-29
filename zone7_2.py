import pandas as pd

# MAGIC NUMBERS ####
GAME_DAY_TITLE = "Game Day"
DAYS_BEFORE = "Days Before Match"
DAYS_AFTER = "Days After Match"
ID = "id"
DATE = "Date"

YES_GAME_DAY = 1
NOT_GAME_DAY = 0


def compute_days_before(training_dates, p_matches_dates):
    if type(p_matches_dates) is list:
        return [-1] * len(p_training)
    # training_dates = list((pd.to_datetime(p_training_dates[DATE])).values)
    matches_dates = pd.to_datetime(p_matches_dates[DATE])
    i = 0
    days_before = []
    for match in matches_dates.values:
        training_dates = training_dates[i:]
        subt = (pd.to_datetime(match) - pd.to_datetime(training_dates)).days
        days_before += [val for val in subt if val > 0]
        i = pd.DataFrame(subt).lt(0).idxmax()[0]
    days_before += [-1] * (len(training_dates) - len(days_before))
    return days_before


def compute_days_after(training_dates, p_matches_dates):
    return


training_sessions = pd.read_csv("training_sessions.csv").sort_values([ID, DATE])
training_sessions[GAME_DAY_TITLE] = NOT_GAME_DAY
# training_sessions[DAYS_BEFORE], training_sessions[DAYS_AFTER] = '?', '?'

match_days = pd.read_csv("match_days.csv").sort_values([ID, DATE])
match_days[GAME_DAY_TITLE] = YES_GAME_DAY
match_days[DAYS_BEFORE], match_days[DAYS_AFTER] = 0, 0

matches_by_id = match_days.groupby(ID)
training_by_id = training_sessions.groupby(ID)
# iterating over the players: each one is a group gotten from the pd.groupby() function
before = []
after = []
for player in training_by_id.groups:
    p_training = list((pd.to_datetime(training_by_id.get_group(player)[DATE])).values)
    try:
        before += compute_days_before(p_training, matches_by_id.get_group(player))
        after += compute_days_after(p_training, matches_by_id.get_group(player))
    except KeyError:
        before += compute_days_before(p_training, [])

# adding -1 for non valid rows (e.g. trainings with no id value)
before += [-1] * (len(training_sessions) - len(before))
training_sessions[DAYS_BEFORE] = pd.Series(before).values

data = pd.concat([match_days, training_sessions], ignore_index = True, sort = True).sort_values([ID, DATE])
print(data)
