#!/usr/bin/python3.3
__author__ = 'Hossein Noroozpour Thany Abady'
from sklearn.preprocessing import Imputer
from sklearn.preprocessing import scale
from sklearn.preprocessing import normalize
from sklearn.decomposition import PCA
from HFile import HFile
class HDataManager():
    def __init__(self, misimput='dni', trainfile='', testfile=''):
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
            self.meanimput()
        elif misimput == 'mei':
            self.medianimput()
        elif misimput == 'mfi':
            self.mfimput()
        else:
            raise 'Error: Unknown missing imputation method!'
    def meanimput(self):
        tr = HFile(self.trfile)
        te = HFile(self.tefile)
        imp = Imputer(missing_values=-1, strategy='mean')
        self.tr = imp.fit_transform(tr.data)
        self.ta = imp.fit_transform(tr.classes)
        self.te = imp.fit_transform(te.data)
    def medianimput(self):
        tr = HFile(self.trfile)
        te = HFile(self.tefile)
        imp = Imputer(missing_values=-1, strategy='median')
        self.tr = imp.fit_transform(tr.data)
        self.ta = imp.fit_transform(tr.classes)
        self.te = imp.fit_transform(te.data)
    def mfimput(self):
        tr = HFile(self.trfile)
        te = HFile(self.tefile)
        imp = Imputer(missing_values=-1, strategy='most_frequent')
        self.tr = imp.fit_transform(tr.data)
        self.ta = imp.fit_transform(tr.classes)
        self.te = imp.fit_transform(te.data)
    def standardize(self):
        self.tr = scale(self.tr)
        self.te = scale(self.te)
    def normalize(self):
        self.tr = normalize(self.tr)
        self.te = normalize(self.te)
    def doPCA(self, reduction_percentage=0.0):
        if len(self.tr[0]) != len(self.te[0]):
            raise 'Error in data!'
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
        pass