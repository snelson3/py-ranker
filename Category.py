from TextDB import TextDB
import os, itertools
import random

MY_DB = TextDB

class Category:
    def __init__(self, fn):
        if not os.path.isfile(os.path.join(fn, "list")):
            raise Exception("No Category list file!")
        self.name = None # Get this from the config file
        self.fn = fn
        self.items = self.getItems()
        self.db = MY_DB(self.fn)
        self.undoStack = []

    def readCategory(self):
        return open(os.path.join(self.fn, "list")).read().split("\n")

    def getItems(self):
        l = self.readCategory()
        return list(map(lambda i: {"name": i}, l))

    def getNumRates(self):
        return len(self.db.getUniqueRates())

    def getTotalRates(self):
        return len(list(itertools.combinations(self.items,2)))

    def getRandomItems(self, n=2):
        # Inefficient
        x = list(self.items)
        random.shuffle(x)
        return [x.pop(0) for i in range(n)]

    def getNewPair(self):
        if len(self.undoStack) > 0:
            return self.undoStack.pop()
        return self.getRandomItems()

    def rate(self, items, r):
        if r == 'undo':
            self.undoStack.append(items)
            self.undoStack.append(self.db.remove1())
            return 0
        self.db.add1(items.pop(r), items[0])
        return 0
