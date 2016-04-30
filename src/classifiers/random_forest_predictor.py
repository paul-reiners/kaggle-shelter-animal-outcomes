'''
Created on Apr 27, 2016

MyLLScore:     0.82221
KaggleLLScore: 0.84454

@author: Paul Reiners
'''
from sklearn import grid_search
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2

from classifiers.predictor_base import PredictorBase
from util import get_data, preprocess_data


class RandomForestPredictor(PredictorBase):
    '''
    Random Forest
    '''

    def __init__(self, animal_type):
        self.animal_type = animal_type
        self.clf = RandomForestClassifier(
            max_depth=8, n_estimators=320, max_features=4)
        self.k_best_k = 16

    def fit(self, X_train, y_train):
        self.clf.fit(X_train, y_train)

    def predict(self, X_test):
        predictions = self.clf.predict_proba(X_test)
        predictions_df = self.bundle_predictions(predictions)

        return predictions_df

    def find_best_params(self):
        parameters = {
            'n_estimators': [160, 320, 640, 1280],
            'max_depth': [2, 4, 8, 16],
            'max_features': [1, 2, 4, 8, self.k_best_k]}
        rf = RandomForestClassifier()
        clf = grid_search.GridSearchCV(rf, parameters)
        train_data = get_data('../../data/train.csv')
        train_data = train_data[train_data['AnimalType'] == self.animal_type]
        train_data = preprocess_data(train_data)
        train_data = train_data.dropna()
        X = train_data.drop(['OutcomeType'], axis=1)
        y = train_data['OutcomeType']
        k_best = SelectKBest(chi2, k=self.k_best_k)
        X = k_best.fit_transform(X, y)
        clf.fit(X, y)
        print clf.best_params_

    def get_k_best_k(self):
        return self.k_best_k

if __name__ == '__main__':
    print 'Cat'
    predictor = RandomForestPredictor('Cat')
    predictor.find_best_params()
    print 'Dog'
    predictor = RandomForestPredictor('Dog')
    predictor.find_best_params()
