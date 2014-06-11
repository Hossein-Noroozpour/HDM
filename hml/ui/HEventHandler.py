#!/usr/bin/python3
# coding=utf-8
"""
Module for GUI Event Handling.
"""
from hml.core import HDataManager

__author__ = 'Hossein Noroozpour Thany Abady'
from gi.repository import Gtk


class HEventHandler():
    """
    Class for handling gui events.
    """

    def __init__(self, builder):
        self.builder = builder

    def on_start_clicked(self, widget):
        """
        Starts mining process.
        :param widget:
        :return: :raise 'Error in classification section!':
        """
        builder = self.builder
        obj = builder.get_object
        print('Button:', widget.get_label(), ' pressed.')
        train_file = builder.get_object('intrfcb').get_filename()
        testfile = builder.get_object('intefcb').get_filename()
        outfile = builder.get_object('outfcb').get_filename()
        if train_file is None:
            dialog = Gtk.MessageDialog(0, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.CLOSE, "File Error")
            dialog.format_secondary_text('Please specify a train file before clicking on start button.')
            dialog.run()
            dialog.destroy()
            return
        if testfile is None:
            dialog = Gtk.MessageDialog(0, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.CLOSE, "File Error")
            dialog.format_secondary_text('Please specify a test file before clicking on start button.')
            dialog.run()
            dialog.destroy()
            return
        if builder.get_object('dvirb').get_active():
            data_manager = HDataManager('dvi', train_file, testfile, outfile)
        elif builder.get_object('irrb').get_active():
            data_manager = HDataManager('ir', train_file, testfile, outfile)
        elif builder.get_object('mirb').get_active():
            data_manager = HDataManager('mi', train_file, testfile, outfile)
        elif builder.get_object('meirb').get_active():
            data_manager = HDataManager('mei', train_file, testfile, outfile)
        elif builder.get_object('mfirb').get_active():
            data_manager = HDataManager('mfi', train_file, testfile, outfile)
        else:
            raise Exception('Error in missing part!')
        if builder.get_object('rrb').get_active():
            pass
        elif builder.get_object('nrb').get_active():
            data_manager.normalize()
        elif builder.get_object('srb').get_active():
            data_manager.standardize()
        else:
            raise Exception('Error in manipulation part!')
        if builder.get_object('dnrrb').get_active():
            pass
        elif builder.get_object('pcarb').get_active():
            data_manager.do_pca(builder.get_object('drps').get_value())
        else:
            raise Exception('Error in dimention reduction!')
        # Begin of classification ###############################################################
        if builder.get_object('cdtrb').get_active():
            if self.classification_decision_tree(data_manager) is False:
                return
        elif builder.get_object('csvmrb').get_active():
            if self.classification_support_vector_machine(data_manager) is False:
                return
        elif builder.get_object('cnbrb').get_active():
            if self.classification_naive_bayes(data_manager) is False:
                return
        elif builder.get_object('cknnrb').get_active():
            if self.classification_k_nearest_neighbour(data_manager) is False:
                return
        else:
            raise Exception('Error in classification section.')
        # End of classification #################################################################
        # Begin of model selection ##############################################################
        if obj('mskfoldrb').get_active():
            if self.model_selection_k_fold_cross_validation(data_manager) is False:
                return
        else:
            raise Exception('Error in model selection section.')
        # End of model selection ################################################################
        data_manager.start_mining()

    @staticmethod
    def on_window_close(*args):
        """
        End of program.
        :param args:
        """
        Gtk.main_quit(*args)

    def on_classification_changed(self, radio_button):
        """

        :param radio_button:
        :raise Exception:
        """
        builder = self.builder
        if radio_button.get_label() == 'Decision tree':
            frame = builder.get_object('cdtdtpf')
        elif radio_button.get_label() == 'Support Vector Machine':
            frame = builder.get_object('csvmsvmpf')
        elif radio_button.get_label() == 'Naive Bayes':
            frame = builder.get_object('cnbnbpf')
        elif radio_button.get_label() == 'K Nearest Neighbours':
            frame = builder.get_object('cknnknnpf')
        else:
            raise Exception('Error in classification change!')
        if radio_button.get_active():
            frame.show()
        else:
            frame.hide()

    def on_model_selection_changed(self, radio_button):
        """

        :param radio_button:
        :raise Exception:
        """
        builder = self.builder
        if radio_button.get_label() == 'K Fold Cross-Validation':
            frame = builder.get_object('mskfcvpf')
        elif radio_button.get_label() == 'Grid Search':
            frame = builder.get_object('msgspf')
        else:
            raise Exception('Error in model selection change!')
        if radio_button.get_active():
            frame.show()
        else:
            frame.hide()

    def classification_decision_tree(self, data_manager):
        """
        :param data_manager:
        :return False or None
        :raise Exception:
        """
        obj = self.builder.get_object
        # Criterion ##########################################################################
        if obj('cdcginirb').get_active():
            criterion = 'gini'
        elif obj('cdcentropyrb').get_active():
            criterion = 'entropy'
        else:
            raise Exception('Error in classification->decision tree->criterion!')
        # Maximum features ##################################################################
        if obj('cdmfdefaultrb').get_active():
            maximum_feature = None
        elif obj('cdmfautorb').get_active():
            maximum_feature = 'auto'
        elif obj('cdmfsqrtrb').get_active():
            maximum_feature = 'sqrt'
        elif obj('cdmflog2rb').get_active():
            maximum_feature = 'log2'
        elif obj('cdmfmnfrb').get_active():
            try:
                maximum_feature = int(obj('cdmfmnfe').get_text())
            except ValueError:
                dialog = Gtk.MessageDialog(0, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.CLOSE, "Max Feature Error")
                dialog.format_secondary_text('Please specify a correct number of features before clicking on start '
                                             'button.')
                dialog.run()
                dialog.destroy()
                return False
        elif obj('cdmfmpcrb').get_active():
            try:
                maximum_feature = float(obj('cdmfmpce').get_text())
            except ValueError:
                dialog = Gtk.MessageDialog(0, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.CLOSE, "Max Feature Error")
                dialog.format_secondary_text('Please specify a correct percentage of features before clicking on start '
                                             'button.')
                dialog.run()
                dialog.destroy()
                return False
        else:
            raise Exception('Error in classification->decision tree->maximum features')
        # Maximum Depth #######################################################################
        max_depth = None
        if obj('cdmddefaultrb').get_active():
            pass
        elif obj('cdmdmndrb').get_active():
            try:
                max_depth = int(obj('cdmdmnde').get_text())
            except ValueError:
                dialog = Gtk.MessageDialog(0, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.CLOSE, "Max Depth Error")
                dialog.format_secondary_text('Please specify a correct maximum depth number before clicking on start '
                                             'button.')
                dialog.run()
                dialog.destroy()
                return False
        else:
            raise Exception('Error in classification->decision tree->maximum depth')
        # Minimum Sample Split ################################################################
        min_samples_split = 2
        if obj('cdmssdefaultrb').get_active():
            pass
        elif obj('cdmssmnssrb').get_active():
            try:
                min_samples_split = int(obj('cdmssmnsse').get_text())
            except ValueError:
                dialog = Gtk.MessageDialog(0, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.CLOSE, "Minimum Samples Split "
                                                                                               "Error")
                dialog.format_secondary_text('Please specify a correct minimum sample split number before clicking on '
                                             'start button.')
                dialog.run()
                dialog.destroy()
                return False
        else:
            raise Exception('Error in classification->decision tree->minimum samples split')
        # Minimum Samples Leaf ################################################################
        min_samples_leaf = 1
        if obj('cdmsldefaultrb').get_active():
            pass
        elif obj('cdmslmnslrb').get_active():
            try:
                min_samples_leaf = int(obj('cdmslmnsle').get_text())
            except ValueError:
                dialog = Gtk.MessageDialog(0, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.CLOSE, "Minimum Samples Leaf "
                                                                                               "Error")
                dialog.format_secondary_text('Please specify a correct minimum sample leaf number before clicking on '
                                             'start button.')
                dialog.run()
                dialog.destroy()
                return False
        else:
            raise Exception('Error in classification->decision tree->minimum samples leaf')
        # Random State #######################################################################
        random_state = None
        if obj('cdrsdefaultrb').get_active():
            pass
        elif obj('cdmslmnslrb').get_active():
            try:
                min_samples_leaf = int(obj('cdmslmnsle').get_text())
            except ValueError:
                dialog = Gtk.MessageDialog(0, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.CLOSE, "Minimum Samples Leaf "
                                                                                               "Error")
                dialog.format_secondary_text('Please specify a correct minimum sample leaf number before clicking on '
                                             'start button.')
                dialog.run()
                dialog.destroy()
                return False
        else:
            raise Exception('Error in classification->decision tree->minimum samples leaf')
        parameters = dict()
        parameters['criterion'] = criterion
        parameters['maximum features'] = maximum_feature
        parameters['maximum depth'] = max_depth
        parameters['minimum samples split'] = min_samples_split
        parameters['minimum samples leaf'] = min_samples_leaf
        parameters['random state'] = random_state
        data_manager.set_classification_method('decision tree', parameters)

    def classification_support_vector_machine(self, data_manager):
        """
        On error condition abort process.
        :param data_manager:
        :return False on error
        :raise Exception:
        """
        obj = self.builder.get_object
        try:
            fault_penalty = float(obj('csvmfpmpe').get_text().strip())
        except ValueError:
            dialog = Gtk.MessageDialog(0, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.CLOSE, 'Input Number Error')
            dialog.format_secondary_text('Please specify a correct fault penalty before clicking on start button.')
            dialog.run()
            dialog.destroy()
            return False
        if obj('csvmktlrb').get_active():
            kernel_type = 'linear'
        elif obj('csvmktrbfrb').get_active():
            kernel_type = 'rbf'
        elif obj('csvmktpolyrb').get_active():
            kernel_type = 'poly'
        elif obj('csvmktsigmoidrb').get_active():
            kernel_type = 'sigmoid'
        else:
            raise Exception('Error in classification->SVM->kernel type')
        try:
            kernel_degree = int(obj('csvmkde').get_text().strip())
        except ValueError:
            dialog = Gtk.MessageDialog(0, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.CLOSE, 'Input Number Error')
            dialog.format_secondary_text('Please specify a correct kernel degree before clicking on start button.')
            dialog.run()
            dialog.destroy()
            return False
        try:
            kernel_gamma = float(obj('csvmkge').get_text().strip())
        except ValueError:
            dialog = Gtk.MessageDialog(0, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.CLOSE, 'Input Number Error')
            dialog.format_secondary_text('Please specify a correct kernel gamma before clicking on start button.')
            dialog.run()
            dialog.destroy()
            return False
        try:
            kernel_coefficient = float(obj('csvmkce').get_text().strip())
        except ValueError:
            dialog = Gtk.MessageDialog(0, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.CLOSE, 'Input Number Error')
            dialog.format_secondary_text('Please specify a correct kernel coefficient before clicking on start button.')
            dialog.run()
            dialog.destroy()
            return False
        try:
            criterion_tolerance = float(obj('csvmcte').get_text().strip())
        except ValueError:
            dialog = Gtk.MessageDialog(0, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.CLOSE, 'Input Number Error')
            dialog.format_secondary_text('Please specify a correct criterion tolerance '
                                         'before clicking on start button.')
            dialog.run()
            dialog.destroy()
            return False
        if obj('csvmcwdrb').get_active():
            classes_weights = 'auto'
        elif obj('csvmcwmwrb').get_active():
            try:
                classes_weights = [float(s) for s in obj('csvmcwmwe').get_text().strip().split(',')]
            except ValueError:
                dialog = Gtk.MessageDialog(0, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.CLOSE, 'Input Number Error')
                dialog.format_secondary_text('Please specify a correct class weight before clicking on start button.')
                dialog.run()
                dialog.destroy()
                return False
        else:
            raise Exception('Error in classification->svm->classes weights')
        probability_estimation = obj('csvmoopecb').get_active()
        shrink_heuristic = obj('csvmooshcb').get_active()
        parameters = dict()
        parameters['fault penalty'] = fault_penalty
        parameters['kernel type'] = kernel_type
        parameters['kernel degree'] = kernel_degree
        parameters['kernel gamma'] = kernel_gamma
        parameters['kernel coefficient'] = kernel_coefficient
        parameters['criterion tolerance'] = criterion_tolerance
        parameters['classes weights'] = classes_weights
        parameters['probability estimation'] = probability_estimation
        parameters['shrinking heuristic'] = shrink_heuristic
        data_manager.set_classification_method('svm', parameters)

    def classification_naive_bayes(self, data_manager):
        """
        :param data_manager:
        """
        obj = self.builder.get_object
        if obj('cnbgnbrb').get_active():
            bayes_method = 'gaussian'
        elif obj('cnbmnnbrb').get_active():
            bayes_method = 'multinomial'
        elif obj('cnbbnbrb').get_active():
            bayes_method = 'bernoulli'
        else:
            raise Exception('Error in classification->bayes->method')
        data_manager.set_classification_method('naive bayes', bayes_method)

    def classification_k_nearest_neighbour(self, data_manager):
        """
        :param data_manager:
        """
        obj = self.builder.get_object
        if obj('cknnirb').get_active():
            iteration = 'single'
        elif obj('cknniirb').get_active():
            iteration = 'multiple'
        else:
            raise Exception('Error in classification->KNN->iteration')
        try:
            number_nearest_neighbour = int(obj('cknnnnne').get_text().strip())
        except ValueError:
            dialog = Gtk.MessageDialog(0, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.CLOSE, 'Input Number Error')
            dialog.format_secondary_text('Please specify a correct number of nearest neighbour before clicking on start'
                                         ' button.')
            dialog.run()
            dialog.destroy()
            return False
        number_nearest_neighbour_iterator = None
        if iteration == 'multiple':
            try:
                number_nearest_neighbour_iterator = int(obj('cknnnnnie').get_text().strip())
            except ValueError:
                dialog = Gtk.MessageDialog(0, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.CLOSE, 'Input Number Error')
                dialog.format_secondary_text('Please specify a correct number of nearest neighbour iterator before '
                                             'clicking on start button.')
                dialog.run()
                dialog.destroy()
                return False
        if obj('cknndiirb').get_active():
            distance_effect = 'i'
        elif obj('cknndisrb').get_active():
            distance_effect = 's'
        elif obj('cknndidrb').get_active():
            distance_effect = 'd'
        else:
            raise Exception('Error in classification->KNN->distance influence')
        parameters = dict()
        parameters['iteration'] = iteration
        parameters['number of nearest neighbour'] = number_nearest_neighbour
        if iteration == 'multiple':
            parameters['number of nearest neighbour iterator'] = number_nearest_neighbour_iterator
        parameters['distance influence'] = distance_effect
        data_manager.set_classification_method('KNN', parameters)

    def model_selection_k_fold_cross_validation(self, data_manager):
        """
        :param data_manager:
        :return:
        """
        obj = self.builder.get_object
        try:
            number_fold = int(obj('mskfcvnfe').get_text().strip())
        except ValueError:
            dialog = Gtk.MessageDialog(0, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.CLOSE, 'Input Number Error')
            dialog.format_secondary_text('Please specify a correct number of fold before clicking on start button.')
            dialog.run()
            dialog.destroy()
            return False
        shuffle = obj('mskfcvooscb').get_active()
        parameters = dict()
        parameters['fold count'] = number_fold
        parameters['shuffle'] = shuffle
        data_manager.set_model_selection_method('k fold cross validation', parameters)
