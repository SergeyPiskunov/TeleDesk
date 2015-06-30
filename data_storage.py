import db_connector


class DataBase(db_connector.DBConnector):
    """ Keeps an instance of a database
    and it's name, path, type [local or shared]"""

    def __init__(self, db_name, db_type, db_file):
        db_connector.DBConnector.__init__(self, db_file)
        self.name = db_name
        self.type = db_type
        self.path = db_file


class DataStorage():
    """ Keeps all SQL queries and provides
    them as short methods """

    def __init__(self, data_sources):
        self.data_bases = {}
        for db in data_sources:
            database = DataBase(db["Name"], db["Type"], db["Path"])
            self.data_bases[db["Name"]] = database

    def get_folders_children(self, database, parameters=None):
        source = self.data_bases.get(database)
        return source.get_data("SELECT * FROM FOLDERS WHERE PARENT = ?", parameters)

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
        return source.get_data("SELECT ID FROM PROFILES WHERE NAME = ? ORDER BY ID DESC LIMIT 1", parameters)

    def create_new_profile(self, database, name, server, domain, port, user, password):
        source = self.data_bases.get(database)
        source.execute(
            "INSERT INTO `PROFILES`(`Name`,`Alias`,`Rating`,`Server`,`Domain`,`Port`,`User`,`Password`) VALUES (\""
            + name + "\",\""
            + name + "\",\""
            + "1" + "\",\""
            + server + "\",\""
            + domain + "\",\""
            + port + "\",\""
            + user + "\",\""
            + password + "\")")

    def update_profile(self, database, idd, name, server, domain, port, user, password):
        source = self.data_bases.get(database)
        source.execute("UPDATE `PROFILES` SET "
                       "  'Alias'='" + name +
                       "','SERVER'='" + server +
                       "','DOMAIN'='" + domain +
                       "','PORT'='" + port +
                       "','USER'='" + user +
                       "' WHERE ID =" + str(idd))

        if password != u'':
            source.execute("UPDATE `PROFILES` SET "
                           " 'PASSWORD'='" + password +
                           "' WHERE ID =" + str(idd))

    def create_new_profile_folder(self, database, parent, name, idd):
        source = self.data_bases.get(database)
        source.execute(
            "INSERT INTO `FOLDERS`(`Parent`,`Name`,`Profile`) VALUES ("
            + parent + ",\""
            + name + "\","
            + idd + ")")

    def create_new_folder(self, database, parent, name):
        source = self.data_bases.get(database)
        source.execute("INSERT INTO `FOLDERS`(`Parent`,`Name`,`Profile`) VALUES ("
                       + parent + ",\""
                       + name + "\" , '')")

    def get_child_elements(self, database, idd):
        source = self.data_bases.get(database)
        return source.get_data("SELECT ID FROM PROFILES WHERE ID IN (SELECT PROFILE FROM FOLDERS WHERE PARENT = ?)", idd)

    def delete_folder(self, database, idd):
        source = self.data_bases.get(database)

        #deleting all child profiles
        source.execute("DELETE FROM PROFILES WHERE ID IN (SELECT PROFILE FROM FOLDERS WHERE PARENT = \"" + idd + "\")")

        #deleting all child folders
        source.execute("DELETE FROM FOLDERS WHERE PARENT = \"" + idd + "\"")

        #deleting folder
        source.execute("DELETE FROM PROFILES WHERE ID IN (SELECT PROFILE FROM FOLDERS WHERE ID = \"" + idd + "\")")

        #deleting profile
        source.execute("DELETE FROM FOLDERS WHERE ID = \"" + idd + "\"")

    def update_item_rating(self, database, idd):
        source = self.data_bases.get(database)
        source.execute("UPDATE PROFILES SET RATING = RATING + 1 WHERE PROFILES.ID IN (SELECT PROFILE FROM FOLDERS WHERE FOLDERS.ID = "+idd+")")


if __name__ == "__main__":
    pass
