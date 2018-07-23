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
        combs = itertools.combinations([i["name"].strip() for i in self.items], n)

        x = set(tuple(sorted(i)) for i in combs)
        if "new_only" in self.config and self.config["new_only"]:
            y = self.db.getUniqueRates()
            x = x.difference(y)
        if "pick_least_picked" in self.config and self.config["pick_least_picked"]:
            y = self.db.getLeastUsedPairs()
            x = x.difference(y)
        if len(x) < 1:
            return -1
        # TODO
        # I'm mucking with the state of an item object a bit to much, it's murky
        # Either make it always a string, or an object if there is use there
        x = [[{"name": i[0]}, {"name": i[1]}] for i in list(x)]
        random.shuffle(x)
        return x.pop()

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
        results = self.db.getResults()
        if "duplicates" in self.config and self.config["duplicates"] in ["oldest", "newest"]:
            new_results = []
            unique_pairs = {}
            ordered = results if self.config["duplicates"] == "newest" else results[::-1]
            for p in range(len(ordered)):
                pair = ordered[p]
                unique_pairs[tuple(sorted([pair["winner"],pair["loser"]]))] = (pair, p)
            for p in sorted(unique_pairs.keys(), key=lambda k: unique_pairs[k][1]):
                new_results.append(unique_pairs[p][0])
            results = new_results
        return alg.findRanks(results)