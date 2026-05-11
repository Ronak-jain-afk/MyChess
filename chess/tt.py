class TTEntry:
    __slots__ = ['key', 'depth', 'score', 'flag', 'move']

    def __init__(self, key, depth, score, flag, move):
        self.key = key
        self.depth = depth
        self.score = score
        self.flag = flag
        self.move = move


EXACT = 0
LOWER = 1
UPPER = 2


class TranspositionTable:
    def __init__(self, size=1000000):
        self.size = size
        self.table = [None] * size
        self.hits = 0
        self.misses = 0

    def _index(self, key):
        return key % self.size

    def probe(self, key, depth, alpha, beta):
        idx = self._index(key)
        entry = self.table[idx]

        if entry and entry.key == key:
            if entry.depth >= depth:
                self.hits += 1
                if entry.flag == EXACT:
                    return entry.score, entry.move
                elif entry.flag == LOWER and entry.score >= beta:
                    return entry.score, entry.move
                elif entry.flag == UPPER and entry.score <= alpha:
                    return entry.score, entry.move
            return None, entry.move

        self.misses += 1
        return None, None

    def store(self, key, score, depth, flag, move):
        idx = self._index(key)
        entry = self.table[idx]

        if entry is None or (entry.key == key and depth >= entry.depth):
            self.table[idx] = TTEntry(key, depth, score, flag, move)

    def clear(self):
        self.table = [None] * self.size
        self.hits = 0
        self.misses = 0

    def statistics(self):
        total = self.hits + self.misses
        hit_rate = (self.hits / total * 100) if total > 0 else 0
        return f"TT: {self.hits} hits, {self.misses} misses, {hit_rate:.1f}%"


tt = TranspositionTable()