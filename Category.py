from TextDB import TextDB
from Rankers import *
import os, itertools
import random

MY_DB = TextDB

class Category:
    def __init__(self, fn):
        if not os.path.isfile(os.path.join(fn, "list")):
            raise Exception("No Category list file!")
        if not os.path.isfile(os.path.join(fn, "config")):
            raise Exception("No Config File!")
        self.fn = fn
        self.config = self.readConfig()
        if not "name" in self.config.keys():
            raise Exception("No Name Set!")
        self.items = self.getItems()
        self.db = MY_DB(self.fn)
        self.undoStack = []

    def readConfig(self):
        with open(os.path.join(self.fn, "config")) as f:
            return {c.split('=')[0]:c.split('=')[1] for c in f.read().split('\n')}

    def saveConfig(self):
        with open(os.path.join(self.fn, "config"), "w") as f:
            f.write("\n".join(["{}={}".format(i, self.config[i]) for i in self.config]))

    def getName(self):
        return self.config['name']

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

    def getAvailableRankers(self):
        return AVAILABLE_RANKERS

    def rankWith(self, alg):
        return alg.findRanks(self.db.getResults())