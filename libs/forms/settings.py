# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\serj\PycharmProjects\input.ui'
#
# Created: Sun Oct 04 21:32:01 2015
#      by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_UserSettingsWin(object):
    def setupUi(self, UserSettingsWindow):
        UserSettingsWindow.setObjectName(_fromUtf8("UserSettingsWindow"))
        UserSettingsWindow.resize(565, 321)
        self.verticalLayout = QtGui.QVBoxLayout(UserSettingsWindow)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.tabWidget = QtGui.QTabWidget(UserSettingsWindow)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.tableWidgetLocalStorage = QtGui.QTableWidget(self.tab)
        self.tableWidgetLocalStorage.setGeometry(QtCore.QRect(-5, 31, 551, 251))
        self.tableWidgetLocalStorage.setObjectName(_fromUtf8("tableWidgetLocalStorage"))
        self.tableWidgetLocalStorage.setColumnCount(0)
        self.tableWidgetLocalStorage.setRowCount(0)
        self.tabWidget.addTab(self.tab, _fromUtf8(""))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.tableWidgetFTPStorage = QtGui.QTableWidget(self.tab_2)
        self.tableWidgetFTPStorage.setGeometry(QtCore.QRect(0, 30, 541, 251))
        self.tableWidgetFTPStorage.setObjectName(_fromUtf8("tableWidgetFTPStorage"))
        self.tableWidgetFTPStorage.setColumnCount(0)
        self.tableWidgetFTPStorage.setRowCount(0)
        self.tabWidget.addTab(self.tab_2, _fromUtf8(""))
        self.verticalLayout.addWidget(self.tabWidget)

        self.retranslateUi(UserSettingsWindow)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(UserSettingsWindow)

    def retranslateUi(self, UserSettingsWindow):
        UserSettingsWindow.setWindowTitle(_translate("UserSettingsWindow", "Settings", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("UserSettingsWindow", "Local storage", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("UserSettingsWindow", "FTP storage", None))

