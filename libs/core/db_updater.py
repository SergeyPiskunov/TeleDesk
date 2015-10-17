# encoding: utf-8
from PyQt4 import QtCore
import ftp_connector


class DBUpdater(QtCore.QThread):
    """ Updates all non-local databases
     and provides status callbacks to the main GUI  """

    def __init__(self, storages, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.storages = storages

    def update(self):
        self.start()

    def run(self):
        for database in self.storages:
            if database["Type"] == 'ftp':
                FTPConnector = ftp_connector.FTPConnector(database["Properties"])
                result = FTPConnector.download(database["Path"], database["Path"])
                if result["success"]:
                    self.emit(QtCore.SIGNAL("show_connections_tree()"), )
                else:
                    self.emit(QtCore.SIGNAL("show_msg(PyQt_PyObject)"), result["message"])


if __name__ == "__main__":
    pass