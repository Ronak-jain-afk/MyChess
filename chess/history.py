class PositionHistory:
    def __init__(self):
        self.keys = []
        self.reversible = []
        self.moves = []  # Track the moves made
        self.last_from_sq = -1
        self.last_to_sq = -1

    def push(self, key: int, reversible: bool, from_sq: int = -1, to_sq: int = -1):
        self.keys.append(key)
        self.reversible.append(reversible)
        self.moves.append((from_sq, to_sq))
        self.last_from_sq = from_sq
        self.last_to_sq = to_sq

    def pop(self):
        """Remove the last position from history."""
        if self.keys:
            self.keys.pop()
            self.reversible.pop()
            self.moves.pop()
            if self.keys:
                # Update last_from_sq, last_to_sq to previous move
                self.last_from_sq, self.last_to_sq = self.moves[-1]
            else:
                self.last_from_sq = -1
                self.last_to_sq = -1

    def is_threefold(self, key: int) -> bool:
        reversible_keys = [k for k, r in zip(self.keys, self.reversible) if r]
        count = sum(1 for k in reversible_keys if k == key)
        return count >= 3

    def clear(self):
        self.keys.clear()
        self.reversible.clear()
        self.moves.clear()
        self.last_from_sq = -1
        self.last_to_sq = -1
