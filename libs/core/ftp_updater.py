# encoding: utf-8
from PyQt4 import QtCore, QtGui

import ftplib
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

        with closing(ftplib.FTP()) as ftp:
            try:
                ftp.connect(self.host, self.port)
                ftp.login(self.login, self.password)
                ftp.set_pasv(True)
                ftp.cwd("/")
                with open(self.local_filename, 'w+b') as f:
                    res = ftp.retrbinary('RETR %s' % self.orig_filename, f.write)
                    if not res.startswith('226 '):
                        msg = "Downloaded of file {0} is not compile.".format(self.orig_filename)
                        self.emit(QtCore.SIGNAL("show_msg(PyQt_PyObject)"), msg)
                        os.remove(self.local_filename)
            except:
                msg = "Error during downloading {0} from FTP".format(self.orig_filename)
                self.emit(QtCore.SIGNAL("show_msg(PyQt_PyObject)"), msg)

        self.emit(QtCore.SIGNAL("show_connections_tree()"), )



if __name__ == "__main__":
    pass