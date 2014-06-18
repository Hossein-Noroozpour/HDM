#!/usr/bin/python3.3
__author__ = 'Hossein Noroozpour Thany Abady'
from hml.core.HDataEncoderM2 import EncM2
from sklearn.preprocessing import scale
from sklearn.preprocessing import normalize
from sklearn.decomposition import PCA
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import MultinomialNB
from sklearn.naive_bayes import BernoulliNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.cross_validation import KFold


def test001(arg_list):
    e = EncM2('/run/media/thany/AE1247021246CF51/Users/Thany/Documents/Lessons' +
              '/DataMining/second/DMC_task_2014/orders_train.txt')
    print("Encoding done.")
    if arg_list[0] == 'std':
        preprocess = scale
    elif arg_list[0] == 'nrm':
        preprocess = normalize
    else:
        print('Error in command line arguments.')
        raise 0
    pca = PCA(int(arg_list[1]))
    if arg_list[2] == 'decision-tree':
        classifier = DecisionTreeClassifier()
    elif arg_list[2] == 'SVM':
        classifier = SVC()
    elif arg_list[2] == 'naive-bayes':
        if arg_list[3] == 'GNB':
            classifier = GaussianNB()
        elif arg_list[3] == 'MNB':
            classifier = MultinomialNB()
        elif arg_list[3] == 'BNB':
            classifier = BernoulliNB()
        else:
            print('Error in command line arguments.')
            raise 0
    elif arg_list[2] == 'KNN':
        #arg_list[4] := 'uniform' or 'distance'
        classifier = KNeighborsClassifier(int(arg_list[3]), arg_list[4])
    else:
        print('Error in command line arguments.')
        raise 0
    selection = KFold(e.datlen)
    print(arg_list)
    for train_index, test_index in selection:
        x_train = e.data[train_index]
        y_train = e.target[train_index]
        x_test = e.data[test_index]
        y_test = e.target[test_index]
        print("Selection is done.")
        x_train = preprocess(x_train)
        x_test = preprocess(x_test)
        print("Pre-processing done.")
        x_train = pca.fit_transform(x_train)
        x_test = pca.fit_transform(x_test)
        print('PCA done.')
        classifier.fit(x_train, y_train)
        print('Score for model is :', classifier.score(x_test, y_test))