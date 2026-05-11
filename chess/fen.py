from typing import List
from chess.constants import PIECE_CHARS, PIECE_TO_CHAR, CASTLE_WK, CASTLE_WQ, CASTLE_BK, CASTLE_BQ, EMPTY

def validate_fen(fen: str):
    """Validate FEN string format and values."""
    parts = fen.split()
    
    if len(parts) != 6:
        raise ValueError(f"Invalid FEN: expected 6 space-separated parts, got {len(parts)}")
    
    placement, side, castle, ep, halfmove_str, fullmove_str = parts
    
    # Validate placement (piece positions)
    ranks = placement.split('/')
    if len(ranks) != 8:
        raise ValueError(f"Invalid FEN: expected 8 ranks, got {len(ranks)}")
    
    for rank_idx, rank in enumerate(ranks):
        file_count = 0
        for char in rank:
            if char.isdigit():
                file_count += int(char)
                if file_count > 8:
                    raise ValueError(f"Invalid FEN: rank {8-rank_idx} exceeds 8 files")
            elif char in 'pnbrqkPNBRQK':
                file_count += 1
            else:
                raise ValueError(f"Invalid FEN: unknown piece '{char}' in rank {8-rank_idx}")
        if file_count != 8:
            raise ValueError(f"Invalid FEN: rank {8-rank_idx} has {file_count} files, expected 8")
    
    # Validate side to move
    if side not in ['w', 'b']:
        raise ValueError(f"Invalid FEN: side to move must be 'w' or 'b', got '{side}'")
    
    # Validate castling rights
    if castle != '-':
        for char in castle:
            if char not in 'KQkq':
                raise ValueError(f"Invalid FEN: invalid castling right '{char}'")
    
    # Validate en passant square
    if ep != '-':
        if len(ep) != 2:
            raise ValueError(f"Invalid FEN: en passant square must be 2 characters or '-', got '{ep}'")
        file_char, rank_char = ep[0], ep[1]
        if file_char not in 'abcdefgh':
            raise ValueError(f"Invalid FEN: en passant file must be a-h, got '{file_char}'")
        if rank_char not in '36':
            raise ValueError(f"Invalid FEN: en passant rank must be 3 or 6, got '{rank_char}'")
        # Validate rank matches side to move: white (w) can only have rank 6, black (b) can only have rank 3
        if (side == 'w' and rank_char != '6') or (side == 'b' and rank_char != '3'):
            raise ValueError(f"Invalid FEN: en passant rank {rank_char} does not match side to move '{side}'")
    
    # Validate halfmove clock
    try:
        halfmove_val = int(halfmove_str)
        if halfmove_val < 0:
            raise ValueError(f"Invalid FEN: halfmove clock must be non-negative, got {halfmove_val}")
    except ValueError as e:
        raise ValueError(f"Invalid FEN: halfmove clock must be an integer, got '{halfmove_str}'")
    
    # Validate fullmove number
    try:
        fullmove_val = int(fullmove_str)
        if fullmove_val < 1:
            raise ValueError(f"Invalid FEN: fullmove number must be >= 1, got {fullmove_val}")
    except ValueError as e:
        raise ValueError(f"Invalid FEN: fullmove number must be an integer, got '{fullmove_str}'")

def set_fen(fen: str, board: list, side_to_move: List[int], castle: List[int], ep_square: List[int], halfmove: List[int], fullmove: List[int]):
    parts = fen.split()
    
    # Validate FEN before processing
    validate_fen(fen)

    placement = parts[0]
    board_array = [EMPTY] * 64

    rank = 7
    file = 0
    for char in placement:
        if char == '/':
            rank -= 1
            file = 0
        elif char.isdigit():
            file += int(char)
        else:
            sq = rank * 8 + file
            board_array[sq] = PIECE_CHARS[char]
            file += 1

    for i in range(64):
        board[i] = board_array[i]

    side_to_move[0] = 0 if parts[1] == 'w' else 1

    castle_rights = 0
    for char in parts[2]:
        if char == 'K':
            castle_rights |= CASTLE_WK
        elif char == 'Q':
            castle_rights |= CASTLE_WQ
        elif char == 'k':
            castle_rights |= CASTLE_BK
        elif char == 'q':
            castle_rights |= CASTLE_BQ
    castle[0] = castle_rights

    if parts[3] == '-':
        ep_square[0] = -1
    else:
        file = ord(parts[3][0]) - ord('a')
        rank = ord(parts[3][1]) - ord('1')
        ep_square[0] = rank * 8 + file

    halfmove[0] = int(parts[4])
    fullmove[0] = int(parts[5])

def get_fen(board: list, side_to_move: List[int], castle: List[int], ep_square: List[int], halfmove: List[int], fullmove: List[int]) -> str:
    placement = []
    for rank in range(7, -1, -1):
        empty = 0
        for file in range(8):
            sq = rank * 8 + file
            piece = board[sq]
            if piece == EMPTY:
                empty += 1
            else:
                if empty > 0:
                    placement.append(str(empty))
                    empty = 0
                placement.append(PIECE_TO_CHAR.get(piece, '.'))
        if empty > 0:
            placement.append(str(empty))
        if rank > 0:
            placement.append('/')

    side = 'w' if side_to_move[0] == 0 else 'b'

    castling = ''
    if castle[0] & CASTLE_WK:
        castling += 'K'
    if castle[0] & CASTLE_WQ:
        castling += 'Q'
    if castle[0] & CASTLE_BK:
        castling += 'k'
    if castle[0] & CASTLE_BQ:
        castling += 'q'
    if castling == '':
        castling = '-'

    ep = '-'
    if ep_square[0] >= 0:
        file = ep_square[0] % 8
        rank = (ep_square[0] // 8) + 1
        ep = chr(ord('a') + file) + str(rank)

    return ' '.join([
        ''.join(placement),
        side,
        castling,
        ep,
        str(halfmove[0]),
        str(fullmove[0])
    ])

STARTING_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
