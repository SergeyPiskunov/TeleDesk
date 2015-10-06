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
        MyWin.resize(200, 350)
        #MyWin.setContentsMargins(-10, -10, -15, -25)
        MyWin.setWindowFlags(QtCore.Qt.CustomizeWindowHint)
        #MyWin.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        self.listView = QtGui.QListView(MyWin)
        self.listView.setObjectName(_fromUtf8("listView"))

        model = QtGui.QStandardItemModel(self.listView)
        for it in [' first', ' second', ' third', ' fourth']:
            item = QtGui.QStandardItem(it)
            model.appendRow(item)
        self.listView.setModel(model)


        self.retranslateUi(MyWin)
        QtCore.QMetaObject.connectSlotsByName(MyWin)

    def retranslateUi(self, MyWin):
        MyWin.setWindowTitle(_translate("MyWin", "TeleDesk v0.1", None))
        pass

