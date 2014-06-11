#!/usr/bin/python3.3
# coding=utf-8
"""
Module for file reading.
"""
__author__ = 'Hossein Noroozpour Thany Abady'


class HFile():
    """
    Class for file reading.
    """
    def __init__(self, file_name, ignore_undefined=False, verbose=0):
        """
        :param file_name: File path + file name
        """
        file = open(file_name)
        self.relation = None
        self.attributes = list()
        self.classes = list()
        self.data = list()
        line_number = 0
        self.class_index = -1
        attribute_index = 0
        for line in file:
            line_number += 1
            if '@attribute' == line[0:10]:
                lbind = line.find('{')
                attname = line[11: lbind].strip()
                if attname == 'class':
                    self.class_index = attribute_index
                attribute_index += 1
                if 0 < verbose:
                    print('Attribute is:', attname)
                attvals = [val.strip() for val in line[lbind + 1:line.find('}')].split(',')]
                if 0 < verbose:
                    print('Attribute values is:', attvals)
                if attname in self.attributes:
                    print('Duplicated attribute definition. Attribute is:', attname)
                    print('Error in input file line:', line_number)
                    exit(1)
                self.attributes.append([attname, attvals])
            elif '@relation' == line[0:9]:
                if 0 < verbose:
                    print('Relation  is:', line[10:].strip())
            elif '@data' == line[0:5]:
                break
        if 1 < verbose:
            print('Header is:', self.attributes)
        for line in file:
            line_number += 1
            args = [arg.strip() for arg in line.split(',')]
            data = list()
            ignored = False
            for i in range(len(args)):
                if i == self.class_index:
                    try:
                        self.classes.append(self.attributes[i][1].index(args[i]))
                    except ValueError:
                        if ignore_undefined:
                            ignored = True
                            break
                        if "?" == args[i]:
                            self.classes.append(-1)
                            if 2 < verbose:
                                print('Undefined class!')
                        else:
                            print("Error in file data reading line:", line_number)
                            print(args[i], " is not in ", self.attributes[i][0])
                            exit(1)
                else:
                    try:
                        data.append(self.attributes[i][1].index(args[i]))
                    except ValueError:
                        if ignore_undefined:
                            ignored = True
                            break
                        if "?" == args[i]:
                            data.append(-1)
                            if 2 < verbose:
                                print('Undefined!')
                        else:
                            print("Error in file data reading line:", line_number)
                            print(args[i], " is not in ", self.attributes[i][0])
                            exit(1)
            if (self.class_index != -1 and len(data) != len(self.attributes) - 1) or\
                    (self.class_index == -1 and len(data) != len(self.attributes)):
                if ignored:
                    continue
                print('Error in file::', file_name, ' line:', line_number)
                print("number of component are not equal to attributes.")
                exit(1)
            self.data.append(data)

    @staticmethod
    def save_result(file_name, features, labels, attributes, label_index):
        """
        :param file_name:
        :param features:
        :param labels:
        :param attributes:
        :param label_index:
        """
        f = open(file_name, 'w')
        s = '@relation car\n\n'
        for a in attributes:
            s += '@attribute ' + a[0] + '        {'
            for i in range(len(a[1]) - 1):
                s += a[1][i] + ', '
            s += a[1][len(a[1]) - 1] + '}\n'
        s += '\n\n@data\n'
        for k in range(len(labels)):
            d = features[k]
            l = labels[k]
            for i in range(len(d)):
                if d[i] == -1:
                    s += '?,'
                else:
                    s += attributes[i][1][d[i]] + ','
            s += attributes[label_index][1][l] + '\n'
        s += '\n\n\n'
        f.write(s)
        f.close()

if '__main__' == __name__:
    hf = HFile('/run/media/thany/AE1247021246CF51/Users'
            '/Thany/Documents/Lessons/DataMining/first/DM-Project-1/data.arff')