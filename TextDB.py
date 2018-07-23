from DB import DB
import os, itertools

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
        if len(results) <= 0:
            raise Exception("No Results to remove!")
        removed = results.pop()
        with open(self.name, "w") as f:
            f.write("\n".join(results))
            f.write("\n")
        return [{"name":x.strip()} for x in removed.split(">")]

    def add1(self, winner, loser):
        if type(winner) is not dict or "name" not in winner \
            or type(loser) is not dict or "name" not in loser:
                raise Exception("Bad winner/loser!")
        with open(self.name, "a") as f:
            f.write("{} > {}\n".format(winner["name"], loser["name"]))

    def getResults(self):
        def _parseLine(line):
            if ">" not in line:
                raise Exception("Malformed line in results: {}".format(line))
            res = line.split(">")
            return {"winner": res[0].strip(), "loser": res[1].strip()}
        return list(map(_parseLine, self.read()))

    def getUniqueRates(self):
        rates = self.getResults()
        return set(map(lambda r: tuple(sorted([r["winner"], r["loser"]])), rates))

    def getLeastUsedPairs(self):
        rates = self.getResults()
        nrates = {}
        for r in list(map(lambda r: tuple(sorted([r["winner"], r["loser"]])), rates)):
            for x in r:
                if x in nrates:
                    nrates[x] += 1
                else:
                    nrates[x] = 1
        min_rate = 99999999999999
        second_min_rate = 9999999999
        for r in nrates:
            if nrates[r] < min_rate:
                if min_rate < second_min_rate:
                    second_min_rate = min_rate
                min_rate = nrates[r]
            if nrates[r] > min_rate and nrates[r] < second_min_rate:
                second_min_rate = nrates[r]
        print(nrates)
        y = [r for r in nrates if nrates[r] in [min_rate, second_min_rate]]
        return set(itertools.combinations(y, 2))