# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'new_folder_dialog.ui'
#
# Created: Mon Mar 30 23:18:37 2015
#      by: PyQt4 UI code generator 4.11.2
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

class NewFolderWindowUi(object):
    def setupUi(self, NewFolderWin):
        NewFolderWin.setObjectName(_fromUtf8("NewFolderWin"))
        NewFolderWin.resize(345, 114)
        self.verticalLayout = QtGui.QVBoxLayout(NewFolderWin)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.pushButtonCancel = QtGui.QPushButton(NewFolderWin)
        self.pushButtonCancel.setObjectName(_fromUtf8("pushButtonCancel"))
        self.gridLayout.addWidget(self.pushButtonCancel, 3, 2, 1, 1)
        self.pushButtonOk = QtGui.QPushButton(NewFolderWin)
        self.pushButtonOk.setObjectName(_fromUtf8("pushButtonOk"))
        self.gridLayout.addWidget(self.pushButtonOk, 3, 1, 1, 1)
        self.labelSpacer = QtGui.QLabel(NewFolderWin)
        self.labelSpacer.setText(_fromUtf8(""))
        self.labelSpacer.setObjectName(_fromUtf8("labelSpacer"))
        self.gridLayout.addWidget(self.labelSpacer, 3, 0, 1, 1)
        self.labelFolderName = QtGui.QLabel(NewFolderWin)
        self.labelFolderName.setFrameShape(QtGui.QFrame.NoFrame)
        self.labelFolderName.setFrameShadow(QtGui.QFrame.Plain)
        self.labelFolderName.setObjectName(_fromUtf8("labelFolderName"))
        self.gridLayout.addWidget(self.labelFolderName, 1, 0, 1, 1)
        self.lineEditFolderName = QtGui.QLineEdit(NewFolderWin)
        self.lineEditFolderName.setObjectName(_fromUtf8("lineEditFolderName"))
        self.gridLayout.addWidget(self.lineEditFolderName, 1, 1, 1, 2)
        self.labelParentName = QtGui.QLabel(NewFolderWin)
        self.labelParentName.setText(_fromUtf8(""))
        self.labelParentName.setObjectName(_fromUtf8("labelParentName"))
        self.gridLayout.addWidget(self.labelParentName, 0, 0, 1, 3)
        self.verticalLayout.addLayout(self.gridLayout)

        self.retranslateUi(NewFolderWin)
        QtCore.QMetaObject.connectSlotsByName(NewFolderWin)

    def retranslateUi(self, NewFolderWin):
        NewFolderWin.setWindowTitle(_translate("NewFolderWin", "New folder", None))
        self.pushButtonCancel.setText(_translate("NewFolderWin", "Cancel", None))
        self.pushButtonOk.setText(_translate("NewFolderWin", "OK", None))
        self.labelFolderName.setText(_translate("NewFolderWin", "Name", None))

