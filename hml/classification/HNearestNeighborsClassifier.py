#!/usr/bin/python3.3
# coding=utf-8
"""
Module for K nearest neighbours.
"""

__author__ = 'Hossein Noroozpour Thany Abady'

#from math3d import sqrt
import numpy


class HNearestNeighboursClassifier():
    """
    Class for K nearest neighbors algorithm.
    """

    def __init__(self, n_neighbors=5, weight_function=lambda l: [1. / (d + .0001) for d in l], weight_name='i'):
        self.n_neighbors = n_neighbors
        self.weight_function = weight_function
        self.train = None
        self.target = None
        self.weight_name = weight_name

    def fit(self, train, target):
        """
        :param train:
        :param target:
        """
        self.train = numpy.array(train)
        self.target = target
        return self

    def predict(self, test):
        """
        :param test:
        """
        result = []
        test = numpy.array(test)
        for t in test:
            distances = []
            for r in self.train:
                d = r - t
                distances.append(sqrt(d.dot(d)))
            weights = self.weight_function(distances)
            wc = [(weights[i], self.target[i]) for i in range(len(self.target))]
            wc.sort(key=lambda tup: tup[0], reverse=True)
            v = dict()
            for i in range(self.n_neighbors):
                if v.get(wc[i][1]) is None:
                    v[wc[i][1]] = 1
                else:
                    v[wc[i][1]] += 1
            vote = 0
            c = 0
            for k in v.keys():
                if v[k] >= vote:
                    c = k
            result.append(c)
        return result

    def __str__(self):
        return 'K nearest neighbors classifier with n=' + str(self.n_neighbors) + ' and weight=' + str(self.weight_name)

    def score(self, x, y):
        """
        :param x:
        :param y:
        """
        p = self.predict(x)
        c = 0
        for i in range(len(y)):
            if p[i] == y[i]:
                c += 1
        return float(c) / float(len(y))