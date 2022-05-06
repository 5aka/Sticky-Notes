# -*- coding: utf-8 -*-

"""
Module implementing NoteMenu.
"""

from PyQt5.QtCore import pyqtSlot, Qt, pyqtSignal
from PyQt5.QtWidgets import QWidget

from Ui_myNoteMenu import Ui_NoteMenu


class NoteMenu(QWidget, Ui_NoteMenu):
    """
    Class documentation goes here.
    """
    index_signal = pyqtSignal(int)
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget (defaults to None)
        @type QWidget (optional)
        """
        super(NoteMenu, self).__init__(parent)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setupUi(self)
        self.radioButton_1.clicked.connect(lambda: self.sendSignal(1))
        self.radioButton_2.clicked.connect(lambda: self.sendSignal(2))
        self.radioButton_3.clicked.connect(lambda: self.sendSignal(3))
        self.radioButton_4.clicked.connect(lambda: self.sendSignal(4))
        self.radioButton_5.clicked.connect(lambda: self.sendSignal(5))
        self.radioButton_6.clicked.connect(lambda: self.sendSignal(6))
        self.radioButton_7.clicked.connect(lambda: self.sendSignal(7))

    def sendSignal(self, index):
        self.index_signal.emit(index)

        # self.hide()
        # self.radioButton_1

        for i in range(1, 8):
            btn = getattr(self, "radioButton_{}".format(i))
            if btn.text():
                btn.setText(None)
                break
        self.sender().setText("√")

