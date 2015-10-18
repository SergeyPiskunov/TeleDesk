# -*- coding: utf-8 -*-
import win32crypt
import binascii


class Serializer:

    def __init__(self):
        pass

    @staticmethod
    def serialize_to_text_win_rdp(connection_params, protocol_version):
        prepared_params = []

        #server + port
        if len(connection_params["Port"]) == 0:
            prepared_params.append("full address:s:"+connection_params["Server"]+":3389")
        else:
            prepared_params.append("full address:s:"+connection_params["Server"]+":"+connection_params["Port"])

        #username
        if connection_params["User"] != u'':
            prepared_params.append("username:s:"+connection_params["User"])

        #password
        if connection_params["Password"] != u'':
            pwdHash = win32crypt.CryptProtectData(connection_params["Password"], u'psw', None, None, None, 0)
            password = binascii.hexlify(pwdHash)
            prepared_params.append("password 51:b:"+password)

        #domain
        if connection_params["Domain"] != u'':
            prepared_params.append("domain:s:"+connection_params["Domain"])

        serialized_item = "\n".join(prepared_params)
        return serialized_item

    @staticmethod
    def serialize_to_file_win_rdp(connection_params, protocol_version, filename):

        serialized_text = Serializer.serialize_to_text_win_rdp(connection_params, protocol_version)
        with open(filename, "w") as s_file:
            s_file.write(serialized_text)
            s_file.close()
            return True
        return False


if __name__ == "__main__":
    pass


"""
#import win32crypt
#import binascii
#pwdHash = win32crypt.CryptProtectData(u"LSzx38$",u'psw',None,None,None,0)
#print binascii.hexlify(pwdHash)

+-----------------------------------+------+-----------------+-----+-----+-----+-----+-----+-----+-----+-----+
|              Setting              | Type |  Default value  | 5.1 | 5.2 | 6.0 | 6.1 | 7.0 | 7.1 | 8.0 | 8.1 |
+-----------------------------------+------+-----------------+-----+-----+-----+-----+-----+-----+-----+-----+
| administrative session            | i    | 0               |     |     |     | X   | X   | X   | X   | X   |
| allow desktop composition         | i    | 0               |     | X   | X   | X   | X   | X   | X   | X   |
| allow font smoothing              | i    | 0               |     | X   | X   | X   | X   | X   | X   | X   |
| alternate full address            | s    |                 |     |     |     |     | X   | X   | X   | X   |
| alternate shell                   | s    |                 | X   | X   | X   | X   | X   | X   | X   | X   |
| audiocapturemode                  | i    | 0               |     |     |     |     | X   | X   | X   | X   |
| audiomode                         | i    | 0               | X   | X   | X   | X   | X   | X   | X   | X   |
| audioqualitymode                  | i    | 0               |     |     |     |     | X   | X   | X   | X   |
| authentication level              | i    | 2               |     | X   | X   | X   | X   | X   | X   | X   |
| autoreconnect max retries         | i    | 20              | X   | X   | X   | X   | X   | X   | X   | X   |
| autoreconnection enabled          | i    | 1               | X   | X   | X   | X   | X   | X   | X   | X   |
| bitmapcachepersistenable          | i    | 1               |     | X   | X   | X   | X   | X   | X   | X   |
| bitmapcachesize                   | i    | 1500            | X   | X   | X   | X   | X   | X   | X   | X   |
| compression                       | i    | 1               | X   | X   | X   | X   | X   | X   | X   | X   |
| connect to console                | i    | 0               | X   | X   | X   |     |     |     |     |     |
| connection type                   | i    | 2               |     |     |     |     | X   | X   | X   | X   |
| desktopheight                     | i    | 600             | X   | X   | X   | X   | X   | X   | X   | X   |
| desktop size id                   | i    | 0               | X   | X   | X   | X   | X   | X   | X   | X   |
| desktopwidth                      | i    | 800             | X   | X   | X   | X   | X   | X   | X   | X   |
| devicestoredirect                 | s    |                 |     |     | X   | X   | X   | X   | X   | X   |
| disable ctrl+alt+del              | i    | 1               | X   | X   | X   | X   | X   | X   | X   | X   |
| disable full window drag          | i    | 1               | X   | X   | X   | X   | X   | X   | X   | X   |
| disable menu anims                | i    | 1               | X   | X   | X   | X   | X   | X   | X   | X   |
| disable themes                    | i    | 0               | X   | X   | X   | X   | X   | X   | X   | X   |
| disable wallpaper                 | i    | 1               | X   | X   | X   | X   | X   | X   | X   | X   |
| disableconnectionsharing          | i    | 0               |     |     | X   | X   | X   | X   | X   | X   |
| disableremoteappcapscheck         | i    | 0               |     |     |     |     | X   | X   | X   | X   |
| displayconnectionbar              | i    | 1               | X   | X   | X   | X   | X   | X   | X   | X   |
| domain                            | s    |                 | X   | X   | X   | X   | X   | X   | X   | X   |
| drivestoredirect                  | s    |                 |     |     | X   | X   | X   | X   | X   | X   |
| enablecredsspsupport              | i    | 1               |     |     | X   | X   | X   | X   | X   | X   |
| enablesuperpan                    | i    | 0               |     |     |     |     | X   | X   | X   | X   |
| full address                      | s    |                 | X   | X   | X   | X   | X   | X   | X   | X   |
| gatewaycredentialssource          | i    | 4               |     |     | X   | X   | X   | X   | X   | X   |
| gatewayhostname                   | s    |                 |     |     | X   | X   | X   | X   | X   | X   |
| gatewayprofileusagemethod         | i    | 0               |     |     | X   | X   | X   | X   | X   | X   |
| gatewayusagemethod                | i    | 4               |     |     | X   | X   | X   | X   | X   | X   |
| keyboardhook                      | i    | 2               | X   | X   | X   | X   | X   | X   | X   | X   |
| negotiate security layer          | i    | 1               |     |     | X   | X   | X   | X   | X   | X   |
| password 51                       | b    |                 | X   | X   | X   | X   | X   | X   | X   | X   |
| pinconnectionbar                  | i    | 1               | X   | X   | X   | X   | X   | X   | X   | X   |
| prompt for credentials            | i    | 0               |     |     | X   | X   | X   | X   | X   | X   |
| prompt for credentials on client  | i    | 0               |     |     |     | X   | X   | X   | X   | X   |
| promptcredentialonce              | i    | 1               |     |     |     | X   | X   | X   | X   | X   |
| public mode                       | i    | 0               |     |     |     |     | X   | X   | X   | X   |
| redirectclipboard                 | i    | 1               |     |     | X   | X   | X   | X   | X   | X   |
| redirectcomports                  | i    | 0               | X   | X   | X   | X   | X   | X   | X   | X   |
| redirectdirectx                   | i    | 1               |     |     |     |     | X   | X   | X   | X   |
| redirectdrives                    | i    | 0               | X   | X   |     |     |     |     |     |     |
| redirectposdevices                | i    | 0               |     |     | X   | X   | X   | X   | X   | X   |
| redirectprinters                  | i    | 1               | X   | X   | X   | X   | X   | X   | X   | X   |
| redirectsmartcards                | i    | 1               | X   | X   | X   | X   | X   | X   | X   | X   |
| remoteapplicationcmdline          | s    |                 |     |     | X   | X   | X   | X   | X   | X   |
| remoteapplicationfile             | s    |                 |     |     | X   | X   | X   | X   | X   | X   |
| remoteapplicationexpandcmdline    | i    | 1               |     |     | X   | X   | X   | X   | X   | X   |
| remoteapplicationexpandworkingdir | i    | 0               |     |     | X   | X   | X   | X   | X   | X   |
| remoteapplicationicon             | s    |                 |     |     | X   | X   | X   | X   | X   | X   |
| remoteapplicationmode             | i    | 0               |     |     | X   | X   | X   | X   | X   | X   |
| remoteapplicationname             | s    |                 |     |     | X   | X   | X   | X   | X   | X   |
| remoteapplicationprogram          | s    |                 |     |     |     | X   | X   | X   | X   | X   |
| screen mode id                    | i    | 2               | X   | X   | X   | X   | X   | X   | X   | X   |
| server port                       | i    | 3389            | X   | X   | X   | X   | X   | X   | X   | X   |
| session bpp                       | i    | 32              | X   | X   | X   | X   | X   | X   | X   | X   |
| shell working directory           | s    |                 | X   | X   | X   | X   | X   | X   | X   | X   |
| smart sizing                      | i    | 0               | X   | X   | X   | X   | X   | X   | X   | X   |
| span monitors                     | i    | 0               |     |     | X   | X   | X   | X   | X   | X   |
| superpanaccelerationfactor        | i    | 1               |     |     |     |     | X   | X   | X   | X   |
| usbdevicestoredirect              | s    |                 |     |     |     |     |     | X   | X   | X   |
| use multimon                      | i    | 0               |     |     |     |     | X   | X   | X   | X   |
| username                          | s    |                 | X   | X   | X   | X   | X   | X   | X   | X   |
| videoplaybackmode                 | i    | 1               |     |     |     |     | X   | X   | X   | X   |
| winposstr                         | s    | 0,3,0,0,800,600 | X   | X   | X   | X   | X   | X   | X   | X   |
+-----------------------------------+------+-----------------+-----+-----+-----+-----+-----+-----+-----+-----+




"""


