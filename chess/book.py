import os
import random
from chess.position import Position
from chess.move import Move

class OpeningBook:
    def __init__(self, filename=None):
        self.entries = {}
        self.loaded = False

        if filename and os.path.exists(filename):
            self.load(filename)

    def load(self, filename):
        """Load a simple text-based opening book."""
        try:
            with open(filename, 'r') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue

                    parts = line.split()
                    if len(parts) < 2:
                        continue

                    placement = parts[0]
                    moves = parts[1:]

                    valid_variants = [
                        ('w', 'KQkq', '-'), ('w', 'KQkq', '6'),
                        ('b', 'KQkq', '-'), ('b', 'KQkq', '3'),
                        ('w', '-', '-'), ('b', '-', '-'),
                    ]

                    for side, castle, ep in valid_variants:
                        for half in ['0']:
                            for full in ['1']:
                                try:
                                    test_fen = f"{placement} {side} {castle} {ep} {half} {full}"
                                    pos = Position(test_fen)
                                    key = pos.key

                                    if key not in self.entries:
                                        self.entries[key] = []
                                    self.entries[key].extend(moves)
                                except (ValueError, IndexError):
                                    pass

            self.loaded = True
            print(f"Opening book loaded: {len(self.entries)} positions")
        except Exception as e:
            print(f"Failed to load opening book: {e}")
            self.loaded = False

    def get_move(self, pos: Position) -> Move:
        """Get a random move from the book for current position."""
        if not self.loaded:
            return None

        key = pos.key
        if key not in self.entries:
            return None

        move_strs = self.entries[key]
        if not move_strs:
            return None

        move_str = random.choice(move_strs)
        return self.move_from_uci(pos, move_str)

    def move_from_uci(self, pos: Position, uci_str: str) -> Move:
        """Convert UCI string to Move object."""
        if len(uci_str) < 4:
            return None

        from chess.square import square_from_string
        from chess.move import Move, FLAG_PROMO_QUEEN, FLAG_PROMO_ROOK, FLAG_PROMO_BISHOP, FLAG_PROMO_KNIGHT

        try:
            from_sq = square_from_string(uci_str[:2])
            to_sq = square_from_string(uci_str[2:4])
        except ValueError:
            return None

        flags = 0
        if len(uci_str) >= 5:
            promo = uci_str[4].lower()
            if promo == 'q':
                flags = FLAG_PROMO_QUEEN
            elif promo == 'r':
                flags = FLAG_PROMO_ROOK
            elif promo == 'b':
                flags = FLAG_PROMO_BISHOP
            elif promo == 'n':
                flags = FLAG_PROMO_KNIGHT

        return Move(from_sq, to_sq, flags)

    def is_empty(self):
        return not self.loaded or len(self.entries) == 0


book = OpeningBook()


def load_book(filename):
    global book
    book = OpeningBook(filename)


_book_instance = None

def get_book_move(pos: Position) -> Move:
    global _book_instance
    if _book_instance is None:
        _book_instance = OpeningBook()
        _book_instance.load('book.txt')
    return _book_instance.get_move(pos)