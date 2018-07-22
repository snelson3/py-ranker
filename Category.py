from TextDB import TextDB
import os, itertools

MY_DB = TextDB

class Category:
    def __init__(self, fn):
        if not os.path.isfile(os.path.join(fn, "list")):
            raise Exception("No Category list file!")
        self.fn = fn
        self.items = self.getItems()
        self.db = MY_DB(self.fn)

    def readCategory(self):
        return open(os.path.join(self.fn, "list")).read().split("\n")

    def getItems(self):
        l = self.readCategory()
        return list(map(lambda i: {"name": i}, l))

    def getNumRates(self):
        return len(self.db.getUniqueRates())

    def getTotalRates(self):
        return len(list(itertools.combinations(self.items,2)))