'''
Created on Apr 30, 2016

Uses SelectKBest to select best features.

@author: Paul Reiners
'''
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2

from core.preprocessing.feature_extraction_scaling import get_data
from core.preprocessing.feature_selection import select_raw_features
from core.preprocessing.sampling import split_data


if __name__ == '__main__':
    possible_outcomes = [
        'Adoption', 'Died', 'Euthanasia', 'Return_to_owner', 'Transfer']
    # Iterate over AnimalType
    for animal_type in ['Cat', 'Dog']:
        train_data = get_data('../data/train.csv')
        train_data = train_data[train_data.SexuponOutcome.notnull()]
        train_data = train_data[train_data.AgeuponOutcome.notnull()]
        print animal_type
        train_data = train_data[train_data['AnimalType'] == animal_type]
        train_data = train_data.drop(['AnimalType'], axis=1)
        train_data = select_raw_features(train_data, animal_type)
        train_data = train_data.dropna()

        # Kittens and puppies
        print "\tnot adult"
        baby_data = train_data[train_data['IsAdult'] == 0]
        X_baby_train, y_baby_train, _, _ = split_data(baby_data)

        baby_k_best = SelectKBest(chi2)
        baby_k_best.fit_transform(X_baby_train, y_baby_train)

        print "\t{}".format(X_baby_train.columns[baby_k_best.get_support()])

        # Adults
        print "\tAdult"
        adult_data = train_data[train_data['IsAdult'] == 1]
        X_adult_train, y_adult_train, _, _ = split_data(adult_data)

        adult_k_best = SelectKBest(chi2)
        adult_k_best.fit_transform(X_adult_train, y_adult_train)

        print "\t{}".format(X_adult_train.columns[adult_k_best.get_support()])
