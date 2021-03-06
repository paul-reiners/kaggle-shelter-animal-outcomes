'''
Created on Apr 26, 2016

Trains models on test data.  If results are better than the best submission
so far, models are run on test data and a new submission file is created.

@author: Paul Reiners
'''

from core.learning.classifiers.xgb_predictor \
    import XGBPredictor
from core.learning.performance_metrics import log_loss
from core.preprocessing.feature_extraction_scaling import get_data
from core.preprocessing.feature_selection import select_features
from core.preprocessing.sampling import split_data
import numpy as np


BEST_SCORE = 0.79955


if __name__ == '__main__':
    predictors = {
        'Cat': {0: XGBPredictor('Cat', 0), 1: XGBPredictor('Cat', 1)},
        'Dog': {0: XGBPredictor('Dog', 0), 1: XGBPredictor('Dog', 1)}}
    test_data_sets = {}
    all_predictions_df = None
    all_y_test = None
    train_data_sets = {}

    for animal_type in ['Cat', 'Dog']:
        for is_adult in [0, 1]:
            train_data = get_data('../data/train.csv', 'train')
            train_data = train_data[train_data.SexuponOutcome.notnull()]
            train_data = train_data[train_data.AgeuponOutcome.notnull()]

            test_data = get_data('../data/test.csv', 'test')
            all_data = train_data.append(test_data)
            all_data = select_features(all_data, animal_type, is_adult)

            train_data = all_data[all_data['tag'] == 'train']
            train_data = train_data.drop(['tag'], axis=1)
            test_data = all_data[all_data['tag'] == 'test']
            test_data = test_data.drop(['OutcomeType', 'tag'], axis=1)
            if animal_type not in test_data_sets:
                test_data_sets[animal_type] = {}
            test_data_sets[animal_type][is_adult] = test_data
            if animal_type not in train_data_sets:
                train_data_sets[animal_type] = {}
            train_data_sets[animal_type][is_adult] = train_data

            X_train, y_train, X_test, y_test = split_data(train_data)

            if all_y_test is None:
                all_y_test = y_test.ravel()
            else:
                all_y_test = np.append(all_y_test, y_test.ravel())
            predictor = predictors[animal_type][is_adult]

            predictor.fit(X_train, y_train)
            predictions_df = predictor.predict(X_test)
            if all_predictions_df is None:
                all_predictions_df = predictions_df
            else:
                all_predictions_df = all_predictions_df.append(predictions_df)

    possible_outcomes = [
        'Adoption', 'Died', 'Euthanasia', 'Return_to_owner', 'Transfer']
    ll = log_loss(
        all_y_test, 'OutcomeType', all_predictions_df, possible_outcomes)

    print "score: %.5f" % ll

    if ll < BEST_SCORE:
        all_test_predictions = None
        # Iterate over AnimalType
        for animal_type in ['Cat', 'Dog']:
            for is_adult in [0, 1]:
                test_data = test_data_sets[animal_type][is_adult]

                index = test_data.index.values
                predictor = predictors[animal_type][is_adult]

                # Retrain on *all* training data:
                train_data = train_data_sets[animal_type][is_adult]
                X = train_data.drop(['OutcomeType'], axis=1)
                y = train_data['OutcomeType']
                predictor.fit(X, y)
                test_predictions = predictor.predict(test_data)

                test_predictions['ID'] = index
                test_predictions = test_predictions.set_index('ID')
                if all_test_predictions is None:
                    all_test_predictions = test_predictions
                else:
                    all_test_predictions = all_test_predictions.append(
                        test_predictions)
        all_test_predictions = all_test_predictions.sort_index()
        columns = [
            'Adoption', 'Died', 'Euthanasia', 'Return_to_owner', 'Transfer']
        all_test_predictions.to_csv('../submissions/my_submission.csv',
                                    index=True, columns=columns)
