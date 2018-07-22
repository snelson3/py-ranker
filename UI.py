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
                while action == 'config':
                    pass
                while action == 'view':
                    pass
                if action == 'rank':
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