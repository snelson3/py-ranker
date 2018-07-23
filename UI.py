from TextDB import TextDB
from Category import Category
import os

MY_DB = TextDB
DATA_PATH = 'sourceData'

class UI:
    def __init__(self):
        self.path = DATA_PATH
        self.availableCategories = self._findCategories()
        while 1:
            self.category = Category(os.path.join(DATA_PATH, self.select_category()))
            while self.category:
                action = self.category_menu()
                while action == 'rate':
                    r = self._rank2()
                    if r < 0:
                        action = None
                if action == 'config':
                    self._setConfig()
                elif action == 'view':
                    self.view_items()
                elif action == 'rank':
                    self.rank_items_menu()
                elif action == 'back':
                    self.category = None

    def _findCategories(self):
        return list(os.walk(DATA_PATH))[0][1]

    def _rank2(self):
        items = self.category.getNewPair()
        r = self.rank_2_menu(items[0], items[1])
        if r == -1:
            return -1
        return self.category.rate(items, r)

    def _setConfig(self):
        config = {
            "duplicates": {
                "type": ["count", "newest", "oldest"],
                "value": None
            },
            "new_only": {
                "type": bool,
                "value": None
            },
            "pick_least_picked": {
                "type": bool,
                "value": None
            }
        }
        if "duplicates" in self.category.config:
            config["duplicates"]["value"] = self.category.config["duplicates"]
        if "new_only" in self.category.config:
            config["new_only"]["value"] = self.category.config["new_only"]
        if "pick_least_picked" in self.category.config:
            config["pick_least_picked"]["value"] = self.category.config["pick_least_picked"]
        config = self.config_menu(config)
        for k in config:
            if config[k]["value"]:
                self.category.config[k] = config[k]["value"]
        self.category.saveConfig()

    def select_category(self):
        # Given availableCategories select one of the categories to look at
        pass

    def rank_2_menu(self, x1, x2):
        # Given two objects, return the better one
        # return index of the winner, or -1 to indicate back, or undo to undo
        pass

    def category_menu(self):
        # Main menu for the category
        pass

    def rank_items_menu(self):
        pass

    def view_items(self):
        pass

    def config_menu(self, schema, config):
        pass

