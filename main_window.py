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
        MyWin.resize(243, 579)
        MyWin.setContentsMargins(-10, -10, -10, -25)
        #MyWin.setSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)

        self.verticalLayout = QtGui.QVBoxLayout(MyWin)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))

        #Menu


        self.mainMenu = QtGui.QMenuBar()
        self.gridLayout.addWidget(self.mainMenu, 1, 0, 1, 4)

        #settings
        self.settingsAction = QtGui.QAction('&Settings', MyWin)
        importRdpAction = QtGui.QAction('&Import from *.rdp file', MyWin)

        #exit application
        self.exitAction = QtGui.QAction('&Exit', MyWin)
        self.exitAction.setShortcut('Ctrl+Q')
        self.exitAction.setStatusTip('Exit application')
        self.exitAction.triggered.connect(QtGui.qApp.quit)

        #add server
        self.addServerAction = QtGui.QAction('&Add server', MyWin)
        self.addServerAction.setStatusTip('Add server')

        #remove server
        self.removeServerAction = QtGui.QAction('&Remove server', MyWin)
        self.removeServerAction.setStatusTip('Remove server')

        #export to RDP
        self.exportToRDPAction = QtGui.QAction('&Export to *.rdp file', MyWin)
        self.exportToRDPAction.setStatusTip('Export to *.rdp file')
        self.exportToRDPAction.triggered.connect(QtGui.qApp.quit)

        #edit server
        self.editServerAction = QtGui.QAction('&Edit server', MyWin)
        self.editServerAction.setStatusTip('Edit server')

        #add group
        self.addGroupAction = QtGui.QAction('&Add group', MyWin)
        self.addGroupAction.setStatusTip('Add group')

        #delete group
        self.deleteGroupAction = QtGui.QAction('&Delete group', MyWin)
        self.deleteGroupAction.setStatusTip('Delete group')

        #main menu
        fileMenu = self.mainMenu.addMenu('&Main')
        fileMenu.addAction(self.settingsAction)
        fileMenu.addAction(importRdpAction)
        fileMenu.addAction(self.exitAction)


        self.treeView = QtGui.QTreeView(MyWin)
        self.treeView.setContextMenuPolicy(3)
        self.treeView.setObjectName(_fromUtf8("treeView"))
        self.treeView.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.gridLayout.addWidget(self.treeView, 2, 0, 1, 4)

        #self.horSpacer = QtGui.QSpacerItem(10, 10, vPolicy=QtGui.QSizePolicy.Expanding)
        #self.horSpacer.
        #self.gridLayout.addWidget(self.horSpacer, 2, 0, 1, 3)

        self.treeView.customContextMenuRequested.connect(self.openMenu)

        self.textEditDescription = QtGui.QTextEdit(MyWin)
        self.textEditDescription.setObjectName(_fromUtf8("textEditDescription"))
        self.gridLayout.addWidget(self.textEditDescription, 3, 0, 3, 4)

        self.labelStatus = QtGui.QLabel(MyWin)
        self.labelStatus.setText(_fromUtf8(""))
        self.labelStatus.setObjectName(_fromUtf8("labelStatus"))
        #self.gridLayout.addWidget(self.labelStatus, 3, 0, 1, 4)
        self.verticalLayout.addLayout(self.gridLayout)

        self.retranslateUi(MyWin)
        QtCore.QMetaObject.connectSlotsByName(MyWin)

    def retranslateUi(self, MyWin):
        MyWin.setWindowTitle(_translate("MyWin", "TeleDesk v0.1", None))

    def openMenu(self, position):

        indexes = self.treeView.selectedIndexes()
        if len(indexes) > 0:

            level = 0
            index = indexes[0]
            while index.parent().isValid():
                index = index.parent()
                level += 1

        menu = QtGui.QMenu()
        if level == 0:
            menu.addAction(self.addGroupAction)
        elif level == 1:
            menu.addAction(self.addServerAction)
            menu.addAction(self.deleteGroupAction)

        elif level == 2:
            menu.addAction(self.editServerAction)
            menu.addAction(self.removeServerAction)
            menu.addAction(self.exportToRDPAction)

        menu.exec_(self.treeView.viewport().mapToGlobal(position))
