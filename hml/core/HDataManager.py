#!/usr/bin/python3.3
# coding=utf-8
"""
Data manager module.
"""
import numpy

from hml.io import HFile


__author__ = 'Hossein Noroozpour Thany Abady'
from sklearn.preprocessing import Imputer
from sklearn.preprocessing import scale
from sklearn.preprocessing import normalize
from sklearn.decomposition import PCA
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import BernoulliNB
from sklearn.naive_bayes import MultinomialNB
from sklearn.naive_bayes import GaussianNB
from sklearn.cross_validation import KFold
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from math import sqrt
from hml.classification.HNearestNeighborsClassifier import HNearestNeighboursClassifier
import time


class HDataManager():
    """
    Class for managing data.
    """
    def __init__(self, misimput='dni', trainfile='', testfile='', outfile=None):
        self.outfile = outfile
        self.classification_method = dict()
        self.model_selection_method = dict()
        self.classifier = None
        self.selector = None
        self.tr = None
        self.ta = None
        self.te = None
        self.trfile = trainfile
        self.tefile = testfile
        self.attributes = None
        self.test_features = HFile(testfile).data
        if misimput == 'dvi':
            tr = HFile(trainfile)
            te = HFile(testfile)
            self.attributes = tr.attributes
            self.class_index = tr.class_index
            self.tr = tr.data
            self.ta = tr.classes
            self.te = te.data
            print('Imputation mode: default value')
        elif misimput == 'ir':
            tr = HFile(trainfile, ignore_undefined=True)
            te = HFile(testfile, ignore_undefined=True)
            self.attributes = tr.attributes
            self.class_index = tr.class_index
            self.tr = tr.data
            self.ta = tr.classes
            self.te = te.data
            print('Imputation mode: ignore')
        elif misimput == 'mi':
            print('Imputation mode: mean value')
            self.mean_impute()
        elif misimput == 'mei':
            print('Imputation mode: median value')
            self.median_impute()
        elif misimput == 'mfi':
            print('Imputation mode: most frequent value')
            self.most_frequent_impute()
        else:
            raise Exception('Error: Unknown missing imputation method!')

    def mean_impute(self):
        """
        impute
        """
        tr = HFile(self.trfile)
        te = HFile(self.tefile)
        self.attributes = tr.attributes
        self.class_index = tr.class_index
        imp = Imputer(missing_values=-1)
        self.ta = tr.classes
        self.tr = imp.fit_transform(tr.data)
        self.te = imp.fit_transform(te.data)

    def median_impute(self):
        """
        impute
        """
        tr = HFile(self.trfile)
        te = HFile(self.tefile)
        self.attributes = tr.attributes
        self.class_index = tr.class_index
        imp = Imputer(missing_values=-1, strategy='median')
        self.tr = imp.fit_transform(tr.data)
        self.ta = tr.classes
        self.te = imp.fit_transform(te.data)

    def most_frequent_impute(self):
        """
        impute
        """
        tr = HFile(self.trfile)
        te = HFile(self.tefile)
        self.attributes = tr.attributes
        self.class_index = tr.class_index
        imp = Imputer(missing_values=-1, strategy='most_frequent')
        self.tr = imp.fit_transform(tr.data)
        self.ta = tr.classes
        self.te = imp.fit_transform(te.data)

    def standardize(self):
        """
        impute
        """
        print('Standardization')
        self.tr = scale(self.tr)
        self.te = scale(self.te)

    def normalize(self):
        """
        impute
        """
        print('Normalization')
        self.tr = normalize(self.tr)
        self.te = normalize(self.te)

    def do_pca(self, reduction_percentage=0.0):
        """
        impute
        :param reduction_percentage:
        """
        print('PCA with reduction percentage:', reduction_percentage)
        if len(self.tr[0]) != len(self.te[0]):
            raise Exception('Error in data!')
        n = int(len(self.tr[0]) * (100.0 - reduction_percentage))
        trpca = PCA(n).fit(self.tr)
        tepca = PCA(n).fit(self.te)
        self.tr = trpca.transform(self.tr)
        self.te = tepca.transform(self.te)
        print('Eigenvectors and eigenvalues for train set:')
        for i in range(len(trpca.explained_variance_)):
            print('\t', i, ': vector:', trpca.components_[i], '  value:', trpca.explained_variance_[i])
        print('Eigenvectors and eigenvalues for test set:')
        for i in range(len(tepca.explained_variance_)):
            print('\t', i, ': vector:', tepca.components_[i], '  value:', tepca.explained_variance_[i])

    def set_classification_method(self, method_name, method_parameter):
        """
        :param method_name:
        :param method_parameter:
        """
        print('Method name is:', method_name)
        if type(method_parameter) == str:
            print(method_parameter)
        else:
            for p in method_parameter.keys():
                print(p, ':', method_parameter[p])
        self.classification_method['name'] = method_name
        self.classification_method['parameters'] = method_parameter

    def set_model_selection_method(self, name, parameters):
        """
        :param name:
        :param parameters:
        """
        print('Method name is:', name)
        for p in parameters.keys():
            print(p, ':', parameters[p])
        self.model_selection_method['name'] = name
        self.model_selection_method['parameters'] = parameters

    def start_mining(self):
        """
        Start data mining routines.
        """
        p = self.classification_method['parameters']
        if 'decision tree' == self.classification_method['name']:
            self.classifier = [DecisionTreeClassifier(
                criterion=p['criterion'],
                max_features=p['maximum features'],
                max_depth=p['maximum depth'],
                min_samples_split=p['minimum samples split'],
                min_samples_leaf=p['minimum samples leaf'],
                random_state=p['random state'])]
        elif 'svm' == self.classification_method['name']:
            self.classifier = [SVC(
                C=p['fault penalty'],
                kernel=p['kernel type'],
                degree=p['kernel degree'],
                gamma=p['kernel gamma'],
                coef0=p['kernel coefficient'],
                tol=p['criterion tolerance'],
                class_weight=p['classes weights'],
                probability=p['probability estimation'],
                shrinking=p['shrinking heuristic'])]
        elif 'naive bayes' == self.classification_method['name']:
            if 'gaussian' == p:
                self.classifier = [GaussianNB()]
            elif 'multinomial' == p:
                self.classifier = [MultinomialNB()]
            elif 'bernoulli' == p:
                self.classifier = [BernoulliNB()]
            else:
                raise Exception('Error in: data manager->naive bayes')
        elif 'KNN' == self.classification_method['name']:
            if 'i' == p['distance influence']:
                weights = lambda l: [1. / (d + .0001) for d in l]
            elif 's' == p['distance influence']:
                weights = lambda l: [1. / (sqrt(d) + .0001) for d in l]
            elif 'd' == p['distance influence']:
                weights = lambda l: [1. - d for d in l]
            else:
                raise Exception('Error in: data manager->KNN')
            if 'single' == p['iteration']:
                self.classifier = [HNearestNeighboursClassifier(
                    n_neighbors=p['number of nearest neighbour'],
                    weight_function=weights,
                    weight_name=p['distance influence']
                )]
            elif 'multiple' == p['iteration']:
                start = p['number of nearest neighbour']
                end = p['number of nearest neighbour iterator']
                self.classifier = [HNearestNeighboursClassifier(
                    n_neighbors=i,
                    weight_function=weights,
                    weight_name=p['distance influence']) for i in range(start, end)]
            else:
                raise Exception('Error in: data manager->classification->KNN')
        p = self.model_selection_method['parameters']
        if 'k fold cross validation' == self.model_selection_method['name']:
            self.selector = KFold(len(self.ta), p['fold count'], shuffle=p['shuffle'])
        else:
            raise Exception('Error in: data manager->model selection->KFold')
        # Start ########################################################################################################
        self.ta = numpy.array(self.ta)
        self.tr = numpy.array(self.tr)
        for train_indices, test_indices in self.selector:
            x_train, x_test = self.tr[train_indices], self.tr[test_indices]
            y_train, y_test = self.ta[train_indices], self.ta[test_indices]
            for c in self.classifier:
                start_time = time.time()
                y_prob = c.fit(x_train, y_train).predict(x_test)
                print(c)
                print('Score:', c.score(x_test, y_test))
                print('Accuracy score:', accuracy_score(y_test, y_prob))
                print('Recall score:', recall_score(y_test, y_prob))
                print('Precision score:', precision_score(y_test, y_prob))
                print('F1 score:', f1_score(y_test, y_prob))
                print('Confusion matrix:', confusion_matrix(y_test, y_prob))
                print('It took ', time.time() - start_time, 's')
        # Save #########################################################################################################
        if self.outfile is not None and len(self.outfile) != 0:
            file_number = 0
            self.outfile += '/' + self.classification_method['name']
            for c in self.classifier:
                file_number += 1
                y_predicted = c.fit(self.tr, self.ta).predict(self.te)
                HFile.save_result(self.outfile + str(file_number) + '.txt',
                                  self.test_features,
                                  y_predicted,
                                  self.attributes,
                                  self.class_index)
            if self.classification_method['name'] == 'decision tree':
                from sklearn import tree
                tree.export_graphviz(self.classifier[0], out_file=self.outfile + '.dot')
