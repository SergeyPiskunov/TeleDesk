import db_connector


class DataBase(db_connector.DBConnector):

    def __init__(self, db_name, db_type, db_file):
        db_connector.DBConnector.__init__(self, db_file)
        self.name = db_name
        self.type = db_type
        self.path = db_file


class DataStorage():

    def __init__(self, data_sources):
        self.data_bases = {}
        for db in data_sources:
            database = DataBase(db["Name"], db["Type"], db["Path"])
            self.data_bases[db["Name"]] = database

    def get_folders_children(self, database, parameters=None):
        dat = self.data_bases.get(database)
        return dat.get_data("SELECT * FROM FOLDERS WHERE PARENT = ?", parameters)

    def get_profile_info(self, database, parameters=None):
        dat = self.data_bases.get(database)
        return dat.get_data("SELECT * FROM PROFILES LEFT JOIN FOLDERS ON FOLDERS.Profile = PROFILES.ID WHERE FOLDERS.NAME = ?", parameters)

    def get_folder_id(self, database, parameters=None):
        dat = self.data_bases.get(database)
        return dat.get_data("SELECT ID FROM FOLDERS WHERE PROFILE = '' AND NAME = ?", parameters)

    def get_profile_id(self, database, parameters=None):
        dat = self.data_bases.get(database)
        return dat.get_data("SELECT ID FROM PROFILES WHERE NAME = ?", parameters)

    def create_new_profile(self, database, name, server, port, user):
        dat = self.data_bases.get(database)
        dat.execute("INSERT INTO `PROFILES`(`Name`,`Alias`,`Server`,`Port`,`User`) VALUES (\""+name+"\",\""+ name +"\",\""+ server +"\",\""+ port +"\",\""+ user +"\")")

    def create_new_profile_folder(self, database, parent, name, id):
        dat = self.data_bases.get(database)
        dat.execute("INSERT INTO `FOLDERS`(`Parent`,`Name`,`Profile`) VALUES (" + parent + ",\"" + name + "\"," + id + ")")

    def create_new_folder(self, database, parent, name):
        dat = self.data_bases.get(database)
        dat.execute("INSERT INTO `FOLDERS`(`Parent`,`Name`,`Profile`) VALUES (" + parent + ",\"" + name + "\" , '')")

    def delete_folder(self, database, name):
        dat = self.data_bases.get(database)
        dat.execute("DELETE FROM FOLDERS WHERE NAME = \"" + name + "\"")

if __name__ == "__main__":
    pass