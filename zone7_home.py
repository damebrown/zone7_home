import pandas as pd
from datetime import date

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
training_sessions = training_sessions.sort_values(["id", "Date"])

match_days = pd.read_csv("match_days.csv")
match_days[GAME_DAY_TITLE] = YES_GAME_DAY
match_days[DAYS_BEFORE], match_days[DAYS_AFTER] = 0, 0
match_days = match_days.sort_values(["id", "Date"])


def day(a):
    """
    returns an int value of the stringy date a's day
    :param a: a stringy date
    :return: an int value of a's day value
    """
    return int(a[8:10])


def month(a):
    """
    returns an int value of the stringy date a's month
    :param a: a stringy date
    :return: an int value of a's month value
    """
    return int(a[5:7])


def year(a):
    """
    returns an int value of the stringy date a's year
    :param a: a stringy date
    :return: an int value of a's year value
    """
    return int(a[0:4])


def is_a_before_b(a, b):
    """
    returns true if the date a is earlier than the date b
    :param a: date
    :param b: date
    :return: True iff a is prior to b
    """
    if not a or not b:
        return False
    year_a, year_b = year(a), year(b)
    if year_a != year_b:
        return year_a < year_b
    month_a, month_b = month(a), month(b)
    if month_a != month_b:
        return month_a < month_b
    return day(a) < day(b)


def subtract(a, b):
    """returning the number of days date a occurred in before date b"""
    d_a = date(year(a), month(a), day(a))
    d_b = date(year(b), month(b), day(b))
    delta = d_b - d_a
    return delta.days


def promote_training():
    """
    this function promotes the data taken from the training data base
    """
    global training, training_date, training_id, training_counter
    training = next(training_gen)[DATA_INDEX]
    training_counter += 1
    training_date = training[DATE_INDEX]
    training_id = training[TRAINING_ID_INDEX]


def unite_n_sort_data():
    """
    this function concatenates the data from the training sessions and from the match days into one data set and than
    sorts it (stable sorting)- first by id and then by date
    :return: the concatenated and sorted data
    """
    match_days_to_concat = pd.DataFrame()
    for i, col in enumerate(training_sessions.columns):
        if col not in match_days.columns:
            match_days_to_concat.insert(i, col, None)
        else:
            match_days_to_concat.insert(i, col, match_days[col])

    # stable-sorting the data: first by id, and then by date
    return pd.concat([match_days_to_concat, training_sessions]).sort_values(["id", "Date"])


def next_match():
    """
    this function updates the days before match count
    """
    global next_match_id, next_match_date
    if i + 1 < len(match_days):
        next_match_id = match_days.iloc[i + 1][MATCH_ID_INDEX]
        if next_match_id == match_id:
            next_match_date = match_days.iloc[i + 1][DATE_INDEX]
            training_sessions.iloc[training_counter, DAYS_BEFORE_INDEX] = abs(subtract(next_match_date, training_date))
        else:
            training_sessions.iloc[training_counter, DAYS_BEFORE_INDEX] = -1


training_counter = 0
training_gen = training_sessions.iterrows()
training = next(training_gen)[DATA_INDEX]
training_date = training[DATE_INDEX]
training_id = training[TRAINING_ID_INDEX]
last_match_date = 0
next_match_id, next_match_date = 0, 0

for i, match in enumerate(match_days.iterrows()):
    match_date = match[DATA_INDEX][DATE_INDEX]
    match_id = match[DATA_INDEX][MATCH_ID_INDEX]
    while match_id != training_id:
        try:
            if training_id > match_id:
                break
            training_sessions.iloc[training_counter, DAYS_AFTER_INDEX] = -1
            if is_a_before_b(a = match_date, b = training_date):
                training_sessions.iloc[training_counter, DAYS_BEFORE_INDEX] = -1
                training_sessions.iloc[training_counter, DAYS_AFTER_INDEX] = abs(
                    subtract(last_match_date, training_date))
            else:
                next_match()
            promote_training()
        except StopIteration:
            last_match_date = match_date
            break
    else:
        if last_match_date:
            # if we changed id
            if is_a_before_b(a = match_date, b = last_match_date):
                last_match_date = 0
        # while the training occurred before the match
        while match_id == training_id and is_a_before_b(a = training_date, b = match_date):
            training_sessions.iloc[training_counter, DAYS_BEFORE_INDEX] = abs(subtract(match_date, training_date))
            if last_match_date:
                training_sessions.iloc[training_counter, DAYS_AFTER_INDEX] = abs(
                    subtract(last_match_date, training_date))
            else:
                training_sessions.iloc[training_counter, DAYS_AFTER_INDEX] = -1
            promote_training()
        last_match_date = match_date
        training_sessions.iloc[training_counter, DAYS_AFTER_INDEX] = abs(subtract(last_match_date, training_date))
        next_match()
        promote_training()

data = unite_n_sort_data()

# pd.DataFrame.to_csv(training_sessions, "sorted_trainings.csv")
# pd.DataFrame.to_csv(match_days, "sorted_match_days.csv")
pd.DataFrame.to_csv(data, "concatenated_data.csv")
