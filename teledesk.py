# encoding: utf-8
from PyQt4 import QtCore, QtGui
import main_window, item_edit_dialog
from db_connector import DBConnector


class MyWindow(QtGui.QWidget):
    """ UI class"""
    dbc = DBConnector("config.db")

    def __init__(self, parent=None):
        # GUI
        QtGui.QWidget.__init__(self, parent)
        self.ui = main_window.Ui_MainWindow()
        self.ui.setupUi(self)

        model = QtGui.QStandardItemModel()
        model.setHorizontalHeaderLabels(['Name'])

        self.ui.treeView.setModel(model)


        root = QtGui.QStandardItem("Local_storage")
        self.fill_tree(MyWindow.dbc, "1", root)
        model.appendRow(root)
        self.ui.treeView.expand(model.indexFromItem(root))


        #model = QtGui.QStandardItemModel()
        #self.ui.treeView.setModel(model)

        self.ui.treeView.doubleClicked.connect(self.init_connection)
        self.ui.treeView.clicked.connect(self.display_item_info)

    def fill_tree(self, dbc, parent, root):
        cildlist = dbc.get_data("SELECT * FROM FOLDERS WHERE PARENT = ?", parent)
        for chld in cildlist:
            child_node = QtGui.QStandardItem(str(chld["NAME"]))

            icon = QtGui.QIcon()
            if str(chld["PROFILE"]) == u'':
                icon = QtGui.QIcon("res/folder.png")
            elif str(chld["PROFILE"]):
                icon = QtGui.QIcon("res/computer.png")
            else:
                pass

            child_node.setIcon(icon)
            root.appendRow(child_node)

            self.ui.treeView.expand(self.ui.treeView.model().indexFromItem(child_node))

            self.fill_tree(dbc, str(chld["ID"]), child_node)

    def display_item_info(self, index):
        selected_name = str(index.model().itemFromIndex(index).text())
        item = MyWindow.dbc.get_data("SELECT * FROM PROFILES LEFT JOIN FOLDERS ON FOLDERS.Profile = PROFILES.ID WHERE FOLDERS.NAME = ?", selected_name)
        if item.__len__():
            alias = str(item[0]["ALIAS"])
            server = str(item[0]["SERVER"])
            port = str(item[0]["PORT"])
            user = str(item[0]["USER"])
            self.ui.textEditDescription.setText("Name - " + alias + "\n"
                                                + "Server - " + server + "\n"
                                                + "Port - " + port + "\n"
                                                + "User - " + user + "\n")
        else:
            self.ui.textEditDescription.setText("")

    def init_connection(self, index):
        selected_name = str(index.model().itemFromIndex(index).text())
        item = MyWindow.dbc.get_data("SELECT * FROM PROFILES LEFT JOIN FOLDERS ON FOLDERS.Profile = PROFILES.ID WHERE FOLDERS.NAME = ?", selected_name)
        if item.__len__():
            self.ui.labelStatus.setText(str(item[0]["PARENT"]))
        #INSERT INTO `FOLDERS`(`ID`,`Parent`,`Name`,`Profile`) VALUES (14, 1, "new", 1);

        item = MyWindow.dbc.get_data("SELECT * FROM PROFILES LEFT JOIN FOLDERS ON FOLDERS.Profile = PROFILES.ID WHERE FOLDERS.NAME = ?", selected_name)
        if item.__len__():
            inputter = ItemEditDialog(None, item[0])
            inputter.exec_()
            #comment = inputter.text.text()
            #print comment


class ItemEditDialog(QtGui.QDialog):

    def __init__(self, parent=None, item_data = None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = item_edit_dialog.Ui_EditWin()
        self.ui.setupUi(self)
        self.ui.lineEditName.setText(item_data["ALIAS"])
        self.ui.lineEditServer.setText(item_data["SERVER"])
        self.ui.lineEditPort.setText(item_data["PORT"])
        self.ui.lineEditUser.setText(item_data["USER"])
        #self.ui.lineEditName.setText(item_data["PASSWORD"])



if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    window = MyWindow()
    window.move(app.desktop().screen().rect().center() - window.rect().center())
    window.show()
    sys.exit(app.exec_())
