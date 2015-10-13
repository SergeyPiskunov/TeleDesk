# encoding: utf-8
from PyQt4 import QtCore

from ftplib import FTP
from datetime import datetime
import os.path, time
from contextlib import closing


class FTPUpdater(QtCore.QThread):
    def __init__(self, ui, ftp_params, parent=None):
        QtCore.QThread.__init__(self, parent)

        self.ui = ui

        self.host = ftp_params["Properties"]['Server']
        self.port = ftp_params["Properties"]['Port']
        self.login = ftp_params["Properties"]['FTPUser']
        self.password = ftp_params["Properties"]['FTPPassword']
        self.orig_filename = ftp_params['Path']
        self.local_filename = ftp_params['Path']

    def update(self):
        self.start()

    def run(self):

        i = self.local_filename
        ftp = FTP(self.host)
        ftp.login(self.login, self.password)
        ftp.cwd("/")
        try:
            ftp.retrbinary("RETR " + self.local_filename, open(i, 'wb').write)
        except:
            print "Error"

        self.emit(QtCore.SIGNAL("show_connections_tree()"), )


if __name__ == "__main__":
    pass