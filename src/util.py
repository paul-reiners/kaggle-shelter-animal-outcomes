'''
Created on Apr 26, 2016

@author: Paul Reiners
'''
from math import log

from sklearn.cross_validation import train_test_split

import numpy as np
import pandas as pd


def log_loss(truths, label_col_name, predictions_df, possible_labels):
    ''' Function to measure log loss of a prediction.

    Parameters
    ==========
    truths          : numpy.ndarray
                      the ground truth
    label_col_name  : str
                      the name of the column you're trying to predict
    predictions_df  : pandas.core.frame.DataFrame
                      your predictions
    possible_labels : list
                      possible labels'''
    n = len(truths)
    total = 0.0
    for i in range(n):
        truth = truths[i]
        for possible_label in possible_labels:
            if truth == possible_label:
                y = 1
            else:
                y = 0
            prediction = predictions_df.iloc[i]
            p = prediction[truth]
            p = max(min(p, 1 - 1e-15), 1e-15)
            total += y * log(p)

    return -1.0 / n * total


def get_data(file_path, tag=None):
    dtype = {'Name': str}
    data = pd.read_csv(
        file_path, dtype=dtype, parse_dates=['DateTime'], index_col=0)
    data.Name = data.Name.fillna('')
    data.SexuponOutcome = data.SexuponOutcome.fillna('')
    if tag:
        data['tag'] = tag

    return data


def split_data(train_data):
    X = train_data.drop(['OutcomeType'], axis=1)
    y = train_data['OutcomeType']
    X_train, X_test, y_train, y_test = train_test_split(X, y)
    return X_train, y_train, X_test, y_test


def get_is_named(name):
    if len(name) > 0:
        return 1.0
    else:
        return 0.0


def get_month(date_time):
    return date_time.month


def is_dog(animal_type):
    if animal_type == 'Dog':
        return 1.0
    else:
        return 0.0


def is_intact(sex_upon_outcome):
    if 'Intact' in sex_upon_outcome:
        return 1.0
    elif 'Neutered' in sex_upon_outcome or 'Spayed' in sex_upon_outcome:
        return 0.0
    else:
        return 0.5


def is_black(color):
    if color == 'Black':
        return 1.0
    else:
        return 0.0


def is_male(sex_upon_outcome):
    if 'Male' in sex_upon_outcome:
        return 1.0
    elif 'Female' in sex_upon_outcome:
        return 0.0
    else:
        return 0.5


def is_pit_bull(breed):
    if 'Pit Bull' in breed:
        return 1.0
    else:
        return 0.0


def is_golden_retriever(breed):
    if 'Golden Retriever' in breed:
        return 1.0
    else:
        return 0.0


def is_doodle_dog(breed):
    if 'Poodle' in breed and ('Labrador' in breed or 'Retriever' in breed):
        return 1.0
    else:
        return 0.0


def is_spring(month):
    return month == 4 or month == 5


def is_dangerous(breed):
    dangerous_breeds = [
        'Great Dane', 'Boxer', 'Wolf Hybrid', 'Malamute', 'Husky', 'Mastiff',
        'Doberman Pinscher', 'German Shepherd', 'Rottweiler', 'Pit Bull']
    for dangerous_breed in dangerous_breeds:
        if dangerous_breed in breed:
            return 1.0
    return 0.0


def is_mix(breed):
    if "Mix" in breed:
        return 1.0
    else:
        return 0.0


def commmon_preprocess_data(data, animal_type):
    data['AgeuponOutcome'] = data['AgeuponOutcome'].apply(convert_age_to_days)
    data['IsNamed'] = data['Name'].apply(get_is_named)
    data['IsIntact'] = data['SexuponOutcome'].apply(is_intact)
    data["OutcomeType"] = data["OutcomeType"].astype('category')
    month = data['DateTime'].apply(get_month)
    data['IsPitBull'] = data['Breed'].apply(is_pit_bull)
    data['IsDangerous'] = data['Breed'].apply(is_dangerous)
    data['IsBlack'] = data['Color'].apply(is_black)
    data['IsGoldenRetriever'] = data[
        'Breed'].apply(is_golden_retriever)
    data['IsDoodleDog'] = data['Breed'].apply(is_doodle_dog)
    data['IsSpring'] = month.apply(is_spring)

    data['IsMale'] = data['SexuponOutcome'].apply(is_male)
    data['IsMix'] = data['Breed'].apply(is_mix)
    data['Month'] = data['DateTime'].apply(get_month)


def preprocess_data(data, animal_type):
    commmon_preprocess_data(data, animal_type)

    keep_cols = ['OutcomeType', 'tag']
    if animal_type == 'Cat':
        keep_cols.extend(
            ['AgeuponOutcome', 'IsNamed', 'IsIntact', 'IsSpring'])
    else:
        keep_cols.extend(['AgeuponOutcome', 'IsNamed',
                          'IsIntact', 'IsPitBull', 'IsDangerous'])

    data = data.loc[:, keep_cols]

    return data


def convert_age_to_days(age_str):
    if type(age_str) is str:
        parts = age_str.split()
        num = int(parts[0])
        unit = parts[1]
        if 'day' in unit:
            return num
        elif 'week' in unit:
            return 7 * num
        elif 'month' in unit:
            return 30 * num
        elif 'year' in unit:
            return 365 * num
    else:
        return np.nan
