# -*- coding: utf-8 -*-

"""
Module implementing Note.
"""

from PyQt5.QtCore import pyqtSlot, Qt, QTextStream, QFile
from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout, QLineEdit, QPushButton, QSizeGrip, QFileDialog
from PyQt5.QtGui import QFont, QTextCharFormat, QTextDocumentFragment, QTextListFormat

from Ui_myNote import Ui_Note
from CustomWidgets.CDrawer import CDrawer
from myNoteMenu import NoteMenu
from DeleteNoteDialog import DeleteNote


class Note(QWidget, Ui_Note):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget (defaults to None)
        @type QWidget (optional)
        """
        super(Note, self).__init__(parent)
        self.setupUi(self)
        # 初始qss样式
        self.setBackground(1)
        # 设置背景透明
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        # 设置无边框
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        # 标题栏移动
        def moveWindow(event):
            # IF LEFT CLICK MOVE WINDOW
            if event.buttons() == Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.dragPos)
                self.dragPos = event.globalPos()
                event.accept()

        self.frame_title.mouseMoveEvent = moveWindow
        # 右下角，调整窗口大小
        self.sizegrip = QSizeGrip(self.frame_grip)
        self.sizegrip.setStyleSheet(
            "QSizeGrip { width: 10px; height: 10px; margin: 5px }")
        self.sizegrip.setToolTip("Resize Window")

        # 一些背景颜色
        # self.titleColor = ["255, 242, 171", "203, 241, 196", "255, 204, 229", "231, 207, 255", "205, 233, 255", "225, 223, 221", "73, 71, 69"]
        # self.buttomColor = ["255, 247, 209", "228, 249, 224", "255, 228, 241", "242, 230, 255", "226, 241, 255", "243, 242, 241", "105, 105, 105"]
        # self.hoverColor = ["229, 222, 188", "205, 224, 201", "229, 205, 216", "225, 214, 237", "191, 217, 237", "226, 225, 224", "116, 116, 116"]

    def mousePressEvent(self, event):
        self.dragPos = event.globalPos()


    @pyqtSlot()
    def on_pushButton_add_clicked(self):
        """
        Add a new window
        """
        newNote = Note()
        newNote.show()
    
    @pyqtSlot()
    def on_pushButton_menu_clicked(self):
        """
        Slot documentation goes here.
        """
        if not hasattr(self, 'topDrawer'):
            self.topDrawer = CDrawer(self, stretch=0.5, direction=CDrawer.TOP)
            self.noteMenu = NoteMenu(self.topDrawer)
            # 发送背景切换的信号
            self.noteMenu.index_signal.connect(self.setBackground)
            # 切换背景后执行退出动画
            self.noteMenu.index_signal.connect(self.topDrawer.animationOut)
            # Delete按钮槽函数绑定
            self.noteMenu.pushButton_delete.clicked.connect(self.deleteNote)
            self.topDrawer.setWidget(self.noteMenu)
        self.topDrawer.show()

    def deleteNote(self):
        # 先退出动画
        self.topDrawer.animationOut()
        # 再弹窗询问
        deleteNote = DeleteNote(self)
        deleteNote.delete_signal.connect(self.setClosed)
        deleteNote.exec_()

    def setClosed(self, closed):
        if closed:
            self.close()

    def setBackground(self, colorIndex):
        # colorIndex -= 1
        # self.frame_title.setStyleSheet("background-color: rgb({});".format(self.titleColor[colorIndex]))
        # self.textBrowser.setStyleSheet("border:none;font: 14pt \"MingLiU-ExtB\";background-color: rgb({});"
        #                                .format(self.buttomColor[colorIndex]))
        # self.frame_buttom.setStyleSheet("background-color: rgb({});".format(self.buttomColor[colorIndex]))
        #
        # for i in ["add", "menu", "close", "bold", "italic", "list", "picture", "strikethrough", "underscore"]:
        #     btn = getattr(self, "pushButton_{}".format(i))
        #     btn.setStyleSheet("QPushButton{{border:none;}}QPushButton:hover{{background: rgb({0});}}QPushButton:checked{{background: rgb({1});}}"
        #                       .format(self.hoverColor[colorIndex], self.hoverColor[colorIndex]))

        file = QFile(":/qss/resources/{}.qss".format(colorIndex))
        file.open(QFile.ReadOnly)
        ts = QTextStream(file)
        ts.setCodec("utf-8")
        styles = ts.readAll()
        self.setStyleSheet(styles)

    @pyqtSlot()
    def on_pushButton_close_clicked(self):
        """
        Close Window
        """
        self.close()
    
    @pyqtSlot(bool)
    def on_pushButton_bold_clicked(self, checked):
        """
        是否加粗
        
        @param checked DESCRIPTION
        @type bool
        """
        if checked:
            self.textBrowser.setFontWeight(QFont.Bold)
        else:
            self.textBrowser.setFontWeight(QFont.Normal)
    
    @pyqtSlot(bool)
    def on_pushButton_italic_clicked(self, checked):
        """
        斜体
        
        @param checked DESCRIPTION
        @type bool
        """
        self.textBrowser.setFontItalic(checked)

    
    @pyqtSlot(bool)
    def on_pushButton_underscore_clicked(self, checked):
        """
        下划线
        
        @param checked DESCRIPTION
        @type bool
        """
        self.textBrowser.setFontUnderline(checked)
    
    @pyqtSlot(bool)
    def on_pushButton_strikethrough_clicked(self, checked):
        """
        Slot documentation goes here.
        
        @param checked DESCRIPTION
        @type bool
        """
        # self.textBrowser.setFontStrikeOut(checked)
    
    @pyqtSlot(QTextCharFormat)
    def on_textBrowser_currentCharFormatChanged(self, format):
        """
        Slot documentation goes here.
        
        @param format DESCRIPTION
        @type QTextCharFormat
        """
        # format = QTextCharFormat()
        if format.fontWeight() == QFont.Bold:
            self.pushButton_bold.setChecked(True)
        else:
            self.pushButton_bold.setChecked(False)

        self.pushButton_italic.setChecked(format.fontItalic())
        self.pushButton_underscore.setChecked(format.fontUnderline())
        self.pushButton_strikethrough.setChecked(format.fontStrikeOut())
    
    @pyqtSlot(bool)
    def on_pushButton_list_clicked(self, checked):
        """
        列表
        
        @param checked DESCRIPTION
        @type bool
        """
        if checked:
            format = QTextListFormat()
            format.setStyle(QTextListFormat.ListDisc)
            self.textBrowser.textCursor().insertList(format)

    
    @pyqtSlot()
    def on_pushButton_picture_clicked(self):
        """
        插入图片
        """
        imgName, imgType = QFileDialog.getOpenFileName(self, "Open", "",
                                                       "*.jpg;;*.jpeg;;*.png;;*.bmp;;*.gif;;All Files(*.jpg;*.jpeg;*.png;*.bmp;*.gif)")
        fragment = QTextDocumentFragment.fromHtml("<img src = '{}'>".format(imgName))
        self.textBrowser.textCursor().insertFragment(fragment)



if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    ui = Note()
    ui.show()
    sys.exit(app.exec_())
