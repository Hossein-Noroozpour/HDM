#!/usr/bin/python3
# coding=utf-8
"""
Module for initializing.
"""
__author__ = 'Hossein Noroozpour Thany Abady'
from gi.repository import Gtk
from hml.ui.HEventHandler import HEventHandler
import sys


class HGUI():
    """
    GUI Initializer.
    """

    def __init__(self, glade_file='hml/ui/gui.glade'):
        self.builder = Gtk.Builder()
        self.builder.add_from_file(glade_file)
        event_handler = HEventHandler(self.builder)
        self.builder.connect_signals(event_handler)
        self.get_object('main_window').show_all()
        self.get_object('csvmsvmpf').hide()
        self.get_object('cnbnbpf').hide()
        self.get_object('cknnknnpf').hide()
        self.get_object('msgspf').hide()

    def get_object(self, name):
        """
        :param name:
        :return:
        """
        return self.builder.get_object(name)


if '__main__' == __name__:
    if len(sys.argv) > 1 and sys.argv[1] == 'test-001':
        from hml.testunits.test_001 import test001
        for features_count in range(4, 13):
            arg_lists = [
                ['std', features_count, 'decision-tree'],
                ['nrm', features_count, 'decision-tree'],
                ['std', features_count, 'SVM'],
                ['nrm', features_count, 'SVM'],
                ['std', features_count, 'naive-bayes', 'GMB'],
                ['std', features_count, 'naive-bayes', 'MNB'],
                ['std', features_count, 'naive-bayes', 'BNB'],
                ['nrm', features_count, 'naive-bayes', 'GNB'],
                ['nrm', features_count, 'naive-bayes', 'MNB'],
                ['nrm', features_count, 'naive-bayes', 'BNB'],
                ['std', features_count, 'KNN', 3, 'uniform'],
                ['std', features_count, 'KNN', 4, 'uniform'],
                ['std', features_count, 'KNN', 5, 'uniform'],
                ['std', features_count, 'KNN', 6, 'uniform'],
                ['std', features_count, 'KNN', 7, 'uniform'],
                ['std', features_count, 'KNN', 8, 'uniform'],
                ['std', features_count, 'KNN', 9, 'uniform'],
                ['std', features_count, 'KNN', 3, 'distance'],
                ['std', features_count, 'KNN', 4, 'distance'],
                ['std', features_count, 'KNN', 5, 'distance'],
                ['std', features_count, 'KNN', 6, 'distance'],
                ['std', features_count, 'KNN', 7, 'distance'],
                ['std', features_count, 'KNN', 8, 'distance'],
                ['std', features_count, 'KNN', 9, 'distance'],
                ['nrm', features_count, 'KNN', 3, 'uniform'],
                ['nrm', features_count, 'KNN', 4, 'uniform'],
                ['nrm', features_count, 'KNN', 5, 'uniform'],
                ['nrm', features_count, 'KNN', 6, 'uniform'],
                ['nrm', features_count, 'KNN', 7, 'uniform'],
                ['nrm', features_count, 'KNN', 8, 'uniform'],
                ['nrm', features_count, 'KNN', 9, 'uniform'],
                ['nrm', features_count, 'KNN', 3, 'distance'],
                ['nrm', features_count, 'KNN', 4, 'distance'],
                ['nrm', features_count, 'KNN', 5, 'distance'],
                ['nrm', features_count, 'KNN', 6, 'distance'],
                ['nrm', features_count, 'KNN', 7, 'distance'],
                ['nrm', features_count, 'KNN', 8, 'distance'],
                ['nrm', features_count, 'KNN', 9, 'distance'],
            ]
            for arg_list in arg_lists:
                test001(arg_list)
    else:
        h = HGUI()
        Gtk.main()