# -*- coding: utf-8 -*-
from dbconnector import DBConnector


class DataBase(DBConnector):
    """ Keeps an instance of a database
    and it's name, path, type [local or shared]"""

    def __init__(self, **kwargs):
        DBConnector.__init__(self, kwargs['Path'])
        self.name = kwargs['Name']
        self.type = kwargs['Type']
        self.path = kwargs['Path']


class DataStorage():
    """ Keeps all SQL queries and provides
    them as short methods """

    def __init__(self, data_sources):
        self.data_bases = {}
        for db in data_sources:
            database = DataBase(**db)
            self.data_bases[db["Name"]] = database
            #if the database is blank create all necessary tables
            tables = database.get_data("SELECT name FROM sqlite_master")
            if not tables:
                database.execute("CREATE TABLE `FOLDERS` ("
                                 "`ID` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,"
                                 "`Parent` INTEGER,"
                                 "`Name` TEXT,"
                                 "`Profile` TEXT);")

                database.execute("CREATE TABLE `PROFILES` ("
                                 "`ID` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,"
                                 "`Rating` INTEGER,"
                                 "`Server` TEXT,"
                                 "`Port` TEXT,"
                                 "`User` TEXT,"
                                 "`Domain` TEXT,"
                                 "`Password` TEXT,"
                                 "`Folder` INTEGER);")

                database.execute("INSERT INTO `FOLDERS`(`Parent`,`Name`,`Profile`) VALUES ("
                                 "NULL,'" + db["Name"] + "', NULL)")

    def get_folders_children(self, database, parameters=None):
        source = self.data_bases.get(database)
        return source.get_data("SELECT * FROM FOLDERS WHERE PARENT = ?", parameters, True)

    def get_profile_info(self, database, parameters=None):
        source = self.data_bases.get(database)
        return source.get_data(
            "SELECT * FROM PROFILES LEFT JOIN FOLDERS ON FOLDERS.Profile = PROFILES.ID WHERE FOLDERS.ID = ?",
            parameters)

    def get_folder_id(self, database, parameters=None):
        source = self.data_bases.get(database)
        return source.get_data("SELECT ID FROM FOLDERS WHERE PROFILE = '' AND NAME = ?", parameters)

    def get_profile_id(self, database, parameters=None):
        source = self.data_bases.get(database)
        # return source.get_data("SELECT ID FROM PROFILES WHERE NAME = ? ORDER BY ID DESC LIMIT 1", parameters)
        return source.get_data(
            "SELECT ID FROM PROFILES WHERE PROFILES.ID IN (SELECT FOLDERS.Profile FROM FOLDERS WHERE FOLDERS.Name = ?) ORDER BY ID DESC LIMIT 1",
            parameters)

    def get_child_elements(self, database, idd):
        source = self.data_bases.get(database)
        return source.get_data("SELECT ID FROM PROFILES WHERE ID IN (SELECT PROFILE FROM FOLDERS WHERE PARENT = ?)",
                               idd, True)

    def delete_folder(self, database, idd):
        source = self.data_bases.get(database)

        # deleting all child profiles
        source.execute("DELETE FROM PROFILES WHERE ID IN (SELECT PROFILE FROM FOLDERS WHERE PARENT = \"" + idd + "\")")

        # deleting all child folders
        source.execute("DELETE FROM FOLDERS WHERE PARENT = \"" + idd + "\"")

        # deleting folder
        source.execute("DELETE FROM PROFILES WHERE ID IN (SELECT PROFILE FROM FOLDERS WHERE ID = \"" + idd + "\")")

        # deleting profile
        source.execute("DELETE FROM FOLDERS WHERE ID = \"" + idd + "\"")

    def create_new_folder(self, database, parent, name):
        source = self.data_bases.get(database)
        source.execute("INSERT INTO `FOLDERS`(`Parent`,`Name`,`Profile`) VALUES ("
                       + parent + ",\""
                       + name + "\" , '')")

    def create_new_profile(self, **kwargs):
        source = self.data_bases.get(kwargs['storage_name'])
        lastrow = source.execute(
            "INSERT INTO `PROFILES`(`Rating`,`Server`,`Domain`,`Port`,`User`,`Password`) VALUES (\""
            + "1" + "\",\""
            + kwargs['server'] + "\",\""
            + kwargs['domain'] + "\",\""
            + kwargs['port'] + "\",\""
            + kwargs['user'] + "\",\""
            + kwargs['password'] + "\")", None, True)

        source.execute(
            "INSERT INTO `FOLDERS`(`PARENT`, 'NAME', 'PROFILE') VALUES (\""
            + kwargs['parent'] + "\",\""
            + kwargs['name'] + "\",\""
            + str(lastrow) + "\")")

    def update_profile(self, **kwargs):

        source = self.data_bases.get(kwargs['storage_name'])
        source.execute("UPDATE `PROFILES` SET "
                       "  'SERVER'='" + kwargs['server'] +
                       "','DOMAIN'='" + kwargs['domain'] +
                       "','PORT'='" + kwargs['port'] +
                       "','USER'='" + kwargs['user'] +
                       "' WHERE ID =" + str(kwargs['item_to_edit']))

        source.execute("UPDATE `FOLDERS` SET "
                       " 'NAME'='" + kwargs['name'] +
                       "' WHERE PROFILE =" + str(kwargs['item_to_edit']))

        if kwargs['password'] != u'':
            source.execute("UPDATE `PROFILES` SET "
                           " 'PASSWORD'='" + kwargs['password'] +
                           "' WHERE ID =" + str(kwargs['item_to_edit']))



if __name__ == "__main__":
    pass
