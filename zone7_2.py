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
    matches_dates = pd.to_datetime(p_matches_dates[DATE])
    trn_before_last_game = 0
    days_before = []
    for match in matches_dates.values:
        training_dates = training_dates[trn_before_last_game:]
        subtraction = (pd.to_datetime(match) - pd.to_datetime(training_dates)).days
        days_before += [val for val in subtraction if val > 0]
        trn_before_last_game = pd.DataFrame(subtraction).lt(0).idxmax()[0]
    days_before += [-1] * (len(training_dates) - len(days_before))
    return days_before


def compute_days_after(training_dates, p_matches_dates):
    if type(p_matches_dates) is list:
        return [-1] * len(p_training)
    m_dates = pd.to_datetime(p_matches_dates[DATE])
    subtraction = (pd.to_datetime(training_dates) - pd.to_datetime(m_dates.values[0])).days
    trn_before_next_game = pd.DataFrame(subtraction).gt(0).idxmax()[0]
    days_after = [-1] * (trn_before_next_game)
    for i in range(len(m_dates.values) - 1):
        training_dates = training_dates[trn_before_next_game:]
        subtraction = (pd.to_datetime(training_dates) - pd.to_datetime(m_dates.values[i])).days
        next_subt = (pd.to_datetime(training_dates) - pd.to_datetime(m_dates.values[i + 1])).days
        trn_before_next_game = pd.DataFrame(next_subt).gt(0).idxmax()[0]
        days_after += [val for val in subtraction[:trn_before_next_game] if val > 0]
    training_dates = training_dates[trn_before_next_game:]
    subtraction = (pd.to_datetime(training_dates) - pd.to_datetime(m_dates.values[-1])).days
    days_after += [val for val in subtraction if val > 0]
    return days_after


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
        after += compute_days_after(p_training, [])

# adding -1 for non valid rows (e.g. trainings with no id value)
before += [-1] * (len(training_sessions) - len(before))
after += [-1] * (len(training_sessions) - len(after))
training_sessions[DAYS_BEFORE] = pd.Series(before).values
training_sessions[DAYS_AFTER] = pd.Series(after).values

data = pd.concat([match_days, training_sessions], ignore_index = True, sort = True).sort_values([ID, DATE])
print(data)
pd.DataFrame.to_csv(data, "second_try_sorted.csv")