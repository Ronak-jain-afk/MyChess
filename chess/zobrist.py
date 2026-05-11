import random

ZOBRIST_PIECE = [[0] * 64 for _ in range(13)]
ZOBRIST_SIDE = 0
ZOBRIST_CASTLE = [0] * 16
ZOBRIST_EN_PASSANT = [0] * 64

def init_zobrist():
    global ZOBRIST_SIDE
    random.seed(0x123456789ABCDEF0)

    for piece in range(1, 13):
        for sq in range(64):
            ZOBRIST_PIECE[piece][sq] = random.getrandbits(64)

    ZOBRIST_SIDE = random.getrandbits(64)

    for i in range(16):
        ZOBRIST_CASTLE[i] = random.getrandbits(64)

    for sq in range(64):
        ZOBRIST_EN_PASSANT[sq] = random.getrandbits(64)

def compute_key(board: list, side: int, castle: int, ep_square: int) -> int:
    key = 0
    for sq in range(64):
        piece = board[sq]
        if piece != 0:
            key ^= ZOBRIST_PIECE[piece][sq]

    if side == 1:
        key ^= ZOBRIST_SIDE

    key ^= ZOBRIST_CASTLE[castle]

    if ep_square >= 0:
        key ^= ZOBRIST_EN_PASSANT[ep_square]

    return key

init_zobrist()