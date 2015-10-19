# -*- coding: utf-8 -*-
from dbconnector import DBConnector
from libs.third_parity import pyaes


class DataBase(DBConnector):
    """ Keeps an instance of a database
    and it's name, path, type [local or shared] """

    def __init__(self, **kwargs):
        DBConnector.__init__(self, kwargs['Path'], len(kwargs['Password']) != 0)
        self.name = kwargs['Name']
        self.type = kwargs['Type']
        self.path = kwargs['Path']

        # According to the AES128 password length must be 16
        if len(kwargs['Password']) != 0:
            key = kwargs['Password']
            if len(key) > 16:
                key = key[:16]
            if len(key) < 16:
                i = 0
                while len(key) < 16:
                    key = key + key[i]
                    i = i + 1
            self.password = key


class DataStorage():
    """ Keeps all SQL queries and provides
    them as short methods """

    def __init__(self, data_sources):
        self.data_bases = {}
        self.crypted_fields = ['Name', 'Server', 'User', 'Password']
        for db in data_sources:
            database = DataBase(**db)
            self.data_bases[db["Name"]] = database

            # if the database is blank(new) create all necessary tables
            tables = database.get_data("SELECT name FROM sqlite_master")
            if not tables:
                database.execute("CREATE TABLE `FOLDERS` ("
                                 "`ID` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,"
                                 "`Parent` INTEGER,"
                                 "`Name` TEXT,"
                                 "`Profile` TEXT);")

                database.execute("CREATE TABLE `PROFILES` ("
                                 "`ID` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,"
                                 "`Server` TEXT,"
                                 "`Port` TEXT,"
                                 "`User` TEXT,"
                                 "`Domain` TEXT,"
                                 "`Password` TEXT)")

                database.execute("INSERT INTO `FOLDERS`(`Parent`,`Name`,`Profile`) VALUES ("
                                 "NULL,'" + db["Name"] + "', NULL)")

    def encrypted(iput_func):
        def encryption_wrapper(self, **kwargs):
            source = self.data_bases.get(kwargs['database'])
            if hasattr(source, 'password') and source.password != u'':
                for fieldname in self.crypted_fields:
                    if kwargs.has_key(fieldname):
                        aes = pyaes.AESModeOfOperationCTR(source.password)
                        kwargs[fieldname] = aes.encrypt(kwargs[fieldname].encode("utf8"))
            return iput_func(self, **kwargs)
        return encryption_wrapper

    def decrypted(input_func):
        def decryption_wrapper(self, *args, **kwargs):
            source = self.data_bases.get(kwargs['database'])
            if hasattr(source, 'password') and source.password != u'':
                result = input_func(self, *args, **kwargs)
                if isinstance(result, list):
                    for result_dict in result:
                        for fieldname in self.crypted_fields:
                            if result_dict.has_key(fieldname):
                                aes = pyaes.AESModeOfOperationCTR(source.password)
                                result_dict[fieldname] = unicode(aes.decrypt(result_dict[fieldname]).decode("utf8"))
                else:
                    for fieldname in self.crypted_fields:
                        if result.has_key(fieldname):
                            aes = pyaes.AESModeOfOperationCTR(source.password)
                            result[fieldname] = unicode(aes.decrypt(result[fieldname]).decode("utf8"))
                return result
            else:
                return input_func(self, *args, **kwargs)
        return decryption_wrapper

    @decrypted
    def get_folders_children(self, **kwargs):
        source = self.data_bases.get(kwargs['database'])
        return source.get_data("SELECT * FROM FOLDERS WHERE PARENT = ?", kwargs['parent'], True)

    @decrypted
    def get_profile_info(self, **kwargs):
        source = self.data_bases.get(kwargs['database'])

        return source.get_data("SELECT * FROM PROFILES "
                               "LEFT JOIN FOLDERS "
                               "ON FOLDERS.Profile = PROFILES.ID "
                               "WHERE FOLDERS.ID = ?",
                               kwargs['ID'])

    @encrypted
    def get_folder_id(self, **kwargs):
        source = self.data_bases.get(kwargs['database'])

        return source.get_data("SELECT ID FROM FOLDERS "
                               "WHERE NAME =? AND PROFILE is null",
                               (kwargs['Name']))

    @encrypted
    def get_profile_id(self, **kwargs):
        source = self.data_bases.get(kwargs['database'])

        return source.get_data("SELECT ID FROM PROFILES "
                               "WHERE PROFILES.ID IN "
                               "(SELECT FOLDERS.Profile FROM FOLDERS "
                               "WHERE FOLDERS.Name = ?) "
                               "ORDER BY ID DESC LIMIT 1",
                               kwargs['Name'])

    def get_child_elements(self, database, idd):
        source = self.data_bases.get(database)

        return source.get_data("SELECT ID FROM PROFILES "
                               "WHERE ID IN "
                               "(SELECT PROFILE FROM FOLDERS "
                               "WHERE PARENT = ?)",
                               idd, True)

    def delete_group(self, database, idd):
        source = self.data_bases.get(database)

        # deleting all child profiles
        source.execute("DELETE FROM PROFILES "
                       "WHERE ID IN "
                       "(SELECT PROFILE FROM FOLDERS "
                       "WHERE PARENT =?)", (idd,))

        # deleting all child folders
        source.execute("DELETE FROM FOLDERS "
                       "WHERE PARENT =?", (idd,))

        # deleting folder
        source.execute("DELETE FROM PROFILES "
                       "WHERE ID IN "
                       "(SELECT PROFILE FROM FOLDERS "
                       "WHERE ID = ?)", (idd,))

        # deleting profile
        source.execute("DELETE FROM FOLDERS "
                       "WHERE ID = ?", (idd,))

    @encrypted
    def create_new_group(self, **kwargs):
        source = self.data_bases.get(kwargs['database'])

        source.execute("INSERT INTO FOLDERS ("
                       "Parent, "
                       "Name "
                       ") VALUES (?,?) ",
                       (kwargs['parent'],
                        kwargs['Name']))

    @encrypted
    def create_new_profile(self, **kwargs):
        source = self.data_bases.get(kwargs['database'])

        # Inserting connection properties
        lastrow = source.execute("INSERT INTO PROFILES("
                                 "Server, "
                                 "Port, "
                                 "User, "
                                 "Domain, "
                                 "Password"
                                 ") VALUES (?,?,?,?,?) ",
                                 (kwargs['Server'],
                                  kwargs['Port'],
                                  kwargs['User'],
                                  kwargs['Domain'],
                                  kwargs['Password'],), True)

        # Inserting group/name
        source.execute("INSERT INTO FOLDERS("
                       "Parent, "
                       "Name, "
                       "Profile "
                       ") VALUES (?,?,?)",
                       (str(kwargs['parent']),
                        kwargs['Name'],
                        str(lastrow)))

    @encrypted
    def update_profile(self, **kwargs):
        database = self.data_bases.get(kwargs['database'])

        # Updating connection properties
        database.execute("UPDATE PROFILES "
                         "SET "
                         "Server=?, "
                         "Port=?, "
                         "User=?, "
                         "Domain=?, "
                         "Password=? "
                         "WHERE "
                         "ID =? ",
                         (kwargs['Server'],
                          kwargs['Port'],
                          kwargs['User'],
                          kwargs['Domain'],
                          kwargs['Password'],
                          kwargs['item_to_edit']))

        # Updating connection name
        database.execute("UPDATE FOLDERS "
                         "SET "
                         "Name=? "
                         "WHERE "
                         "Profile =? ",
                         (kwargs['Name'],
                          kwargs['item_to_edit']))



if __name__ == "__main__":
    pass
