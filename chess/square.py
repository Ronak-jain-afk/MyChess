from chess.constants import FILE_NAMES, RANK_NAMES

def square(file: int, rank: int) -> int:
    return rank * 8 + file

def file_of(sq: int) -> int:
    return sq % 8

def rank_of(sq: int) -> int:
    return sq // 8

def is_light_square(sq: int) -> bool:
    return (file_of(sq) + rank_of(sq)) % 2 == 1

def square_from_string(s: str) -> int:
    if len(s) != 2:
        raise ValueError(f"Invalid square string: {s}")
    file = ord(s[0]) - ord('a')
    rank = ord(s[1]) - ord('1')
    if not (0 <= file <= 7 and 0 <= rank <= 7):
        raise ValueError(f"Invalid square string: {s}")
    return square(file, rank)

def square_to_string(sq: int) -> str:
    return FILE_NAMES[file_of(sq)] + RANK_NAMES[rank_of(sq)]

def mirror(sq: int) -> int:
    return square(file_of(sq), 7 - rank_of(sq))

def is_valid_square(sq: int) -> bool:
    return 0 <= sq < 64

def file_distance(a: int, b: int) -> int:
    return abs(file_of(a) - file_of(b))

def rank_distance(a: int, b: int) -> int:
    return abs(rank_of(a) - rank_of(b))