# encoding: utf-8
import os
import time
import win32crypt
import binascii
from PyQt4 import QtGui, QtCore

from libs.db import datastorage

from libs.forms import mainwindow
from libs.forms import settings
from libs.forms import newfolder
from libs.forms import itemedit

from libs.core import serializer
from libs.core import usersettings


class MyWindow(QtGui.QWidget):
    # datastorage root element id
    ROOT_ELEMENT_ID = "1"
    APP_ICON = "res/computer.png"
    FOLDER_ICON = "res/folder.png"
    SERVER_ICON = "res/computer.png"

    """ UI class"""

    def __init__(self, parent=None):

        super(MyWindow, self).__init__()
        # loading user settings
        self.user_settings = usersettings.UserSettings()
        self.user_settings.load_config()
        self.ds = datastorage.DataStorage(self.user_settings.databases)

        # GUI
        QtGui.QWidget.__init__(self, parent)
        self.ui = mainwindow.MainWindowUi()
        self.ui.setupUi(self)

        # tree view
        model = QtGui.QStandardItemModel()
        model.setHorizontalHeaderLabels(['Name'])
        self.ui.treeView.setModel(model)
        self.ui.treeView.setColumnHidden(1, True)
        self.ui.treeView.header().close()

        for stor in self.user_settings.databases:
            root = QtGui.QStandardItem(stor["Name"])
            self.fill_tree(stor["Name"], self.ROOT_ELEMENT_ID, root)
            model.appendRow(root)
            self.ui.treeView.expand(model.indexFromItem(root))

        self.ui.treeView.doubleClicked.connect(self.init_connection_fromwindow)
        self.ui.treeView.clicked.connect(self.display_item_info)
        self.ui.deleteGroupAction.triggered.connect(self.remove_item)
        self.ui.editServerAction.triggered.connect(self.edit_item)
        self.ui.addGroupAction.triggered.connect(self.add_new_folder)
        self.ui.addServerAction.triggered.connect(self.add_new_item)
        self.ui.removeServerAction.triggered.connect(self.remove_item)
        self.ui.settingsAction.triggered.connect(self.show_user_settings)

        # Minimizing to tray
        style = self.style()
        # Set the window and tray icon to something
        # icon = style.standardIcon(QtGui.QStyle.SP_ComputerIcon)
        icon = MyWindow.APP_ICON
        self.tray_icon = QtGui.QSystemTrayIcon()
        self.tray_icon.setIcon(QtGui.QIcon(icon))
        self.setWindowIcon(QtGui.QIcon(icon))

        # Restore the window when the tray icon is double clicked.
        self.tray_icon.activated.connect(self.restore_window_from_tray)

    def event(self, event):
        if (event.type() == QtCore.QEvent.WindowStateChange and
                self.isMinimized()):
            self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.Tool)
            self.tray_icon.show()
            return True
        else:
            return super(MyWindow, self).event(event)

    def closeEvent(self, event):
        reply = QtGui.QMessageBox.question(self, 'Message', "Are you sure to quit?",
                                           QtGui.QMessageBox.Yes | QtGui.QMessageBox.No,
                                           QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            self.tray_icon.show()
            self.hide()
            event.ignore()

    def keyPressEvent(self, event):

        # DEL key
        if event.key() == 16777223:
            self.remove_item()

        # INS key
        elif event.key() == 16777222:
            self.add_new_item()

    def restore_window_from_menu(self):
        self.tray_icon.hide()
        self.showNormal()
        self.move(QtCore.QPoint(app.desktop().screen().availableGeometry().width() - window.rect().width() - 15,
                                app.desktop().screen().availableGeometry().height() - window.rect().height() - 35))

    def restore_window_from_tray(self, reason):
        if reason == QtGui.QSystemTrayIcon.DoubleClick:
            self.tray_icon.hide()
            self.showNormal()
            self.move(QtCore.QPoint(app.desktop().screen().availableGeometry().width() - window.rect().width() - 15,
                                    app.desktop().screen().availableGeometry().height() - window.rect().height() - 35))

        if reason == QtGui.QSystemTrayIcon.Trigger:
            tray_menu = QtGui.QMenu(None)

            self.tray_icon.setContextMenu(tray_menu)
            self.tray_icon.setToolTip("TeleDesk")

            # self.ui.exitAction.triggered.connect(QtGui.qApp.quit)
            # self.ui.exitAction = QtGui.QAction('&Exit', MyWindow)

            # Title
            self.ui.restore_win = QtGui.QAction("&TeleDesk", self)
            tray_menu.addAction(self.ui.restore_win)
            self.ui.restore_win.triggered.connect(self.restore_window_from_menu)

            tray_menu.addSeparator()

            folder_icon = QtGui.QIcon(MyWindow.FOLDER_ICON)
            computer_icon = QtGui.QIcon(MyWindow.SERVER_ICON)

            for stor in self.user_settings.databases:
                top_list = self.user_settings.get_top_ten_connections(stor["Name"], 32)
                node_entry = tray_menu.addAction(stor["Name"])
                node_entry.setIcon(folder_icon)
                if top_list.__len__():
                    for menu_item in top_list:
                        item = self.ds.get_profile_info(stor["Name"], menu_item[0])
                        if item:
                            entry = tray_menu.addAction(item["NAME"])
                            entry.setIcon(computer_icon)
                            self.connect(entry, QtCore.SIGNAL('triggered()'),
                                         lambda menu_it=(stor["Name"], menu_item): self.init_connection_frommenu(
                                             menu_it))

                            # self.connect(button, SIGNAL("clicked()"), lambda who="Three": self.anyButton(who))

            tray_menu.addSeparator()

            # Exit
            self.ui.extact = QtGui.QAction("&Exit", self)
            tray_menu.addAction(self.ui.extact)
            self.ui.extact.triggered.connect(QtGui.qApp.quit)

            self.tray_icon.contextMenu().popup(QtGui.QCursor.pos())

    def fill_tree(self, storage, parent, root):
        cildlist = self.ds.get_folders_children(storage, parent)

        for chld in cildlist:
            child_node = QtGui.QStandardItem(unicode(chld["NAME"]))
            child_node.setData(QtCore.QVariant(unicode(chld["ID"])))

            # icon = QtGui.QIcon()
            if str(chld["PROFILE"]) == u'':
                icon = QtGui.QIcon(MyWindow.FOLDER_ICON)
            elif str(chld["PROFILE"]):
                icon = QtGui.QIcon(MyWindow.SERVER_ICON)
            else:
                pass

            child_node.setIcon(icon)
            root.appendRow(child_node)
            self.ui.treeView.expand(self.ui.treeView.model().indexFromItem(child_node))

            self.fill_tree(storage, unicode(chld["ID"]), child_node)

    def update_tree(self):

        model = QtGui.QStandardItemModel()
        model.setHorizontalHeaderLabels(['Name'])
        self.ui.treeView.setModel(model)
        for stor in self.user_settings.databases:
            root = QtGui.QStandardItem(stor["Name"])
            self.fill_tree(stor["Name"], self.ROOT_ELEMENT_ID, root)
            model.appendRow(root)
            self.ui.treeView.expand(model.indexFromItem(root))

    def display_item_info(self, index):

        selected_id = str(index.model().itemFromIndex(index).data().toString())
        storage_name = self.get_storage_name(index)

        if selected_id:
            item = self.ds.get_profile_info(storage_name, selected_id)

            if item.__len__():
                name = unicode(item["NAME"])
                server = unicode(item["SERVER"])
                port = str(item["PORT"])
                user = unicode(item["USER"])
                self.ui.labelStatus.setText(" Name - " + name + "\n"
                                            + " Server - " + server + "\n"
                                            + " Port - " + port + "\n"
                                            + " User - " + user + "\n\n")
            else:
                self.ui.labelStatus.setText("")

    def init_connection_fromwindow(self, index):
        selected_id = str(index.model().itemFromIndex(index).data().toString())
        storage_name = self.get_storage_name(index)
        self.init_connection(storage_name, selected_id)

    def init_connection_frommenu(self, selected_item):
        storage_name = selected_item[0]
        selected_id = selected_item[1]
        self.init_connection(storage_name, selected_id)

    def init_connection(self, storage_name, selected_id):
        self.user_settings.update_item_rating(storage_name, selected_id)
        item = self.ds.get_profile_info(storage_name, selected_id)
        if item.__len__():
            te = serializer.Serializer().serialize_to_file_win_rdp(item, "7.1", item["NAME"] + ".rdp")
            if te:
                os.startfile(item["NAME"] + ".rdp")
                time.sleep(3)
                os.remove(item["NAME"] + ".rdp")

    def edit_item(self):
        index = self.ui.treeView.selectedIndexes()[0]
        selected_id = str(index.model().itemFromIndex(index).data().toString())
        storage_name = self.get_storage_name(index)

        item = self.ds.get_profile_info(storage_name, selected_id)
        if item.__len__():
            input_dialog = ItemEditDialog(self.ds,
                                          {"Storage": storage_name,
                                           "Parent": None,
                                           "ItemData": item,
                                           "Mode": "Edit"})
            input_dialog.ui.pushButtonClose.clicked.connect(lambda: input_dialog.close())
            input_dialog.exec_()
            self.update_tree()

            item = self.ds.get_profile_info(storage_name, selected_id)

            if item.__len__():
                name = unicode(item["NAME"])
                server = unicode(item["SERVER"])
                port = str(item["PORT"])
                user = unicode(item["USER"])
                self.ui.labelStatus.setText(" Name - " + name + "\n"
                                            + " Server - " + server + "\n"
                                            + " Port - " + port + "\n"
                                            + " User - " + user + "\n\n")
            else:
                self.ui.labelStatus.setText("")

    def add_new_item(self):
        index = self.ui.treeView.selectedIndexes()[0]
        selected_name = unicode(index.model().itemFromIndex(index).text())
        storage_name = str(index.model().itemFromIndex(index).parent().text())
        item = self.ds.get_folder_id(storage_name, selected_name)

        if item.__len__():
            item_data = {"Storage": storage_name, "Parent": str(item["ID"]), "ItemData": None, "Mode": "AddItem"}
            input_dialog = ItemEditDialog(self.ds, item_data)
            input_dialog.exec_()
            if input_dialog.updated:
                self.update_tree()

    def add_new_folder(self):
        index = self.ui.treeView.selectedIndexes()[0]
        selected_name = str(index.model().itemFromIndex(index).text())
        storage_name = str(index.model().itemFromIndex(index).text())

        item = self.ds.get_folder_id(storage_name, selected_name)
        if item.__len__():
            item_data = {"Storage": storage_name, "Parent": str(item["ID"]), "ItemData": None, "Mode": "AddFolder"}
            inputter = NewFolderDialog(self.ds, item_data)
            inputter.exec_()
            if inputter.updated:
                self.update_tree()

    def remove_item(self):
        index = self.ui.treeView.selectedIndexes()[0]
        selected_id = str(index.model().itemFromIndex(index).data().toString())
        storage_name = self.get_storage_name(index)
        if selected_id != self.ROOT_ELEMENT_ID:
            # if there are child elements, asking user before deleting
            child_elements = self.ds.get_child_elements(storage_name, selected_id)
            if child_elements.__len__():
                reply = QtGui.QMessageBox.question(self, 'Message', "Delete element with all child elements?",
                                                   QtGui.QMessageBox.Yes | QtGui.QMessageBox.No,
                                                   QtGui.QMessageBox.No)
                if reply == QtGui.QMessageBox.Yes:
                    self.ds.delete_folder(storage_name, selected_id)
            else:
                reply = QtGui.QMessageBox.question(self, 'Message', "Delete element?",
                                                   QtGui.QMessageBox.Yes | QtGui.QMessageBox.No,
                                                   QtGui.QMessageBox.No)
                if reply == QtGui.QMessageBox.Yes:
                    self.ds.delete_folder(storage_name, selected_id)

            self.update_tree()

    def show_user_settings(self):
        settings_dialog = UserSettingsDialog(self.user_settings)
        # settings_dialog.ui.pushButtonClose.clicked.connect(lambda: input_dialog.close())
        settings_dialog.exec_()

    @staticmethod
    def get_storage_name(index):

        item = index.model().itemFromIndex(index)
        storage_name = unicode(item.text())
        while item:
            if not item.parent():
                storage_name = unicode(item.text())
            item = item.parent()
        return storage_name


class ItemEditDialog(QtGui.QDialog):
    def __init__(self, ds, item_data=None):
        self.ds = ds
        self.storage_name = item_data["Storage"]
        self.updated = False
        self.parent = item_data["Parent"]
        QtGui.QWidget.__init__(self, None)
        self.ui = itemedit.ItemEditWindowUi()
        self.ui.setupUi(self)
        if item_data["Mode"] == "Edit":
            self.item_to_edit = item_data["ItemData"]["ID"]
            self.ui.lineEditName.setText(item_data["ItemData"]["NAME"])
            self.ui.lineEditServer.setText(item_data["ItemData"]["SERVER"])
            self.ui.lineEditPort.setText(item_data["ItemData"]["PORT"])
            self.ui.lineEditUser.setText(item_data["ItemData"]["USER"])
            self.ui.lineEditDomain.setText(item_data["ItemData"]["DOMAIN"])
            self.ui.pushButtonSave.clicked.connect(self.edit_item)
        elif item_data["Mode"] == "AddItem":
            # self.ui.lineEditName.setText(item_data["Parent"])
            self.ui.pushButtonSave.clicked.connect(self.create_new_item)
        else:
            pass

    def create_new_item(self):
        pwdHash = win32crypt.CryptProtectData(str(self.ui.lineEditPassword.text()), u'psw', None, None, None, 0)
        password = binascii.hexlify(pwdHash)

        self.ds.create_new_profile(**{
            'parent': self.parent,
            'storage_name': self.storage_name,
            'name': unicode(self.ui.lineEditName.text()),
            'server': unicode(self.ui.lineEditServer.text()),
            'domain': unicode(self.ui.lineEditDomain.text()),
            'user': unicode(self.ui.lineEditUser.text()),
            'password': password,
            'port': str(self.ui.lineEditPort.text())})

        self.updated = True
        self.close()

    def edit_item(self):

        password = self.ui.lineEditPassword.text()

        if password != u'':
            pwdHash = win32crypt.CryptProtectData(unicode(password), u'psw', None, None, None, 0)
            password = binascii.hexlify(pwdHash)
        else:
            password = ''

        self.ds.update_profile(**{
            'item_to_edit': self.item_to_edit,
            'storage_name': self.storage_name,
            'name': unicode(self.ui.lineEditName.text()),
            'server': unicode(self.ui.lineEditServer.text()),
            'domain': unicode(self.ui.lineEditDomain.text()),
            'user': unicode(self.ui.lineEditUser.text()),
            'password': password,
            'port': str(self.ui.lineEditPort.text())})

        self.close()


class NewFolderDialog(QtGui.QDialog):
    def __init__(self, ds, item_data=None):
        self.updated = False
        self.ds = ds
        self.storage = item_data["Storage"]
        self.parent = item_data["Parent"]
        QtGui.QWidget.__init__(self, None)
        self.ui = newfolder.NewFolderWindowUi()
        self.ui.setupUi(self)
        self.ui.pushButtonOk.clicked.connect(self.ok)
        self.ui.pushButtonCancel.clicked.connect(self.cancel)
        self.ui.labelParentName.setText("Enter folder name")

    def ok(self):
        name = unicode(self.ui.lineEditFolderName.text())
        self.ds.create_new_folder(self.storage, self.parent, name)
        self.updated = True
        self.close()

    def cancel(self):
        self.close()


class UserSettingsDialog(QtGui.QDialog):
    def __init__(self, usersett):
        QtGui.QWidget.__init__(self, None)
        self.ui = settings.SettingsWindowUi()
        self.ui.setupUi(self)
        self.usersett = usersett

        # dividing list of databases into local and FTP databases
        # to display them in separate tables
        localdatabases = [dict(Name=x["Name"],
                               Path=x["Path"],
                               User=x["User"],
                               Password=x["Password"]) for x in self.usersett.databases
                          if x["Type"] == "local"]

        localdatabases_columns = {"Name": "",
                                  "Path": "",
                                  "User": "",
                                  "Password": ""}
        self.ui.localStorageTableView.setModel(settings.SettingsTableModel(localdatabases, localdatabases_columns))

        self.ftpdatabases = [dict(Name=x["Name"],
                                  Path=x["Path"],
                                  User=x["User"],
                                  Password=x["Password"],
                                  Server=x["Properties"]["Server"],
                                  Port=x["Properties"]["Port"],
                                  FTPUser=x["Properties"]["FTPUser"],
                                  FTPPassword=x["Properties"]["FTPPassword"]) for x in self.usersett.databases
                             if x["Type"] == "ftp"]

        ftpdatabases_columns = {"Name": "",
                                "Server": "",
                                "Port": "",
                                "FTPUser": "",
                                "FTPPassword": "",
                                "Path": "",
                                "User": "",
                                "Password": ""}

        self.ui.FTPStorageTableView.setModel(settings.SettingsTableModel(self.ftpdatabases, ftpdatabases_columns))

        self.ui.OKButton.clicked.connect(self.save)
        self.ui.CancelButton.clicked.connect(self.cancel)
        self.ui.deleteLocalStorageButton.clicked.connect(self.removeLocalStorageRow)
        self.ui.addLocalStorageButton.clicked.connect(self.addLocalStorageRow)
        self.ui.deleteFTPStorageButton.clicked.connect(self.removeFTPStorageRow)
        self.ui.addFTPStorageButton.clicked.connect(self.addFTPStorageRow)

    def save(self):
        self.usersett.databases = self.ui.localStorageTableView.model().databases
        self.usersett.databases = []
        localdatabases = [dict(Name=x["Name"],
                               Type="local",
                               Properties={},
                               Path=x["Path"],
                               User=x["User"],
                               Password=x["Password"])
                          for x in self.ui.localStorageTableView.model().databases]

        ftpdatabases = [dict(Name=x["Name"],
                             Type="ftp",
                             Properties=dict(Server=x["Server"],
                                             Port=x["Port"],
                                             FTPUser=x["FTPUser"],
                                             FTPPassword=x["FTPPassword"]),
                             Path=x["Path"],
                             User=x["User"],
                             Password=x["Password"])
                        for x in self.ui.FTPStorageTableView.model().databases]

        self.usersett.databases = localdatabases + ftpdatabases

        self.usersett.save_config()
        self.close()

    def cancel(self):
        self.close()

    def addLocalStorageRow(self):
        selected_index = self.ui.localStorageTableView.model().index(len(self.usersett.databases), 0)

        self.ui.localStorageTableView.model().insertRow(len(self.usersett.databases), selected_index)

    def removeLocalStorageRow(self):
        selected_index = self.ui.localStorageTableView.selectionModel().selectedIndexes()[0]

        self.ui.localStorageTableView.model().removeRow(selected_index.row(), selected_index.parent())

    def addFTPStorageRow(self):
        selected_index = self.ui.FTPStorageTableView.model().index(len(self.usersett.databases), 0)

        self.ui.FTPStorageTableView.model().insertRow(len(self.usersett.databases), selected_index)

    def removeFTPStorageRow(self):
        selected_index = self.ui.FTPStorageTableView.selectionModel().selectedIndexes()[0]

        self.ui.FTPStorageTableView.model().removeRow(selected_index.row(), selected_index.parent())


if __name__ == "__main__":
    import sys

    app = QtGui.QApplication(sys.argv)

    # app.setStyle("Windows")
    # app.setStyle("WindowsXP")
    # app.setStyle("WindowsVista")
    # app.setStyle("Motif")
    # app.setStyle("CDE")
    app.setStyle("Plastique")
    # app.setStyle("Cleanlooks")

    window = MyWindow()
    window.move(QtCore.QPoint(app.desktop().screen().availableGeometry().width() - window.rect().width() - 15,
                              app.desktop().screen().availableGeometry().height() - window.rect().height() - 35))
    # window.setSizePolicy(0, 0)
    window.show()
    sys.exit(app.exec_())
