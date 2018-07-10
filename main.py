import os, random

class UI:
    def __init__(self):
        # I don't think the UI needs any state
        pass
    
    def rank_2(self, x1, x2):
        # Given two objects, return the better one
        pass

class CMD_UI(UI):
    def __init__(self):
        UI.__init__(self)

    def rank_2(self, x1, x2):
        print("##############")
        print("#enter 1 or 2#")
        ans = input("{}\nor\n{}\n".format(x1["name"], x2["name"]))
        if ans in ["1", "2"]:
            return [x1,x2][int(ans)-1]
        print("Invalid input")
        return self.rank_2(x1, x2)


# Text format
# Avengers > Thor

class DB:
    def __init__(self, name):
        self.name = name

    def read(self):
        pass

    def add1(self, winner, loser):
        pass

class TextDB(DB):
    def __init__(self, fn):
        DB.__init__(self, fn)

    def read(self):
        if not os.path.isfile(self.name):
            print("New DB")
            return []
        with open(self.name) as f:
            return f.read().split('\n')

    def add1(self, winner, loser):
        assert type(winner) == dict and "name" in winner
        assert type(loser) == dict and "name" in loser
        with open(self.name, "a") as f:
            f.write("{} > {}\n".format(winner["name"], loser["name"]))

class Master:
    def __init__(self, category):
        self.category = category
        self.items = self.getItems()
        self.ui = self.makeUI(CMD_UI)
        self.db = self.makeDB(TextDB)
        self.results = self.db.read()
        while 1:
            i = self.getRandomItems()
            x1 = i[0]
            x2 = i[1]
            winner = self.ui.rank_2(x1,x2)
            loser = x1 if winner is x2 else x2
            self.db.add1(winner, loser)

    def readCategory(self):
        assert os.path.isdir(os.path.join("sourceData", self.category))
        assert os.path.isfile(os.path.join("sourceData", self.category, "list"))
        return open(os.path.join("sourceData", self.category, "list")).read().split("\n")

    def getItems(self):
        l = self.readCategory()
        return list(map(lambda i: {"name": i}, l))

    def makeUI(self, cls):
        return cls()

    def makeDB(self, cls):
        return cls(os.path.join("sourceData", self.category, "results"))

    def getRandomItems(self, n=2):
        # Inefficient
        x = list(self.items)
        random.shuffle(x)
        return [x.pop(0) for i in range(n)]

import sys
assert len(sys.argv) > 1
Master(sys.argv[1])
