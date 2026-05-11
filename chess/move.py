from dataclasses import dataclass
from chess.constants import wQ, wR, wB, wN, bQ, bR, bB, bN

FLAG_NONE = 0
FLAG_EN_PASSANT = 1
FLAG_CASTLE = 2
FLAG_PROMO_QUEEN = 4
FLAG_PROMO_ROOK = 8
FLAG_PROMO_BISHOP = 16
FLAG_PROMO_KNIGHT = 32

PROMO_PIECES_WHITE = {
    FLAG_PROMO_QUEEN: wQ,
    FLAG_PROMO_ROOK: wR,
    FLAG_PROMO_BISHOP: wB,
    FLAG_PROMO_KNIGHT: wN,
}

PROMO_PIECES_BLACK = {
    FLAG_PROMO_QUEEN: bQ,
    FLAG_PROMO_ROOK: bR,
    FLAG_PROMO_BISHOP: bB,
    FLAG_PROMO_KNIGHT: bN,
}

@dataclass(slots=True)
class MoveState:
    captured: int
    promoted: int
    old_ep: int
    old_castle: int
    old_halfmove: int
    old_fullmove: int
    from_piece: int

@dataclass(slots=True)
class Move:
    frm: int
    to: int
    flags: int = FLAG_NONE

    def __repr__(self):
        if self.is_promotion:
            promo_char = self.promo_char
            return f"{self.from_square_str}{self.to_square_str}{promo_char}"
        return f"{self.from_square_str}{self.to_square_str}"

    @property
    def from_square_str(self) -> str:
        from chess.square import square_to_string
        return square_to_string(self.frm)

    @property
    def to_square_str(self) -> str:
        from chess.square import square_to_string
        return square_to_string(self.to)

    @property
    def is_en_passant(self) -> bool:
        return bool(self.flags & FLAG_EN_PASSANT)

    @property
    def is_castle(self) -> bool:
        return bool(self.flags & FLAG_CASTLE)

    @property
    def is_promotion(self) -> bool:
        return self.flags & (FLAG_PROMO_QUEEN | FLAG_PROMO_ROOK | FLAG_PROMO_BISHOP | FLAG_PROMO_KNIGHT) != 0

    @property
    def promotion_piece(self) -> int:
        if not self.is_promotion:
            return 0
        for flag, piece in PROMO_PIECES_WHITE.items():
            if self.flags & flag:
                return piece
        return 0
    
    def get_promotion_piece(self, color: int) -> int:
        """Get promotion piece based on moving side color"""
        if not self.is_promotion:
            return 0
        promo_dict = PROMO_PIECES_WHITE if color == 0 else PROMO_PIECES_BLACK
        for flag, piece in promo_dict.items():
            if self.flags & flag:
                return piece
        return 0

    @property
    def promo_char(self) -> str:
        if not self.is_promotion:
            return ''
        flags = self.flags
        if flags & FLAG_PROMO_QUEEN:
            return 'q'
        if flags & FLAG_PROMO_ROOK:
            return 'r'
        if flags & FLAG_PROMO_BISHOP:
            return 'b'
        if flags & FLAG_PROMO_KNIGHT:
            return 'n'
        return ''

def move_from_string(s: str, from_sq: int) -> Move:
    if len(s) < 4:
        raise ValueError(f"Invalid move string: {s}")

    to_sq = (ord(s[2]) - ord('a')) + (ord(s[3]) - ord('1')) * 8

    flags = FLAG_NONE
    if len(s) == 5:
        promo = s[4].lower()
        if promo == 'q':
            flags = FLAG_PROMO_QUEEN
        elif promo == 'r':
            flags = FLAG_PROMO_ROOK
        elif promo == 'b':
            flags = FLAG_PROMO_BISHOP
        elif promo == 'n':
            flags = FLAG_PROMO_KNIGHT

    return Move(from_sq, to_sq, flags)

NULL_MOVE = Move(0, 0, FLAG_NONE)
