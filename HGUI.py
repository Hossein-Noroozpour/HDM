# coding=utf-8
"""
Module for GUI initializing.
"""
from gi.repository import Gtk
from HEventHandler import HEventHandler

__author__ = 'Hossein Noroozpour Thany Abady'


class HGUI():
    """
    GUI Initializer.
    """

    def __init__(self, glade_file='gui.glade'):
        self.builder = Gtk.Builder()
        self.builder.add_from_file(glade_file)
        self.builder.connect_signals(HEventHandler(self.builder))
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