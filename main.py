import os, random
from collections import defaultdict

# TODO ONLY RATE PAIRS NOT RATED BEFORE
# TODO mode of choosing where x1 is always a thing with the minimum number of rates

# When it's working need to figure out where to deal with bad data

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