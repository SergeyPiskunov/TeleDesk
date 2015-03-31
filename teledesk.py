# encoding: utf-8

from PyQt4 import QtGui
import main_window
import item_edit_dialog
import new_folder_dialog
from db_connector import DBConnector
from data_storage import DataStorage


class MyWindow(QtGui.QWidget):
    """ UI class"""
    #dbc = DBConnector("config.db")

    def __init__(self, parent=None):

        #list of data sources
        so = {"Name": "Local_storage", "Type": "local", "Path": "config.db"}
        #so2 = {"Name": "Common_storage", "Type": "common", "Path": "config.db"}
        sources = [so]
        self.ds = DataStorage(sources)

        # GUI
        QtGui.QWidget.__init__(self, parent)
        self.ui = main_window.Ui_MainWindow()
        self.ui.setupUi(self)
        model = QtGui.QStandardItemModel()
        model.setHorizontalHeaderLabels(['Name'])
        self.ui.treeView.setModel(model)
        root = QtGui.QStandardItem("Local_storage")
        self.fill_tree("1", root)
        model.appendRow(root)
        self.ui.treeView.expand(model.indexFromItem(root))
        #model = QtGui.QStandardItemModel()
        #self.ui.treeView.setModel(model)
        self.ui.treeView.doubleClicked.connect(self.init_connection)
        self.ui.treeView.clicked.connect(self.display_item_info)
        self.ui.pushButtonAdd.clicked.connect(self.add_new_item)
        self.ui.pushButtonAddFolder.clicked.connect(self.add_new_folder)
        self.ui.pushButtonRemove.clicked.connect(self.remove_item)


    def fill_tree(self, parent, root):
        cildlist = self.ds.get_folders_children("Local_storage", parent)

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

            self.fill_tree(str(chld["ID"]), child_node)

    def display_item_info(self, index):
        selected_name = str(index.model().itemFromIndex(index).text())
        item = self.ds.get_profile_info("Local_storage", selected_name)

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
        item = self.ds.get_profile_info("Local_storage", selected_name)
        if item.__len__():
            item_data = {"Parent": None, "ItemData": item[0], "Mode": "Edit"}
            input_dialog = ItemEditDialog(item_data)
            input_dialog.exec_()

    def add_new_item(self):
        index = self.ui.treeView.selectedIndexes()[0]
        selected_name = str(index.model().itemFromIndex(index).text())
        item = self.ds.get_folder_id("Local_storage", selected_name)
        if item.__len__():
            item_data = {"Parent": str(item[0]["ID"]), "ItemData": None, "Mode": "AddItem"}
            inputter = ItemEditDialog(self.ds, item_data)
            inputter.exec_()
            if inputter.updated:
                model = QtGui.QStandardItemModel()
                model.setHorizontalHeaderLabels(['Name'])
                self.ui.treeView.setModel(model)
                root = QtGui.QStandardItem("Local_storage")

                self.fill_tree("1", root)
                model.appendRow(root)
                self.ui.treeView.expand(model.indexFromItem(root))

    def add_new_folder(self):
        index = self.ui.treeView.selectedIndexes()[0]
        selected_name = str(index.model().itemFromIndex(index).text())
        item = self.ds.get_folder_id("Local_storage", selected_name)
        if item.__len__():
            item_data = {"Parent": str(item[0]["ID"]), "ItemData": None, "Mode": "AddFolder"}
            inputter = NewFolderDialog(self.ds, item_data)
            inputter.exec_()
            if inputter.updated:
                model = QtGui.QStandardItemModel()
                model.setHorizontalHeaderLabels(['Name'])
                self.ui.treeView.setModel(model)
                root = QtGui.QStandardItem("Local_storage")
                self.fill_tree("1", root)
                model.appendRow(root)
                self.ui.treeView.expand(model.indexFromItem(root))

    def remove_item(self):
        index = self.ui.treeView.selectedIndexes()[0]
        selected_name = str(index.model().itemFromIndex(index).text())
        if selected_name != "Local_storage":
            self.ds.delete_folder("Local_storage", selected_name)
            model = QtGui.QStandardItemModel()
            model.setHorizontalHeaderLabels(['Name'])
            self.ui.treeView.setModel(model)
            root = QtGui.QStandardItem("Local_storage")
            self.fill_tree("1", root)
            model.appendRow(root)
            self.ui.treeView.expand(model.indexFromItem(root))


class ItemEditDialog(QtGui.QDialog):

    def __init__(self, ds, item_data=None):
        self.ds = ds
        self.updated = False
        self.parent = item_data["Parent"]
        QtGui.QWidget.__init__(self, None)
        self.ui = item_edit_dialog.Ui_EditWin()
        self.ui.setupUi(self)
        if item_data["Mode"] == "Edit":
            self.ui.lineEditName.setText(item_data["ItemData"]["ALIAS"])
            self.ui.lineEditServer.setText(item_data["ItemData"]["SERVER"])
            self.ui.lineEditPort.setText(item_data["ItemData"]["PORT"])
            self.ui.lineEditUser.setText(item_data["ItemData"]["USER"])
            #self.ui.lineEditName.setText(item_data["PASSWORD"])
        elif item_data["Mode"] == "AddItem":
            #self.ui.lineEditName.setText(item_data["Parent"])
            self.ui.pushButtonSave.clicked.connect(self.create_new_item)
        else:
            pass

    def create_new_item(self):
        name = str(self.ui.lineEditName.text())
        server = str(self.ui.lineEditServer.text())
        user = str(self.ui.lineEditUser.text())
        port = str(self.ui.lineEditPort.text())
        self.ds.create_new_profile("Local_storage", name, server, port, user)

        item = self.ds.get_profile_id("Local_storage", name)
        if item.__len__():
            id = str(item[0]["ID"])
            self.ds.create_new_profile_folder("Local_storage", self.parent, name, id)
            self.updated = True
            self.close()


class NewFolderDialog(QtGui.QDialog):

    def __init__(self, ds, item_data=None):
        self.updated = False
        self.ds = ds
        self.parent = item_data["Parent"]
        QtGui.QWidget.__init__(self, None)
        self.ui = new_folder_dialog.Ui_NewFolderWin()
        self.ui.setupUi(self)
        self.ui.pushButtonOk.clicked.connect(self.ok)
        self.ui.pushButtonCancel.clicked.connect(self.cancel)
        self.ui.labelParentName.setText("/"+str(self.parent))

    def ok(self):
        name = str(self.ui.lineEditFolderName.text())
        self.ds.create_new_folder("Local_storage", self.parent, name)
        self.updated = True
        self.close()

    def cancel(self):
        self.close()



if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    window = MyWindow()
    window.move(app.desktop().screen().rect().center() - window.rect().center())
    window.show()
    sys.exit(app.exec_())
    #INSERT INTO `FOLDERS`(`ID`,`Parent`,`Name`,`Profile`) VALUES (14, 1, "new", 1);

