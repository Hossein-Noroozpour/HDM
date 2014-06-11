#!/usr/bin/python3
# coding=utf-8
"""
Module for initializing.
"""
from gi.repository import Gtk
from hml.ui.HEventHandler import HEventHandler


__author__ = 'Hossein Noroozpour Thany Abady'


class HGUI():
    """
    GUI Initializer.
    """

    def __init__(self, glade_file='hml//ui//gui.glade'):
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
    h = HGUI()
    Gtk.main()