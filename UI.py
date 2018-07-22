from TextDB import TextDB
from Category import Category
import os

MY_DB = TextDB
DATA_PATH = 'sourceData'

class UI:
    def __init__(self):
        self.path = DATA_PATH
        self.availableCategories = self._findCategories()
        self.category = Category(os.path.join(DATA_PATH, self.select_category()))
        numRates = self.category.getNumRates()
        print(numRates)
        totalRates = self.category.getTotalRates()
        print("{}% Complete ({} Rates Left)".format(int((numRates/totalRates)*100), totalRates-numRates))
        pass

    def _findCategories(self):
        return list(os.walk(DATA_PATH))[0][1]

    def select_category(self):
        # Given availableCategories select one of the categories to look at
        pass

    def rank_2(self, x1, x2):
        # Given two objects, return the better one
        pass
