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

class ItemEditWindowUi(object):
    def setupUi(self, EditWin):
        EditWin.setObjectName(_fromUtf8("EditWin"))
        EditWin.setFixedSize(QtCore.QSize(450, 380))
        self.verticalLayout = QtGui.QVBoxLayout(EditWin)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.tabWidgetSettings = QtGui.QTabWidget(EditWin)
        self.tabWidgetSettings.setObjectName(_fromUtf8("tabWidgetSettings"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.layoutWidget = QtGui.QWidget(self.tab)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 10, 408, 161))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.gridLayout = QtGui.QGridLayout(self.layoutWidget)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.labelName = QtGui.QLabel(self.layoutWidget)
        self.labelName.setObjectName(_fromUtf8("labelName"))
        self.gridLayout.addWidget(self.labelName, 0, 0, 1, 1)
        self.labelStatus = QtGui.QLabel(self.layoutWidget)
        self.labelStatus.setText(_fromUtf8(""))
        self.labelStatus.setObjectName(_fromUtf8("labelStatus"))
        self.gridLayout.addWidget(self.labelStatus, 0, 2, 1, 2)
        self.labelServer = QtGui.QLabel(self.layoutWidget)
        self.labelServer.setObjectName(_fromUtf8("labelServer"))
        self.gridLayout.addWidget(self.labelServer, 1, 0, 1, 1)
        self.labelUsername = QtGui.QLabel(self.layoutWidget)
        self.labelUsername.setMidLineWidth(14)
        self.labelUsername.setObjectName(_fromUtf8("labelUsername"))
        self.gridLayout.addWidget(self.labelUsername, 2, 0, 1, 1)
        self.labelDomain = QtGui.QLabel(self.layoutWidget)
        self.labelDomain.setObjectName(_fromUtf8("labelDomain"))
        self.gridLayout.addWidget(self.labelDomain, 3, 0, 1, 1)
        self.lineEditName = QtGui.QLineEdit(self.layoutWidget)
        self.lineEditName.setObjectName(_fromUtf8("lineEditName"))
        self.gridLayout.addWidget(self.lineEditName, 0, 1, 1, 1)
        self.lineEditServer = QtGui.QLineEdit(self.layoutWidget)
        self.lineEditServer.setObjectName(_fromUtf8("lineEditServer"))
        self.gridLayout.addWidget(self.lineEditServer, 1, 1, 1, 1)
        self.lineEditDomain = QtGui.QLineEdit(self.layoutWidget)
        self.lineEditDomain.setObjectName(_fromUtf8("lineEditDomain"))
        self.gridLayout.addWidget(self.lineEditDomain, 3, 1, 1, 1)
        self.lineEditUser = QtGui.QLineEdit(self.layoutWidget)
        self.lineEditUser.setObjectName(_fromUtf8("lineEditUser"))
        self.gridLayout.addWidget(self.lineEditUser, 2, 1, 1, 1)
        self.labelPassword = QtGui.QLabel(self.layoutWidget)
        self.labelPassword.setObjectName(_fromUtf8("labelPassword"))
        self.gridLayout.addWidget(self.labelPassword, 4, 0, 1, 1)
        self.lineEditPassword = QtGui.QLineEdit(self.layoutWidget)
        self.lineEditPassword.setObjectName(_fromUtf8("lineEditPassword"))
        self.gridLayout.addWidget(self.lineEditPassword, 4, 1, 1, 1)
        self.labelPort = QtGui.QLabel(self.layoutWidget)
        self.labelPort.setObjectName(_fromUtf8("labelPort"))
        self.gridLayout.addWidget(self.labelPort, 1, 2, 1, 1)
        self.lineEditPort = QtGui.QLineEdit(self.layoutWidget)
        self.lineEditPort.setObjectName(_fromUtf8("lineEditPort"))
        self.gridLayout.addWidget(self.lineEditPort, 1, 3, 1, 1)
        self.checkBoxShowPassword = QtGui.QCheckBox(self.layoutWidget)
        self.checkBoxShowPassword.setObjectName(_fromUtf8("checkBoxShowPassword"))
        self.gridLayout.addWidget(self.checkBoxShowPassword, 4, 2, 1, 2)
        self.tabWidgetSettings.addTab(self.tab, _fromUtf8(""))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.tabWidgetSettings.addTab(self.tab_2, _fromUtf8(""))
        self.verticalLayout.addWidget(self.tabWidgetSettings)
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.pushButtonClose = QtGui.QPushButton(EditWin)
        self.pushButtonClose.setObjectName(_fromUtf8("pushButtonClose"))
        self.gridLayout_2.addWidget(self.pushButtonClose, 0, 2, 1, 1)
        self.pushButtonSave = QtGui.QPushButton(EditWin)
        self.pushButtonSave.setObjectName(_fromUtf8("pushButtonSave"))
        self.gridLayout_2.addWidget(self.pushButtonSave, 0, 1, 1, 1)
        self.labelspacer = QtGui.QLabel(EditWin)
        self.labelspacer.setText(_fromUtf8(""))
        self.labelspacer.setObjectName(_fromUtf8("labelspacer"))
        self.gridLayout_2.addWidget(self.labelspacer, 0, 0, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout_2)

        self.retranslateUi(EditWin)
        self.tabWidgetSettings.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(EditWin)

    def retranslateUi(self, EditWin):
        EditWin.setWindowTitle(_translate("EditWin", "Edit", None))
        self.labelName.setText(_translate("EditWin", "Name", None))
        self.labelServer.setText(_translate("EditWin", "Server", None))
        self.labelUsername.setText(_translate("EditWin", "User", None))
        self.labelDomain.setText(_translate("EditWin", "Domain", None))
        self.labelPassword.setText(_translate("EditWin", "Password", None))
        self.labelPort.setText(_translate("EditWin", "Port", None))
        self.checkBoxShowPassword.setText(_translate("EditWin", "Show password", None))
        self.tabWidgetSettings.setTabText(self.tabWidgetSettings.indexOf(self.tab), _translate("EditWin", "Main", None))
        self.tabWidgetSettings.setTabText(self.tabWidgetSettings.indexOf(self.tab_2), _translate("EditWin", "Advanced", None))
        self.pushButtonClose.setText(_translate("EditWin", "Close", None))
        self.pushButtonSave.setText(_translate("EditWin", "Save", None))


class ItemEditDialog(QtGui.QDialog):
    def __init__(self, ds, item_data=None):
        self.ds = ds
        self.storage_name = item_data["Storage"]
        self.updated = False
        self.parent = item_data["Parent"]
        QtGui.QWidget.__init__(self, None)
        self.ui = ItemEditWindowUi()
        self.ui.setupUi(self)
        if item_data["Mode"] == "Edit":
            self.item_to_edit = item_data["ItemData"]["Profile"]
            self.ui.lineEditName.setText(item_data["ItemData"]["Name"])
            self.ui.lineEditServer.setText(item_data["ItemData"]["Server"])
            self.ui.lineEditPort.setText(item_data["ItemData"]["Port"])
            self.ui.lineEditUser.setText(item_data["ItemData"]["User"])
            self.ui.lineEditDomain.setText(item_data["ItemData"]["Domain"])
            self.ui.pushButtonSave.clicked.connect(self.edit_item)
        elif item_data["Mode"] == "AddItem":
            # self.ui.lineEditName.setText(item_data["Parent"])
            self.ui.pushButtonSave.clicked.connect(self.create_new_item)
        else:
            pass

    def create_new_item(self):

        self.ds.create_new_profile(**{
            'parent': self.parent,
            'database': self.storage_name,
            'Name': unicode(self.ui.lineEditName.text()),
            'Server': unicode(self.ui.lineEditServer.text()),
            'Domain': unicode(self.ui.lineEditDomain.text()),
            'User': unicode(self.ui.lineEditUser.text()),
            'Password': unicode(self.ui.lineEditPassword.text()),
            'Port': str(self.ui.lineEditPort.text())})

        self.updated = True
        self.close()

    def edit_item(self):

        password = self.ui.lineEditPassword.text()

        if password != u'':
            password = unicode(password)
        else:
            password = ''

        self.ds.update_profile(**{
            'item_to_edit': self.item_to_edit,
            'database': self.storage_name,
            'Name': unicode(self.ui.lineEditName.text()),
            'Server': unicode(self.ui.lineEditServer.text()),
            'Domain': unicode(self.ui.lineEditDomain.text()),
            'User': unicode(self.ui.lineEditUser.text()),
            'Password': password,
            'Port': str(self.ui.lineEditPort.text())})

        self.close()




