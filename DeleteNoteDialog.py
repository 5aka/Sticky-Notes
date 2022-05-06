# -*- coding: utf-8 -*-

"""
Module implementing DeleteNote.
"""

from PyQt5.QtCore import pyqtSlot, pyqtSignal, Qt
from PyQt5.QtWidgets import QDialog, QApplication

from Ui_DeleteNoteDialog import Ui_DeleteNote


class DeleteNote(QDialog, Ui_DeleteNote):
    """
    Class documentation goes here.
    """
    delete_signal = pyqtSignal(int)
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget (defaults to None)
        @type QWidget (optional)
        """
        super(DeleteNote, self).__init__(parent)
        self.setupUi(self)
        # 设置背景透明
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        # 设置无边框
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        # 固定大小
    
    @pyqtSlot()
    def on_pushButton_yes_clicked(self):
        """
        Slot documentation goes here.
        """
        self.delete_signal.emit(1)
        self.close()
    
    @pyqtSlot()
    def on_pushButton_no_clicked(self):
        """
        Slot documentation goes here.
        """
        self.delete_signal.emit(0)
        self.close()
    
    @pyqtSlot(bool)
    def on_checkBox_clicked(self, checked):
        """
        Slot documentation goes here.
        
        @param checked DESCRIPTION
        @type bool
        """
        self.pushButton_no.setDisabled(checked)


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    ui = DeleteNote()
    ui.show()
    sys.exit(app.exec_())