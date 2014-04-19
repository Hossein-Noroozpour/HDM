#!/usr/bin/python3.3
# coding=utf-8
"""
Data manager module.
"""
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
from sklearn.neighbors import KNeighborsClassifier
from math import sqrt
from HFile import HFile


class HDataManager():
    """
    Class for managing data.
    """
    def __init__(self, misimput='dni', trainfile='', testfile=''):
        self.classification_method = dict()
        self.model_selection_method = dict()
        self.classifier = None
        self.tr = None
        self.ta = None
        self.te = None
        self.trfile = trainfile
        self.tefile = testfile
        if misimput == 'dvi':
            tr = HFile(trainfile)
            te = HFile(testfile)
            self.tr = tr.data
            self.ta = tr.classes
            self.te = te.data
        elif misimput == 'ir':
            tr = HFile(trainfile, ignore_undefined=True)
            te = HFile(testfile, ignore_undefined=True)
            self.tr = tr.data
            self.ta = tr.classes
            self.te = te.data
        elif misimput == 'mi':
            self.mean_impute()
        elif misimput == 'mei':
            self.median_impute()
        elif misimput == 'mfi':
            self.mfimput()
        else:
            raise Exception('Error: Unknown missing imputation method!')

    def mean_impute(self):
        """
        impute
        """
        tr = HFile(self.trfile)
        te = HFile(self.tefile)
        imp = Imputer(missing_values=-1)
        self.tr = imp.fit_transform(tr.data)
        self.ta = imp.fit_transform(tr.classes)
        self.te = imp.fit_transform(te.data)

    def median_impute(self):
        """
        impute
        """
        tr = HFile(self.trfile)
        te = HFile(self.tefile)
        imp = Imputer(missing_values=-1, strategy='median')
        self.tr = imp.fit_transform(tr.data)
        self.ta = imp.fit_transform(tr.classes)
        self.te = imp.fit_transform(te.data)

    def mfimput(self):
        """
        impute
        """
        tr = HFile(self.trfile)
        te = HFile(self.tefile)
        imp = Imputer(missing_values=-1, strategy='most_frequent')
        self.tr = imp.fit_transform(tr.data)
        self.ta = imp.fit_transform(tr.classes)
        self.te = imp.fit_transform(te.data)

    def standardize(self):
        """
        impute
        """
        self.tr = scale(self.tr)
        self.te = scale(self.te)

    def normalize(self):
        """
        impute
        """
        self.tr = normalize(self.tr)
        self.te = normalize(self.te)

    def do_pca(self, reduction_percentage=0.0):
        """
        impute
        :param reduction_percentage:
        """
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
            self.classifier = DecisionTreeClassifier(
                criterion=p['criterion'],
                max_features=p['maximum features'],
                max_depth=p['maximum depth'],
                min_samples_split=p['minimum samples split'],
                min_samples_leaf=p['minimum samples leaf'],
                random_state=p['random state'])
        elif 'svm' == self.classification_method['name']:
            self.classifier = SVC(
                C=p['fault penalty'],
                kernel=p['kernel type'],
                degree=p['kernel degree'],
                gamma=p['kernel gamma'],
                coef0=p['kernel coefficient'],
                tol=p['coefficient tolerance'],
                class_weight=p['classes weights'],
                probability=p['probability estimation'],
                shrinking=p['shrinking heuristic']
            )
        elif 'naive bayes' == self.classification_method['name']:
            if 'gaussian' == p:
                self.classifier = GaussianNB()
            elif 'multinomial' == p:
                self.classifier = MultinomialNB()
            elif 'bernoulli' == p:
                self.classifier = BernoulliNB()
            else:
                raise Exception('Error in: data manager->naive bayes')
        elif 'KNN' == self.classification_method['name']:
            if 'i' == p['distance influence']:
                weights = 'distance'
            elif 's' == p['distance influence']:
                weights = lambda l: map(lambda d: 1. / (sqrt(d) + .0001), l)
            elif 'd' == p['distance influence']:
                weights = lambda l: map(lambda d: 1. - d, l)
            else:
                raise Exception('Error in: data manager->KNN')
            if 'single' == p['iteration']:
                self.classifier = [KNeighborsClassifier(
                    n_neighbors=p['number of nearest neighbour'],
                    weights=weights
                )]
            elif 'multiple' == p['iteration']:
                start = p['number of nearest neighbour']
                end = p['number of nearest neighbour iterator']
                self.classifier = [KNeighborsClassifier(n_neighbors=i, weights=weights) for i in range(start, end)]
            else:
                raise Exception('Error in: data manager->classification->KNN')
        