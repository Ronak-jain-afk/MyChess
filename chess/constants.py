from enum import IntEnum
from typing import Optional

class Color(IntEnum):
    WHITE = 0
    BLACK = 1

class PieceType(IntEnum):
    EMPTY = 0
    PAWN = 1
    KNIGHT = 2
    BISHOP = 3
    ROOK = 4
    QUEEN = 5
    KING = 6

EMPTY = 0
wP, wN, wB, wR, wQ, wK = 1, 2, 3, 4, 5, 6
bP, bN, bB, bR, bQ, bK = 7, 8, 9, 10, 11, 12

PIECE_CHARS = {
    'P': wP, 'N': wN, 'B': wB, 'R': wR, 'Q': wQ, 'K': wK,
    'p': bP, 'n': bN, 'b': bB, 'r': bR, 'q': bQ, 'k': bK
}

PIECE_TO_CHAR = {v: k for k, v in PIECE_CHARS.items()}

MATERIAL_VALUES = {
    PieceType.PAWN: 100,
    PieceType.KNIGHT: 320,
    PieceType.BISHOP: 330,
    PieceType.ROOK: 500,
    PieceType.QUEEN: 900,
    PieceType.KING: 20000,
}

def piece_color(piece: int) -> Optional[Color]:
    if piece == EMPTY:
        return None
    return Color.WHITE if piece <= 6 else Color.BLACK

def piece_type(piece: int) -> PieceType:
    if piece == EMPTY:
        return PieceType.EMPTY
    return PieceType(piece if piece <= 6 else piece - 6)

def is_piece(piece: int) -> bool:
    return piece != EMPTY

FILE_NAMES = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
RANK_NAMES = ['1', '2', '3', '4', '5', '6', '7', '8']

KNIGHT_OFFSETS = [
    -17, -15, -10, -6, 6, 10, 15, 17
]

KING_OFFSETS = [
    -9, -8, -7, -1, 1, 7, 8, 9
]

SLIDING_OFFSETS = {
    PieceType.BISHOP: [-9, -7, 7, 9],
    PieceType.ROOK: [-8, -1, 1, 8],
    PieceType.QUEEN: [-9, -8, -7, -1, 1, 7, 8, 9],
}

CASTLE_NONE = 0
CASTLE_WK = 1
CASTLE_WQ = 2
CASTLE_BK = 4
CASTLE_BQ = 8