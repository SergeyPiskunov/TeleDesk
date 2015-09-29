import pickle


class UserSettings(object):
    """ Initializing with path to user settings file.
    Allow to load and save user settings via pickle """

    def __init__(self, config_path='uconfig.cfg'):
        self.config_path = config_path
        self.config = {}
        self.login = ''
        self.password = ''
        self.language = ''
        self.dbs = {}
        self.topten = {}

    def reset_to_dafaults(self):
        self.login = 'root'
        self.password = 'toor'
        self.language = 'en'
        self.topten = {"Local_storage": {}}
        self.dbs = {'local_storage': {"Name": "Local_storage", "Type": "local", "Path": "config.db"},
                    'Common_storage': {"Name": "Common_storage", "Type": "local", "Path": "config2.db"}}
        self.save_config()

    def load_config(self):
        with open(self.config_path, 'rb') as p_file:
            self.config = pickle.load(p_file)
            self.login = self.config['login']
            self.password = self.config['password']
            self.language = self.config['language']
            self.dbs = self.config['storage_settings']
            self.topten = self.config['topten']

    def save_config(self):
        self.config = {
            'language': self.language,
            'login': self.login,
            'password': self.password,
            'storage_settings': self.dbs,
            'topten': self.topten}
        with open(self.config_path, 'wb') as p_file:
            pickle.dump(self.config, p_file)

    def update_item_rating(self, storage_name, item):
        if storage_name in self.topten.keys():
            if item in self.topten[storage_name].keys():
                self.topten[storage_name][item] += 1
            else:
                self.topten[storage_name][item] = 1
        else:
            self.topten[storage_name] = {item: 1}

        with open(self.config_path, 'wb') as p_file:
            pickle.dump(self.config, p_file)


    def get_rated_items(self, storage_name, items=5):
        toplist = sorted(self.topten[storage_name].items(), key=lambda x: x[1], reverse=True)
        #print storage_name, toplist, self.topten
        result = []
        if items > len(toplist):
            items = len(toplist)

        for i in range(items):
            result.append(toplist[i][0])

        #print storage_name, result
        return toplist


if __name__ == "__main__":
    usersettings = UserSettings()
    usersettings.reset_to_dafaults()
    # usersettings.load_config()
