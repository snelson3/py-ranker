from collections import defaultdict

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