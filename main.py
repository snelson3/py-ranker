import os, random
from collections import defaultdict

# Try to implement these without holding anything in memory, even if it's slow with file io
# THe list of items is kept in memory right now, but that's fine
#TODO ONLY RATE PAIRS NOT RATED BEFORE
#TODO mode of choosing where x1 is always a thing with the minimum number of rates

class Master:
    def __init__(self, category):
        self.category = category
        self.items = self.getItems()
        self.ui = self.makeUI(CMD_KIVY)
        self.db = self.makeDB(TextDB)
        self.undostack = [] # Maybe this should be part of the DB

    def rate1(self, pair):
        x1 = pair[0]
        x2 = pair[1]
        winner = self.ui.rank_2(x1, x2)
        if winner == "undo":
            self.undostack.append(self.db.remove1())
        elif winner == -1:
            return -1
        else:
            loser = x1 if winner is x2 else x2
            self.db.add1(winner, loser)
            return 1

    def rate(self, n=99999):
        for _ in range(n):
            if len(self.undostack) > 0:
                while len(self.undostack) > 0:
                    items = self.undostack[-1]
                    r = self.rate1(items)
                    if r == -1:
                        break
                    if r == 1:
                        self.undostack.pop() # Pair was successfully re-evaluated
            else:
                r = self.rate1(self.getRandomItems())
            if r == -1:
                break # End the rate session

    def makeUI(self, cls):
        return cls()

    def getRandomItems(self, n=2):
        # Inefficient
        x = list(self.items)
        random.shuffle(x)
        return [x.pop(0) for i in range(n)]


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
        master.rate(n=int(sys.argv[2]))
else:
    master.rate()