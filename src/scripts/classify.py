'''
Created on May 25, 2016

@author: Paul Reiners

Based on
["Workflows in Python: Using Pipeline and GridSearchCV for More Compact and
 Comprehensive Code"]
(https://civisanalytics.com/blog/data-science/2016/01/06/workflows-python-using-pipeline-gridsearchcv-for-compact-code/)
by Katie Malone
'''
import sklearn.ensemble
import sklearn.feature_selection
import sklearn.metrics
import sklearn.pipeline
from core.preprocessing.feature_extraction_scaling import get_data
from core.preprocessing.feature_selection import select_raw_features


if __name__ == '__main__':
    for animal_type in ['Cat', 'Dog']:
        print animal_type
        for is_adult in [0, 1]:
            print "is_adult:", is_adult
            train_data = get_data('../data/train.csv')
            train_data = train_data[train_data.SexuponOutcome.notnull()]
            train_data = train_data[train_data.AgeuponOutcome.notnull()]
            train_data = train_data[train_data['AnimalType'] == animal_type]
            train_data = train_data.drop(['AnimalType'], axis=1)
            train_data = select_raw_features(train_data, animal_type)
            train_data = train_data.dropna()
            train_data = train_data[train_data['IsAdult'] == is_adult]

            X = train_data.drop(['OutcomeType'], axis=1)
            y = train_data['OutcomeType']

            select = sklearn.feature_selection.SelectKBest(k=100)
            clf = sklearn.ensemble.RandomForestClassifier()

            steps = [('feature_selection', select),
                     ('random_forest', clf)]

            pipeline = sklearn.pipeline.Pipeline(steps)

            X_train, X_test, y_train, y_test = \
                sklearn.cross_validation.train_test_split(
                    X, y, test_size=0.33, random_state=42)

            # fit your pipeline on X_train and y_train
            pipeline.fit(X_train, y_train)
            # call pipeline.predict() on your X_test data to make a set of test
            # predictions
            y_prediction = pipeline.predict(X_test)
            # test your predictions using sklearn.classification_report()
            report = sklearn.metrics.classification_report(
                y_test, y_prediction)
            # and print the report
            print(report)