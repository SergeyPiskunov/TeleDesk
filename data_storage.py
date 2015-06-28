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

    def create_new_profile(self, database, name, server, port, user):
        source = self.data_bases.get(database)
        source.execute(
            "INSERT INTO `PROFILES`(`Name`,`Alias`,`Server`,`Port`,`User`) VALUES (\""
            + name + "\",\""
            + name + "\",\""
            + server + "\",\""
            + port + "\",\""
            + user + "\")")

    def update_profile(self, database, id, name, server, port, user):
        source = self.data_bases.get(database)
        source.execute("UPDATE `PROFILES` SET "
                       "  'Alias'='" + name +
                       "','SERVER'='" + server +
                       "','PORT'='" + port +
                       "','USER'='" + user +
                       "' WHERE ID =" + str(id))

    def create_new_profile_folder(self, database, parent, name, id):
        source = self.data_bases.get(database)
        source.execute(
            "INSERT INTO `FOLDERS`(`Parent`,`Name`,`Profile`) VALUES ("
            + parent + ",\""
            + name + "\","
            + id + ")")

    def create_new_folder(self, database, parent, name):
        source = self.data_bases.get(database)
        source.execute("INSERT INTO `FOLDERS`(`Parent`,`Name`,`Profile`) VALUES ("
                       + parent + ",\""
                       + name + "\" , '')")

    def delete_folder(self, database, idd):
        source = self.data_bases.get(database)
        source.execute("DELETE FROM PROFILES WHERE PROFILES.ID IN "
                       "(SELECT PROFILES.ID FROM PROFILES LEFT JOIN FOLDERS "
                       "ON FOLDERS.Profile = PROFILES.ID WHERE FOLDERS.ID = \"" + idd + "\")")

        source.execute("DELETE FROM PROFILES WHERE ID IN (SELECT FOLDERS.PROFILE FROM FOLDERS WHERE FOLDERS.ID = \"" + idd + "\")")
        source.execute("DELETE FROM FOLDERS WHERE ID = \"" + idd + "\"")
        source.execute("DELETE FROM FOLDERS WHERE PARENT = \"" + idd + "\"")

if __name__ == "__main__":
    pass
