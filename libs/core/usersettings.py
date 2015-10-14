# -*- coding: utf-8 -*-
from contextlib import contextmanager
import pickle


class UserSettings(object):
    """ Initializing with path to user settings file.
    Allow to load and save user settings via pickle """

    def __init__(self, config_file='u_config.cfg'):
        self.config_file = config_file
        self.master_login = ''
        self.master_password = ''
        self.ui_language = ''
        self.databases = {}
        self.top_ten_connections = {}

    def reset_to_dafaults(self, config_file=None):
        """ Writes default settings to the self.config_file """
        self.master_login = 'root'
        self.master_password = 'toor'
        self.ui_language = 'en'
        self.top_ten_connections = {}
        self.databases = [{"Name": "local",
                           "Type": "local",
                           "Path": "local.db",
                           "User": "",
                           "Password": "",
                           "Properties": {}}]
        self.save_config()

    def load_config(self):
        """ Loads all user settings from the self.config_file """
        try:
            with open(self.config_file, 'rb') as cfg_file:
                config = pickle.load(cfg_file)
                self.master_login = config['master_login']
                self.master_password = config['master_password']
                self.ui_language = config['ui_language']
                self.databases = config['databases']
                self.top_ten_connections = config['top_ten_connections']
        except IOError:
            self.reset_to_dafaults()
            self.load_config()

    def save_config(self):
        """ Saves all user settings in the self.config_file """
        config = {
            'ui_language': self.ui_language,
            'master_login': self.master_login,
            'master_password': self.master_password,
            'databases': self.databases,
            'top_ten_connections': self.top_ten_connections}
        with open(self.config_file, 'wb') as cfg_file:
            pickle.dump(config, cfg_file)

    def update_item_rating(self, storage_name, item):
        """ Increments usage rating of given connection
            in a given storage name"""
        if storage_name in self.top_ten_connections.keys():
            if item in self.top_ten_connections[storage_name].keys():
                self.top_ten_connections[storage_name][item] += 1
            else:
                self.top_ten_connections[storage_name][item] = 1
        else:
            self.top_ten_connections[storage_name] = {item: 1}
        self.save_config()

    def get_top_ten_connections(self, storage_name, items=5):
        """ Returns top(items) most frequently used connections """
        if self.top_ten_connections:

            if not self.top_ten_connections.has_key(storage_name):
                return None

            top_list = sorted(self.top_ten_connections[storage_name].items(), key=lambda x: x[1], reverse=True)
            result = []
            if items > len(top_list):
                items = len(top_list)
            for i in range(items):
                result.append(top_list[i])
            return result
        else:
            return None


if __name__ == "__main__":
    user_settings = UserSettings()
    user_settings.reset_to_dafaults()
    # user_settings.load_config()
