# -*- coding: utf-8 -*-


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

class Ui_MainWindow(object):
    def setupUi(self, MyWin):
        MyWin.setObjectName(_fromUtf8("MyWin"))
        MyWin.resize(443, 379)
        self.verticalLayout = QtGui.QVBoxLayout(MyWin)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))

        self.pushButtonAdd = QtGui.QPushButton(MyWin)
        self.pushButtonAdd.setObjectName(_fromUtf8("pushButtonAdd"))
        self.gridLayout.addWidget(self.pushButtonAdd, 0, 0, 1, 1)

        self.pushButtonAddFolder = QtGui.QPushButton(MyWin)
        self.pushButtonAddFolder.setObjectName(_fromUtf8("pushButtonAddFolder"))
        self.gridLayout.addWidget(self.pushButtonAddFolder, 0, 1, 1, 1)

        self.pushButtonEdit = QtGui.QPushButton(MyWin)
        self.pushButtonEdit.setObjectName(_fromUtf8("pushButtonEdit"))
        self.gridLayout.addWidget(self.pushButtonEdit, 0, 2, 1, 1)

        self.pushButtonRemove = QtGui.QPushButton(MyWin)
        self.pushButtonRemove.setObjectName(_fromUtf8("pushButtonRemove"))
        self.gridLayout.addWidget(self.pushButtonRemove, 0, 3, 1, 1)

        self.treeView = QtGui.QTreeView(MyWin)
        self.treeView.setObjectName(_fromUtf8("treeView"))
        self.treeView.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.gridLayout.addWidget(self.treeView, 1, 0, 1, 3)

        self.textEditDescription = QtGui.QTextEdit(MyWin)
        self.textEditDescription.setObjectName(_fromUtf8("textEditDescription"))
        self.gridLayout.addWidget(self.textEditDescription, 1, 3, 1, 1)
        self.labelStatus = QtGui.QLabel(MyWin)
        self.labelStatus.setText(_fromUtf8(""))
        self.labelStatus.setObjectName(_fromUtf8("labelStatus"))
        self.gridLayout.addWidget(self.labelStatus, 2, 0, 1, 4)
        self.verticalLayout.addLayout(self.gridLayout)

        self.retranslateUi(MyWin)
        QtCore.QMetaObject.connectSlotsByName(MyWin)

    def retranslateUi(self, MyWin):
        MyWin.setWindowTitle(_translate("MyWin", "TeleDesk v0.1", None))
        self.pushButtonAdd.setText(_translate("MyWin", "Add server", None))
        self.pushButtonAddFolder.setText(_translate("MyWin", "Add folder", None))
        self.pushButtonEdit.setText(_translate("MyWin", "Edit", None))
        self.pushButtonRemove.setText(_translate("MyWin", "Remove", None))



