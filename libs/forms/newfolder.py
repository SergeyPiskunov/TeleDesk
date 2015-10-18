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


class NewGroupDialogUi(object):
    """ Creating new Group dialog.
        User interface definition """
    def setupUi(self, NewGroupWin):
        NewGroupWin.setObjectName(_fromUtf8("NewGroupWin"))
        NewGroupWin.resize(345, 114)
        self.verticalLayout = QtGui.QVBoxLayout(NewGroupWin)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.pushButtonCancel = QtGui.QPushButton(NewGroupWin)
        self.pushButtonCancel.setObjectName(_fromUtf8("pushButtonCancel"))
        self.gridLayout.addWidget(self.pushButtonCancel, 3, 2, 1, 1)
        self.pushButtonOk = QtGui.QPushButton(NewGroupWin)
        self.pushButtonOk.setObjectName(_fromUtf8("pushButtonOk"))
        self.pushButtonOk.setDefault(True)
        self.gridLayout.addWidget(self.pushButtonOk, 3, 1, 1, 1)
        self.labelGroupName = QtGui.QLabel(NewGroupWin)
        self.labelGroupName.setFrameShape(QtGui.QFrame.NoFrame)
        self.labelGroupName.setFrameShadow(QtGui.QFrame.Plain)
        self.labelGroupName.setObjectName(_fromUtf8("labelGroupName"))
        self.gridLayout.addWidget(self.labelGroupName, 1, 0, 1, 1)
        self.lineEditGroupName = QtGui.QLineEdit(NewGroupWin)
        self.lineEditGroupName.setObjectName(_fromUtf8("lineEditGroupName"))
        self.gridLayout.addWidget(self.lineEditGroupName, 1, 1, 1, 2)
        self.verticalLayout.addLayout(self.gridLayout)

        self.retranslateUi(NewGroupWin)
        QtCore.QMetaObject.connectSlotsByName(NewGroupWin)

    def retranslateUi(self, NewGroupWin):
        NewGroupWin.setWindowTitle(_translate("NewGroupWin", "New group", None))
        self.pushButtonCancel.setText(_translate("NewGroupWin", "Cancel", None))
        self.pushButtonOk.setText(_translate("NewGroupWin", "OK", None))


class NewGroupDialog(QtGui.QDialog):
    """ Dialog allows to create a new group"""
    def __init__(self, database, item_data=None):
        QtGui.QWidget.__init__(self, None)
        self.ui = NewGroupDialogUi()
        self.ui.setupUi(self)
        self.ui.pushButtonOk.clicked.connect(self.ok)
        self.ui.pushButtonCancel.clicked.connect(self.cancel)
        self.ui.labelGroupName.setText("Group name")
        self.database = database
        self.storage = item_data["Storage"]
        self.parent = item_data["Parent"]
        self.updated = False

    def ok(self):
        #write changes to database
        name = unicode(self.ui.lineEditGroupName.text())
        if len(name):
            self.database.create_new_group(**dict(database=self.storage, parent=self.parent, Name=name))
            self.updated = True
            self.close()

    def cancel(self):
        self.close()


if __name__ == "__main__":
    pass
