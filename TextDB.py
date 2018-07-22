from DB import DB
import os

class TextDB(DB):
    def __init__(self, fn):
        DB.__init__(self, os.path.join(fn,"results"))

    def read(self):
        if not os.path.isfile(self.name):
            print("New DB")
            return []
        with open(self.name) as f:
            return filter(lambda l: len(l) > 0,f.read().split('\n'))

    def remove1(self):
        # This is inefficient
        with open(self.name, "r") as f:
            results = f.read().strip().split('\n')
        assert len(results) > 0
        removed = results.pop()
        with open(self.name, "w") as f:
            f.write("\n".join(results))
            f.write("\n")
        return [{"name":x.strip()} for x in removed.split(">")]

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

    def getUniqueRates(self):
        rates = self.getResults()
        return set(map(lambda r: tuple(sorted([r["winner"], r["loser"]])), rates))
