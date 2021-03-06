'''
Created on Apr 27, 2016

MyLLScore:     1.55686
KaggleLLScore:

@author: Paul Reiners
'''
from sklearn.ensemble import AdaBoostClassifier

from core.learning.classifiers.predictor_base import PredictorBase


class AdaBoostPredictor(PredictorBase):
    '''
    AdaBoost
    '''

    def __init__(self):
        self.clf = AdaBoostClassifier()

    def fit(self, X_train, y_train):
        self.clf.fit(X_train, y_train)

    def predict(self, X_test):
        predictions = self.clf.predict_proba(X_test)
        predictions_df = self.bundle_predictions(predictions)

        return predictions_df
