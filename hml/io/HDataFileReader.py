#!/usr/bin/python3.3
# coding=utf-8
"""
Module for file reading.
"""
__author__ = 'Hossein Noroozpour Thany Abady'


class DataFileReader():
    """
    Class for raw data reading.
    It does not change data and just read them and store them in 2 dimensional list.
    File format must be like this:
        d12<splitter>d12<splitter>d13<splitter>d14<splitter>d15<new line>
        d22<splitter>d22<splitter>d23<splitter>d24<splitter>d25<new line>
            ...
            ...
            ...
    """
    def __init__(self, file_name):
        self.file = open(file_name)

    def get_data(self, splitter=',', element_function=lambda x: x):
        """
        :param element_function:
        :param splitter:
        :return:
        """
        return [[element_function(e.strip()) for e in line.split(splitter)] for line in self.file]