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
    from chess.constants import wP, bP
    
    key = 0
    for sq in range(64):
        piece = board[sq]
        if piece != 0:
            key ^= ZOBRIST_PIECE[piece][sq]

    if side == 1:
        key ^= ZOBRIST_SIDE

    key ^= ZOBRIST_CASTLE[castle]

    # CRITICAL: Only include en-passant if a pawn exists to capture it
    if ep_square >= 0:
        if side == 0:  # White to move, check if Black pawn exists at captured square
            captured_sq = ep_square - 8  # Captured pawn is one rank below
            if 0 <= captured_sq < 64 and board[captured_sq] == bP:
                key ^= ZOBRIST_EN_PASSANT[ep_square]
        else:  # Black to move, check if White pawn exists at captured square
            captured_sq = ep_square + 8  # Captured pawn is one rank above
            if 0 <= captured_sq < 64 and board[captured_sq] == wP:
                key ^= ZOBRIST_EN_PASSANT[ep_square]

    return key

init_zobrist()