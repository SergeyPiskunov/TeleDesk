# encoding: utf-8
import ftplib
import os.path
from contextlib import closing


class FTPConnector(object):
    """ Object handles main FTP operations
        after any operation returns dict [is success, message] """

    def __init__(self, ftp_params):
        self.host = ftp_params['FTP_Server']
        self.port = ftp_params['FTP_Port']
        self.login = ftp_params['FTP_User']
        self.password = ftp_params['FTP_Password']
        #self.folder = ftp_params['FTP_Folder']

    def download(self, ftp_file, local_file):
        with closing(ftplib.FTP()) as ftp:
            try:
                ftp.connect(self.host, self.port)
                ftp.login(self.login, self.password)
                ftp.set_pasv(True)
                ftp.cwd("/")
                with open(local_file, 'w+b') as f:
                    res = ftp.retrbinary('RETR %s' % ftp_file, f.write)
                    if not res.startswith('226 '):
                        message = "Downloaded of file {0} is not compile.".format(ftp_file)
                        os.remove(local_file)
                        return dict(success=False, message=message)
            except:
                message = "Error during downloading {0} from FTP".format(ftp_file)
                return dict(success=False, message=message)

        message = "File {0} successfully downloaded".format(ftp_file)
        return dict(success=True, message=message)

    def upload(self, ftp_file, local_file):
        pass


if __name__ == "__main__":
    pass