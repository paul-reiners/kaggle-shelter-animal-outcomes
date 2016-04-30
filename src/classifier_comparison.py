'''
Created on Apr 29, 2016

Based on [Classifier comparison]
(http://scikit-learn.org/stable/auto_examples/classification/plot_classifier_comparison.html).

@author: Paul Reiners
'''
import time

from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2

from classifiers.ada_boost_predictor import AdaBoostPredictor
from classifiers.decision_tree_predictor import DecisionTreePredictor
from classifiers.linear_descriminant_analysis_predictor \
    import LinearDiscriminantAnalysisPredictor
from classifiers.naive_bayes_predictor import NaiveBayesPredictor
from classifiers.nearest_neighbors_predictor import NearestNeighborsPredictor
from classifiers.quadratic_descriminant_analysis_predictor \
    import QuadraticDiscriminantAnalysisPredictor
from classifiers.random_forest_predictor import RandomForestPredictor
from util import get_data, split_data, log_loss, preprocess_data


if __name__ == '__main__':
    names = ["Nearest Neighbors", "Decision Tree",
             "Random Forest", "AdaBoost", "Naive Bayes",
             "Linear Discriminant Analysis", "Quadratic Discriminant Analysis"]
    # Slow: "Linear SVM", "RBF SVM"
    possible_outcomes = [
        'Adoption', 'Died', 'Euthanasia', 'Return_to_owner', 'Transfer']
    # Iterate over AnimalType
    for animal_type in ['Cat', 'Dog']:
        classifiers = [
            NearestNeighborsPredictor(),
            DecisionTreePredictor(),
            RandomForestPredictor(animal_type),
            AdaBoostPredictor(),
            NaiveBayesPredictor(),
            LinearDiscriminantAnalysisPredictor(),
            QuadraticDiscriminantAnalysisPredictor()]
        # Slow: LinearSVMPredictor(), RBF_SVMPredictor()

        train_data = get_data('../data/train.csv')
        print animal_type
        train_data = train_data[train_data['AnimalType'] == animal_type]
        train_data = train_data.drop(['AnimalType'], axis=1)
        train_data = preprocess_data(train_data)
        train_data = train_data.dropna()
        X_train, y_train, X_test, y_test = split_data(train_data)
        # k
        #  5: 0.92539 (no warning)
        #  6: 0.84462 (no warning)
        #  8: 0.85657 (1 warning)
        # 10: 0.89024 (1 warning)

        # iterate over classifiers
        for name, clf in zip(names, classifiers):
            k_best = SelectKBest(chi2, k=clf.get_k_best_k())
            clf_X_train = k_best.fit_transform(X_train, y_train)
            clf_X_test = k_best.transform(X_test)

            print "\t{} {}".format(name, time.ctime())
            clf.fit(clf_X_train, y_train)
            predictions_df = clf.predict(clf_X_test)
            ll = log_loss(
                y_test, 'OutcomeType', predictions_df, possible_outcomes)

            print "\t\tscore: %.5f\n" % ll
