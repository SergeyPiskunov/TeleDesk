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


class MainWindowUi(object):
    def setupUi(self, MyWin):
        MyWin.setObjectName(_fromUtf8("MyWin"))
        MyWin.resize(243, 600)
        MyWin.setContentsMargins(-10, -10, -10, -25)

        MyWin.setMinimumSize(243, 600)
        MyWin.setMaximumSize(243, 600)

        self.verticalLayout = QtGui.QVBoxLayout(MyWin)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))

        #Menu


        self.mainMenu = QtGui.QMenuBar()
        self.gridLayout.addWidget(self.mainMenu, 1, 0, 1, 4)

        #settings
        self.settingsAction = QtGui.QAction("&Settings", MyWin)
        importRdpAction = QtGui.QAction('&Import from *.rdp file', MyWin)

        #re-read databases
        self.refresh_DBAction = QtGui.QAction('&Refresh DB`s', MyWin)

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
        fileMenu = self.mainMenu.addMenu('&Menu')
        fileMenu.addAction(self.settingsAction)
        fileMenu.addAction(self.refresh_DBAction)
        fileMenu.addAction(importRdpAction)
        fileMenu.addAction(self.exitAction)

        #tree view
        self.treeView = QtGui.QTreeView(MyWin)
        self.treeView.setContextMenuPolicy(3)
        self.treeView.setObjectName(_fromUtf8("treeView"))
        self.treeView.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.treeView.customContextMenuRequested.connect(self.openMenu)
        self.gridLayout.addWidget(self.treeView, 2, 0, 1, 4)

        #status label
        self.labelStatus = QtGui.QLabel(MyWin)
        self.labelStatus.setObjectName(_fromUtf8("labelStatus"))
        self.gridLayout.addWidget(self.labelStatus, 4, 0, 4, 3)
        self.verticalLayout.addLayout(self.gridLayout)

        self.retranslateUi(MyWin)
        QtCore.QMetaObject.connectSlotsByName(MyWin)

    def retranslateUi(self, MyWin):
        MyWin.setWindowTitle(_translate("MyWin", "TeleDesk v1.0a", None))

    def openMenu(self, position):

        indexes = self.treeView.selectedIndexes()
        level = -1
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

        elif level == -1:
            menu.addAction(self.refresh_DBAction)


        menu.exec_(self.treeView.viewport().mapToGlobal(position))
