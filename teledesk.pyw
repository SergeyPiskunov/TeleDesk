# encoding: utf-8
import os
import time
import sys
import win32crypt
import binascii
from PyQt4 import QtGui, QtCore

from libs.db import datastorage

from libs.forms import mainwindow
from libs.forms import settings
from libs.forms import newfolder
from libs.forms import itemedit

from libs.core import serializer
from libs.core import user_settings
from libs.core import db_updater


class MyWindow(QtGui.QWidget):
    # datastorage root element identifier
    ROOT_ELEMENT_ID = "1"

    def __init__(self, parent=None):
        # GUI
        super(MyWindow, self).__init__()
        QtGui.QWidget.__init__(self, parent)
        self.ui = mainwindow.MainWindowUi()
        self.ui.setupUi(self)
        self.tray_menu = QtGui.QMenu(None)

        # loading user settings
        self.user_settings = user_settings.UserSettings()
        self.user_settings.load_config()
        self.ui.settingsAction.triggered.connect(self.show_user_settings)

        # loading database wrappers
        self.databases = datastorage.DataStorage(self.user_settings.databases)

        # checking passwords for encrypted databases
        for database in self.user_settings.databases:
            try:
                cildlist = self.databases.get_folders_children(
                    **dict(database=database['Name'], parent = '1'))
            except:
                self.show_msg('bad password for base {0}'.format(database['Name']))
                return None

        # displaying tree view
        self.show_connections_tree()

        # buttons event handlers
        self.ui.treeView.doubleClicked.connect(self.init_connection_fromwindow)
        self.ui.treeView.clicked.connect(self.display_item_info)
        self.ui.deleteGroupAction.triggered.connect(self.remove_item)
        self.ui.editServerAction.triggered.connect(self.edit_item)
        self.ui.addGroupAction.triggered.connect(self.add_new_folder)
        self.ui.addServerAction.triggered.connect(self.add_new_item)
        self.ui.removeServerAction.triggered.connect(self.remove_item)
        self.ui.update_DBAction.triggered.connect(self.update_databases)

        # Minimizing to tray and restoring if double-clicked
        self.tray_icon = QtGui.QSystemTrayIcon()
        self.tray_icon.setIcon(self.ui.computer_icon)
        self.setWindowIcon(self.ui.computer_icon)
        self.tray_icon.activated.connect(self.restore_window_from_tray)

        #updater for all nonlocal  databases
        #self.update_databases()

    def update_databases(self):

        self.dbupdater = db_updater.DBUpdater(self.user_settings.databases)
        self.connect(self.dbupdater, QtCore.SIGNAL("show_msg(PyQt_PyObject)"),
                     self.show_msg, QtCore.Qt.QueuedConnection)
        self.connect(self.dbupdater, QtCore.SIGNAL("show_connections_tree()"),
                     self.show_connections_tree, QtCore.Qt.QueuedConnection)
        self.dbupdater.update()

    def show_msg(self, msg):

        QtGui.QMessageBox.information(self, "Info", msg, QtGui.QMessageBox.Ok)

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
            event.ignore()

    def keyPressEvent(self, event):

        # DEL key
        if event.key() == 16777223:
            self.remove_item()

        # INS key
        #elif event.key() == 16777222:
        #    self.add_new_item()

    def restore_window_from_menu(self):

        self.tray_icon.hide()
        self.showNormal()
        self.move(QtCore.QPoint(app.desktop().screen().availableGeometry().width()
                                - window.rect().width() - 15,
                                app.desktop().screen().availableGeometry().height()
                                - window.rect().height() - 35))

    def restore_window_from_tray(self, reason):

        # if doubleclicked - displaying main window
        if reason == QtGui.QSystemTrayIcon.DoubleClick:
            self.tray_icon.hide()
            self.showNormal()
            self.move(QtCore.QPoint(app.desktop().screen().availableGeometry().width()
                                    - window.rect().width() - 15,
                                    app.desktop().screen().availableGeometry().height()
                                    - window.rect().height() - 35))

        # if clicked - displaying most frequently used connections
        if reason == QtGui.QSystemTrayIcon.Trigger:
            self.tray_menu.clear()
            self.tray_icon.setContextMenu(self.tray_menu)
            self.tray_icon.setToolTip("TeleDesk")

            # Title
            self.ui.restore_win = QtGui.QAction("&TeleDesk", self)
            self.tray_menu.addAction(self.ui.restore_win)
            self.ui.restore_win.triggered.connect(self.restore_window_from_menu)

            self.tray_menu.addSeparator()

            for stor in self.user_settings.databases:
                top_list = self.user_settings.get_top_connections(stor["Name"], 5)
                if top_list:
                    node_entry = self.tray_menu.addAction(stor["Name"])
                    node_entry.setIcon(self.ui.database_icon)
                    for menu_item in top_list:
                        if menu_item:
                            item = self.databases.get_profile_info(**dict(database=stor["Name"], ID=menu_item))
                            if item:
                                entry = self.tray_menu.addAction(item["Name"])
                                entry.setIcon(self.ui.computer_icon)
                                self.connect(entry, QtCore.SIGNAL('triggered()'),
                                             lambda menu_it=dict(database=stor["Name"], ID=menu_item):
                                             self.init_connection_frommenu(menu_it))

            self.tray_menu.addSeparator()

            # Exit
            self.ui.extact = QtGui.QAction("&Exit", self)
            self.tray_menu.addAction(self.ui.extact)
            self.ui.extact.triggered.connect(QtGui.qApp.quit)

            self.tray_icon.contextMenu().popup(QtGui.QCursor.pos())

    def show_connections_tree(self, onlylocal=False):

        model = QtGui.QStandardItemModel()
        model.setHorizontalHeaderLabels(['Name'])
        self.ui.treeView.setModel(model)
        self.ui.treeView.setColumnHidden(1, True)
        self.ui.treeView.header().close()
        for stor in self.user_settings.databases:
            if onlylocal and stor["Type"] != 'local':
                continue
            root = QtGui.QStandardItem(stor["Name"])
            root.setIcon(self.ui.database_icon)
            self.fill_tree(stor["Name"], self.ROOT_ELEMENT_ID, root)
            model.appendRow(root)
            self.ui.treeView.expand(model.indexFromItem(root))

    def fill_tree(self, storage, parent, root):

        cildlist = self.databases.get_folders_children(**dict(database=storage, parent = parent))
        if cildlist:
            for chld in cildlist:
                child_node = QtGui.QStandardItem(chld["Name"])
                child_node.setData(QtCore.QVariant(chld["ID"]))

                if chld["Profile"] == None:
                    icon = self.ui.group_icon
                else:
                    icon = self.ui.computer_icon

                child_node.setIcon(icon)
                root.appendRow(child_node)
                self.ui.treeView.expand(self.ui.treeView.model().indexFromItem(child_node))

                self.fill_tree(storage, chld["ID"], child_node)

    def display_item_info(self, index):

        selected_id = str(index.model().itemFromIndex(index).data().toString())
        storage_name = self.get_storage_name(index)

        if selected_id:
            item = self.databases.get_profile_info(**dict(database=storage_name, ID = selected_id))

            if item.__len__():
                name = unicode(item["Name"])
                server = unicode(item["Server"])
                if len(item["Port"]) == 0:
                    port = '3389'
                else:
                    port = str(item["Port"])
                user = unicode(item["User"])
                self.ui.labelStatus.setText(" Name - " + name + "\n"
                                            + " Server - " + server + "\n"
                                            + " Port - " + port + "\n"
                                            + " User - " + user + "\n\n")
            else:
                self.ui.labelStatus.setText("")

    def init_connection_fromwindow(self, index):

        selected_id = str(index.model().itemFromIndex(index).data().toString())
        if selected_id:
            storage_name = self.get_storage_name(index)
            self.init_connection(storage_name, selected_id)

    def init_connection_frommenu(self, menu_item):

        self.init_connection(menu_item['database'], menu_item['ID'])

    def init_connection(self, storage_name, selected_id):

        self.user_settings.update_item_rating(storage_name, selected_id)
        item = self.databases.get_profile_info(**dict(database=storage_name, ID=selected_id))
        if item:
            tempfile = serializer.Serializer().serialize_to_file_win_rdp(item, "7.1", item["Name"] + ".rdp")
            if tempfile:
                os.startfile(item["Name"] + ".rdp")
                time.sleep(5)
                os.remove(item["Name"] + ".rdp")

    def edit_item(self):

        index = self.ui.treeView.selectedIndexes()[0]
        selected_id = str(index.model().itemFromIndex(index).data().toString())
        storage_name = self.get_storage_name(index)

        item = self.databases.get_profile_info(**dict(database=storage_name, ID = selected_id))
        if item.__len__():
            input_dialog = itemedit.ItemEditDialog(self.databases,
                                          {"Storage": storage_name,
                                           "Parent": None,
                                           "ItemData": item,
                                           "Mode": "Edit"})
            input_dialog.ui.pushButtonClose.clicked.connect(lambda: input_dialog.close())
            input_dialog.exec_()
            self.show_connections_tree(False)

            item = self.databases.get_profile_info(**dict(database=storage_name, ID = selected_id))

            if item.__len__():
                name = unicode(item["Name"])
                server = unicode(item["Server"])
                port = str(item["Port"])
                user = unicode(item["User"])
                self.ui.labelStatus.setText(" Name - " + name + "\n"
                                            + " Server - " + server + "\n"
                                            + " Port - " + port + "\n"
                                            + " User - " + user + "\n\n")
            else:
                self.ui.labelStatus.setText("")

    def add_new_item(self):

        index = self.ui.treeView.selectedIndexes()
        if index:
            index = index[0]
            selected_name = unicode(index.model().itemFromIndex(index).text())
            storage_name = str(index.model().itemFromIndex(index).parent().text())
            item = self.databases.get_folder_id(**dict(database=storage_name, Name=selected_name))

            if item:
                item_data = {"Storage": storage_name, "Parent": str(item["ID"]), "ItemData": None, "Mode": "AddItem"}
                input_dialog = itemedit.ItemEditDialog(self.databases, item_data)
                input_dialog.exec_()
                if input_dialog.updated:
                    self.show_connections_tree(False)

    def add_new_folder(self):

        index = self.ui.treeView.selectedIndexes()[0]
        storage_name = str(index.model().itemFromIndex(index).text())
        item_data = {"Storage": storage_name, "Parent": str(1), "ItemData": None, "Mode": "AddFolder"}
        inputter = newfolder.NewGroupDialog(self.databases, item_data)
        inputter.exec_()
        if inputter.updated:
            self.show_connections_tree(False)

    def remove_item(self):

        index = self.ui.treeView.selectedIndexes()[0]
        selected_id = str(index.model().itemFromIndex(index).data().toString())
        storage_name = self.get_storage_name(index)
        if selected_id != self.ROOT_ELEMENT_ID:
            # if there are child elements, asking user before deleting
            child_elements = self.databases.get_child_elements(storage_name, selected_id)
            if child_elements.__len__():
                reply = QtGui.QMessageBox.question(self, 'Message', "Delete element with all child elements?",
                                                   QtGui.QMessageBox.Yes | QtGui.QMessageBox.No,
                                                   QtGui.QMessageBox.No)
                if reply == QtGui.QMessageBox.Yes:
                    self.databases.delete_group(storage_name, selected_id)
            else:
                reply = QtGui.QMessageBox.question(self, 'Message', "Delete element?",
                                                   QtGui.QMessageBox.Yes | QtGui.QMessageBox.No,
                                                   QtGui.QMessageBox.No)
                if reply == QtGui.QMessageBox.Yes:
                    self.databases.delete_group(storage_name, selected_id)

            self.show_connections_tree(False)

    def show_user_settings(self):

        settings_dialog = settings.UserSettingsDialog(self.user_settings)
        settings_dialog.exec_()
        self.show_connections_tree(False)

    @staticmethod
    def get_storage_name(index):

        item = index.model().itemFromIndex(index)
        storage_name = unicode(item.text())
        while item:
            if not item.parent():
                storage_name = unicode(item.text())
            item = item.parent()
        return storage_name


if __name__ == "__main__":

    app = QtGui.QApplication(sys.argv)
    app.setStyle("Plastique")
    window = MyWindow()
    window.move(QtCore.QPoint(app.desktop().screen().availableGeometry().width() - window.rect().width() - 15,
                              app.desktop().screen().availableGeometry().height() - window.rect().height() - 35))
    window.show()
    sys.exit(app.exec_())
