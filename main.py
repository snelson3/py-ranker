import os, random
from collections import defaultdict

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
        print("##############")
        ans = input("{}\nor\n{}\n".format(x1["name"], x2["name"]))
        if ans == "-1":
            return -1
        if ans in ["1", "2"]:
            return [x1,x2][int(ans)-1]
        print("Invalid input")
        return self.rank_2(x1, x2)

    def printRank(self, ranks):
        for rank in ranks:
            print("{}: {}".format(rank[1], rank[0]))

# Text format
# Avengers > Thor

#TODO UNDO FUNCTIONALITY
#TODO SPECIFIC NUMBER OF RATES
#TODO ONLY RATE PAIRS NOT RATED BEFORE

class DB:
    def __init__(self, name):
        self.name = name

    def read(self):
        pass

    def add1(self, winner, loser):
        pass

    def getResults(self):
        pass

class TextDB(DB):
    def __init__(self, fn):
        DB.__init__(self, fn)

    def read(self):
        if not os.path.isfile(self.name):
            print("New DB")
            return []
        with open(self.name) as f:
            return filter(lambda l: len(l) > 0,f.read().split('\n'))

    def add1(self, winner, loser):
        assert type(winner) == dict and "name" in winner
        assert type(loser) == dict and "name" in loser
        with open(self.name, "a") as f:
            f.write("{} > {}\n".format(winner["name"], loser["name"]))

    def getResults(self):
        def _parseLine(line):
            assert ">" in line
            res = line.split(">")
            return {"winner": res[0].strip(), "loser": res[1].strip()}
        return list(map(_parseLine, self.read()))

class Master:
    def __init__(self, category):
        self.category = category
        self.items = self.getItems()
        self.ui = self.makeUI(CMD_UI)
        self.db = self.makeDB(TextDB)

    def rate(self):
        while 1:
            i = self.getRandomItems()
            x1 = i[0]
            x2 = i[1]
            winner = self.ui.rank_2(x1, x2)
            if winner == -1:
                break # End the rate session
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

class Ranker:
    # Eliminate dupes option
    def __init__(self):
        pass

    def rank(self, pairs):
        d = self.findRanks(pairs)
        return sorted(map(lambda i: (i, d[i]), d.keys()), key=lambda i: i[1] * -1)

    def findRanks(self, pairs):
        pass

class SimpleRanker(Ranker):
    # Very simple 1 point every time something wins
    def findRanks(self, pairs):
        d = defaultdict(int)
        for pair in pairs:
            d[pair["winner"]] += 1
            d[pair["loser"]] += 0
        return d

class TSRanker(Ranker):
    # Use the True skill library to rank pairs
    def findRanks(self, pairs):
        from trueskill import TrueSkill, Rating
        env = TrueSkill(draw_probability=0.0)
        d = defaultdict(Rating)
        for p in pairs:
            d[p["winner"]], d[p["loser"]] = env.rate_1vs1(d[p["winner"]], d[p["loser"]])
        for i in d:
            well = d[i]
            d[i] = round(env.expose(d[i]), 2)
        return d

### This needs to change a bit
import sys
assert len(sys.argv) > 1
master = Master(sys.argv[1])
if len(sys.argv) > 2:
    if sys.argv[2] == "rank":
        ranker = SimpleRanker()
        if len(sys.argv) > 3 and sys.argv[3] == "ts":
            ranker = TSRanker()
        master.ui.printRank(ranker.rank(master.db.getResults()))
else:
    master.rate()