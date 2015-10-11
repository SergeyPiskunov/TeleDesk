# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\serj\PycharmProjects\helloworld.ui'
#
# Created: Fri Oct 09 21:59:43 2015
# by: PyQt4 UI code generator 4.11.3
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


class SettingsWindowUi(object):
    def setupUi(self, UserSettingsWindow):
        UserSettingsWindow.setObjectName(_fromUtf8("UserSettingsWindow"))
        UserSettingsWindow.resize(591, 270)
        self.verticalLayout = QtGui.QVBoxLayout(UserSettingsWindow)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.tabWidget = QtGui.QTabWidget(UserSettingsWindow)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.generalTab = QtGui.QWidget()
        self.generalTab.setObjectName(_fromUtf8("generalTab"))
        self.formLayoutWidget_2 = QtGui.QWidget(self.generalTab)
        self.formLayoutWidget_2.setGeometry(QtCore.QRect(290, 10, 271, 171))
        self.formLayoutWidget_2.setObjectName(_fromUtf8("formLayoutWidget_2"))
        self.generalTabRight = QtGui.QFormLayout(self.formLayoutWidget_2)
        self.generalTabRight.setMargin(0)
        self.generalTabRight.setObjectName(_fromUtf8("generalTabRight"))
        self.formLayoutWidget_5 = QtGui.QWidget(self.generalTab)
        self.formLayoutWidget_5.setGeometry(QtCore.QRect(10, 10, 271, 171))
        self.formLayoutWidget_5.setObjectName(_fromUtf8("formLayoutWidget_5"))
        self.generalTabLeft = QtGui.QFormLayout(self.formLayoutWidget_5)
        self.generalTabLeft.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.generalTabLeft.setMargin(0)
        self.generalTabLeft.setObjectName(_fromUtf8("generalTabLeft"))
        self.langLabel = QtGui.QLabel(self.formLayoutWidget_5)
        self.langLabel.setObjectName(_fromUtf8("langLabel"))
        self.generalTabLeft.setWidget(0, QtGui.QFormLayout.LabelRole, self.langLabel)
        self.comboBox = QtGui.QComboBox(self.formLayoutWidget_5)
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.generalTabLeft.setWidget(0, QtGui.QFormLayout.FieldRole, self.comboBox)
        self.lineEdit = QtGui.QLineEdit(self.formLayoutWidget_5)
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.generalTabLeft.setWidget(2, QtGui.QFormLayout.FieldRole, self.lineEdit)
        self.masterPasswordcheckBox = QtGui.QCheckBox(self.formLayoutWidget_5)
        self.masterPasswordcheckBox.setObjectName(_fromUtf8("masterPasswordcheckBox"))
        self.generalTabLeft.setWidget(2, QtGui.QFormLayout.LabelRole, self.masterPasswordcheckBox)
        self.resetButton = QtGui.QPushButton(self.formLayoutWidget_5)
        self.resetButton.setObjectName(_fromUtf8("resetButton"))
        self.generalTabLeft.setWidget(3, QtGui.QFormLayout.FieldRole, self.resetButton)
        self.tabWidget.addTab(self.generalTab, _fromUtf8(""))
        self.localStorageTab = QtGui.QWidget()
        self.localStorageTab.setObjectName(_fromUtf8("localStorageTab"))
        self.localStorageTableView = QtGui.QTableView(self.localStorageTab)
        self.localStorageTableView.setGeometry(QtCore.QRect(0, 40, 561, 151))
        self.localStorageTableView.setObjectName(_fromUtf8("localStorageTableView"))
        self.formLayoutWidget_3 = QtGui.QWidget(self.localStorageTab)
        self.formLayoutWidget_3.setGeometry(QtCore.QRect(0, 10, 161, 25))
        self.formLayoutWidget_3.setObjectName(_fromUtf8("formLayoutWidget_3"))
        self.localStorageLayout = QtGui.QFormLayout(self.formLayoutWidget_3)
        self.localStorageLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.localStorageLayout.setMargin(0)
        self.localStorageLayout.setObjectName(_fromUtf8("localStorageLayout"))
        self.addLocalStorageButton = QtGui.QPushButton(self.formLayoutWidget_3)
        self.addLocalStorageButton.setObjectName(_fromUtf8("addLocalStorageButton"))
        self.localStorageLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.addLocalStorageButton)
        self.deleteLocalStorageButton = QtGui.QPushButton(self.formLayoutWidget_3)
        self.deleteLocalStorageButton.setObjectName(_fromUtf8("deleteLocalStorageButton"))
        self.localStorageLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.deleteLocalStorageButton)
        self.tabWidget.addTab(self.localStorageTab, _fromUtf8(""))
        self.FTPStorageTab = QtGui.QWidget()
        self.FTPStorageTab.setObjectName(_fromUtf8("FTPStorageTab"))
        self.FTPStorageTableView = QtGui.QTableView(self.FTPStorageTab)
        self.FTPStorageTableView.setGeometry(QtCore.QRect(0, 40, 561, 151))
        self.FTPStorageTableView.setObjectName(_fromUtf8("FTPStorageTableView"))
        self.formLayoutWidget_4 = QtGui.QWidget(self.FTPStorageTab)
        self.formLayoutWidget_4.setGeometry(QtCore.QRect(0, 10, 161, 25))
        self.formLayoutWidget_4.setObjectName(_fromUtf8("formLayoutWidget_4"))
        self.FTPStorageLayout = QtGui.QFormLayout(self.formLayoutWidget_4)
        self.FTPStorageLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.FTPStorageLayout.setMargin(0)
        self.FTPStorageLayout.setObjectName(_fromUtf8("FTPStorageLayout"))
        self.addFTPStorageButton = QtGui.QPushButton(self.formLayoutWidget_4)
        self.addFTPStorageButton.setObjectName(_fromUtf8("addFTPStorageButton"))
        self.FTPStorageLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.addFTPStorageButton)
        self.deleteFTPStorageButton = QtGui.QPushButton(self.formLayoutWidget_4)
        self.deleteFTPStorageButton.setObjectName(_fromUtf8("deleteFTPStorageButton"))
        self.FTPStorageLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.deleteFTPStorageButton)
        self.tabWidget.addTab(self.FTPStorageTab, _fromUtf8(""))
        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.blanklabel1 = QtGui.QLabel(UserSettingsWindow)
        self.blanklabel1.setText(_fromUtf8(""))
        self.blanklabel1.setObjectName(_fromUtf8("blanklabel1"))
        self.horizontalLayout.addWidget(self.blanklabel1)
        self.blanklabel2 = QtGui.QLabel(UserSettingsWindow)
        self.blanklabel2.setText(_fromUtf8(""))
        self.blanklabel2.setObjectName(_fromUtf8("blanklabel2"))
        self.horizontalLayout.addWidget(self.blanklabel2)
        self.OKButton = QtGui.QPushButton(UserSettingsWindow)
        self.OKButton.setObjectName(_fromUtf8("OKButton"))
        self.horizontalLayout.addWidget(self.OKButton)
        self.CancelButton = QtGui.QPushButton(UserSettingsWindow)
        self.CancelButton.setObjectName(_fromUtf8("CancelButton"))
        self.horizontalLayout.addWidget(self.CancelButton)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(UserSettingsWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(UserSettingsWindow)

    def retranslateUi(self, UserSettingsWindow):
        UserSettingsWindow.setWindowTitle(_translate("UserSettingsWindow", "Settings", None))
        self.langLabel.setText(_translate("UserSettingsWindow", "Language", None))
        self.masterPasswordcheckBox.setText(_translate("UserSettingsWindow", "use master passord", None))
        self.resetButton.setText(_translate("UserSettingsWindow", "Reset to defaults", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.generalTab),
                                  _translate("UserSettingsWindow", "General", None))
        self.addLocalStorageButton.setText(_translate("UserSettingsWindow", "Add", None))
        self.deleteLocalStorageButton.setText(_translate("UserSettingsWindow", "Delete", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.localStorageTab),
                                  _translate("UserSettingsWindow", "Local storage", None))
        self.addFTPStorageButton.setText(_translate("UserSettingsWindow", "Add", None))
        self.deleteFTPStorageButton.setText(_translate("UserSettingsWindow", "Delete", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.FTPStorageTab),
                                  _translate("UserSettingsWindow", "FTP storage", None))
        self.OKButton.setText(_translate("UserSettingsWindow", "Save", None))
        self.CancelButton.setText(_translate("UserSettingsWindow", "Cancel", None))


class SettingsTableModel(QtCore.QAbstractTableModel):
    def __init__(self, databases, column_structure, parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self.databases = databases
        self.column_structure = column_structure


    def rowCount(self, parent):
        return len(self.databases)

    def columnCount(self, parent):
        if len(self.databases):
            return len(self.databases[0].keys())
        else:
            return len(self.column_structure)

    def flags(self, index):
        return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    def data(self, index, role):

        if role == QtCore.Qt.DisplayRole:
            row = index.row()
            column = index.column()
            return self.databases[row].values()[column]

        if role == QtCore.Qt.EditRole:
            row = index.row()
            column = index.column()
            return self.databases[row].values()[column]

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        if role == QtCore.Qt.EditRole:
            row = index.row()
            column = index.column()
            self.databases[row][self.databases[row].keys()[column]] = unicode(value.toPyObject())
            self.dataChanged.emit(index, index)
            return True
        return False

    def headerData(self, section, orientation, role):

        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                if len(self.databases):
                    return self.databases[0].keys()[section]
                else:
                    return self.column_structure.keys()[section]
            else:
                return QtCore.QString("Storage %1").arg(section + 1)

    def insertRow(self, int_row, parent=QtCore.QAbstractItemModel):
        self.beginInsertRows(parent, 1, 1)
        self.databases.append(self.column_structure)
        self.endInsertRows()

        return True

    def removeRow(self, int_row, parent):
        self.beginRemoveRows(parent, int_row, int_row)
        del self.databases[int_row]
        self.endRemoveRows()

        return True

    def insertColumns(self, position, columns, parent=QtCore.QModelIndex()):
        self.beginInsertColumns(parent, position, position + columns - 1)

        rowCount = len(self.databases)

        for i in range(columns):
            for j in range(rowCount):
                self.databases[j].insert(position, QtGui.QColor("#000000"))

        self.endInsertColumns()

        return True
