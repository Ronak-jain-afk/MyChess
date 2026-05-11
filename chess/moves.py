from chess.constants import (
    EMPTY, wP, wN, wB, wR, wQ, wK, bP, bN, bB, bR, bQ, bK,
    Color, PieceType, KNIGHT_OFFSETS, KING_OFFSETS, SLIDING_OFFSETS,
    CASTLE_WK, CASTLE_WQ, CASTLE_BK, CASTLE_BQ
)
from chess.square import file_of, rank_of, square, is_valid_square, file_distance
from chess.move import Move, FLAG_NONE, FLAG_EN_PASSANT, FLAG_CASTLE

KNIGHT_ATTACKS = [0] * 64
KING_ATTACKS = [0] * 64
RAYS = [[0] * 8 for _ in range(64)]

def index_bitboard(bb):
    return (bb & -bb).bit_length() - 1

def square_to_bitboard(sq):
    return 1 << sq

def init_tables():
    for sq in range(64):
        bb = 0
        for offset in KNIGHT_OFFSETS:
            nsq = sq + offset
            if is_valid_square(nsq) and file_distance(sq, nsq) <= 2:
                bb |= 1 << nsq
        KNIGHT_ATTACKS[sq] = bb

    for sq in range(64):
        bb = 0
        for offset in KING_OFFSETS:
            nsq = sq + offset
            if is_valid_square(nsq) and file_distance(sq, nsq) <= 1:
                bb |= 1 << nsq
        KING_ATTACKS[sq] = bb

    for sq in range(64):
        for d in range(8):
            ray = 0
            f = file_of(sq)
            r = rank_of(sq)

            if d == 0:   deltas = (0, 1)
            elif d == 1: deltas = (0, -1)
            elif d == 2: deltas = (1, 0)
            elif d == 3: deltas = (-1, 0)
            elif d == 4: deltas = (1, 1)
            elif d == 5: deltas = (1, -1)
            elif d == 6: deltas = (-1, 1)
            elif d == 7: deltas = (-1, -1)

            df, dr = deltas
            cf, cr = f + df, r + dr
            while 0 <= cf <= 7 and 0 <= cr <= 7:
                ray |= 1 << (cr * 8 + cf)
                cf += df
                cr += dr

            RAYS[sq][d] = ray

def is_attacked_by(pos, sq, by_color):
    enemy_pawn = wP if by_color == Color.WHITE else bP
    enemy_knight = wN if by_color == Color.WHITE else bN
    enemy_bishop = wB if by_color == Color.WHITE else bB
    enemy_rook = wR if by_color == Color.WHITE else bR
    enemy_queen = wQ if by_color == Color.WHITE else bQ
    enemy_king = wK if by_color == Color.WHITE else bK

    # Pawn attacks
    if by_color == Color.WHITE:
        pawn_dr = -1
    else:
        pawn_dr = 1

    for df in [-1, 1]:
        f, r = file_of(sq) + df, rank_of(sq) + pawn_dr
        if 0 <= f <= 7 and 0 <= r <= 7:
            if pos.board[r * 8 + f] == enemy_pawn:
                return True

    # En passant attack detection
    # En passant square is where opponent's pawn can capture
    # We check if enemy pawn can attack the given square via en passant
    ep_sq = pos.ep_square[0]
    if ep_sq >= 0:
        ep_file = file_of(ep_sq)
        ep_rank = rank_of(ep_sq)
        sq_file = file_of(sq)
        sq_rank = rank_of(sq)
        
        if by_color == Color.WHITE:
            # Black pawn attacks en passant by moving to ep_sq
            # Black pawns are on the 4th rank (rank 3) when en passant is available
            # They attack diagonally downward (toward rank 0)
            # ep_sq is the target square for en passant capture
            # If white king is on ep_sq, check if black pawn on rank above can capture
            if sq_rank == ep_rank:
                if sq_file == ep_file - 1 or sq_file == ep_file + 1:
                    pawn_sq = (ep_rank + 1) * 8 + sq_file
                    if 0 <= pawn_sq < 64 and pos.board[pawn_sq] == bP:
                        return True
        else:
            # White pawn attacks en passant by moving to ep_sq
            # White pawns are on the 5th rank (rank 4) when en passant is available
            # They attack diagonally upward (toward rank 7)
            # ep_sq is the target square for en passant capture
            # If black king is on ep_sq, check if white pawn on rank below can capture
            if sq_rank == ep_rank:
                if sq_file == ep_file - 1 or sq_file == ep_file + 1:
                    pawn_sq = (ep_rank - 1) * 8 + sq_file
                    if 0 <= pawn_sq < 64 and pos.board[pawn_sq] == wP:
                        return True

    # Knight attacks
    bb = KNIGHT_ATTACKS[sq]
    while bb:
        tsq = index_bitboard(bb)
        bb &= bb - 1
        if pos.board[tsq] == enemy_knight:
            return True

    # King attacks
    bb = KING_ATTACKS[sq]
    while bb:
        tsq = index_bitboard(bb)
        bb &= bb - 1
        if pos.board[tsq] == enemy_king:
            return True

    for d in [4, 5, 6, 7]:
        ray = RAYS[sq][d]
        bb = ray
        while bb:
            tsq = index_bitboard(bb)
            bb &= bb - 1
            piece = pos.board[tsq]
            if piece in [enemy_bishop, enemy_queen]:
                return True
            elif piece != EMPTY:
                break

    for d in [0, 1, 2, 3]:
        ray = RAYS[sq][d]
        bb = ray
        while bb:
            tsq = index_bitboard(bb)
            bb &= bb - 1
            piece = pos.board[tsq]
            if piece in [enemy_rook, enemy_queen]:
                return True
            elif piece != EMPTY:
                break

    return False

def find_king(pos, color):
    king = wK if color == Color.WHITE else bK
    for sq in range(64):
        if pos.board[sq] == king:
            return sq
    return -1

def is_in_check(pos, color):
    king_sq = find_king(pos, color)
    if king_sq == -1:
        return False
    enemy_color = Color.BLACK if color == Color.WHITE else Color.WHITE
    return is_attacked_by(pos, king_sq, enemy_color)

def generate_pawn_moves(pos, color):
    moves = []
    direction = 1 if color == Color.WHITE else -1  # white moves up (+), black moves down (-)
    start_rank = 1 if color == Color.WHITE else 6  # rank 2 (white) or rank 7 (black)
    promo_rank = 7 if color == Color.WHITE else 0  # rank 8 (white) or rank 1 (black)
    ep_rank = 3 if color == Color.WHITE else 4

    for sq in range(64):
        piece = pos.board[sq]
        if (color == Color.WHITE and piece == wP) or (color == Color.BLACK and piece == bP):
            f, r = file_of(sq), rank_of(sq)

            nsq = sq + direction * 8
            if 0 <= nsq < 64 and pos.board[nsq] == EMPTY:
                if rank_of(nsq) == promo_rank:
                    for flag, promo in [(4, wQ if color == Color.WHITE else bQ),
                                        (8, wR if color == Color.WHITE else bR),
                                        (16, wB if color == Color.WHITE else bB),
                                        (32, wN if color == Color.WHITE else bN)]:
                        moves.append(Move(sq, nsq, flag))
                else:
                    moves.append(Move(sq, nsq))

                if r == start_rank:
                    dsnq = nsq + direction * 8
                    if 0 <= dsnq < 64 and pos.board[dsnq] == EMPTY:
                        moves.append(Move(sq, dsnq))

            for df in [-1, 1]:
                f2, r2 = f + df, r + direction
                if 0 <= f2 <= 7 and 0 <= r2 <= 7:
                    cap_sq = r2 * 8 + f2
                    target = pos.board[cap_sq]

                    if target != EMPTY:
                        if (color == Color.WHITE and target > 6) or (color == Color.BLACK and target <= 6 and target != 0):
                            if rank_of(cap_sq) == promo_rank:
                                for flag, promo in [(4, wQ if color == Color.WHITE else bQ),
                                                    (8, wR if color == Color.WHITE else bR),
                                                    (16, wB if color == Color.WHITE else bB),
                                                    (32, wN if color == Color.WHITE else bN)]:
                                    moves.append(Move(sq, cap_sq, flag))
                            else:
                                moves.append(Move(sq, cap_sq))

                    ep_sq = pos.ep_square[0]
                    if cap_sq == ep_sq:
                        moves.append(Move(sq, cap_sq, FLAG_EN_PASSANT))

    return moves

def generate_knight_moves(pos, color):
    moves = []
    piece = wN if color == Color.WHITE else bN

    for sq in range(64):
        if pos.board[sq] == piece:
            for offset in KNIGHT_OFFSETS:
                nsq = sq + offset
                if is_valid_square(nsq):
                    f1, r1 = file_of(sq), rank_of(sq)
                    f2, r2 = file_of(nsq), rank_of(nsq)
                    if (abs(f1 - f2) == 1 and abs(r1 - r2) == 2) or (abs(f1 - f2) == 2 and abs(r1 - r2) == 1):
                        target = pos.board[nsq]
                        if target == EMPTY:
                            moves.append(Move(sq, nsq))
                        elif (color == Color.WHITE and target > 6) or (color == Color.BLACK and target <= 6 and target != 0):
                            moves.append(Move(sq, nsq))

    return moves

def generate_sliding_moves(pos, piece_type, color):
    moves = []

    if piece_type == PieceType.BISHOP:
        piece = wB if color == Color.WHITE else bB
        directions = [4, 5, 6, 7]
    elif piece_type == PieceType.ROOK:
        piece = wR if color == Color.WHITE else bR
        directions = [0, 1, 2, 3]
    else:
        piece = wQ if color == Color.WHITE else bQ
        directions = [0, 1, 2, 3, 4, 5, 6, 7]

    for sq in range(64):
        if pos.board[sq] == piece:
            f, r = file_of(sq), rank_of(sq)
            for d in directions:
                if d == 0: df, dr = 0, 1
                elif d == 1: df, dr = 0, -1
                elif d == 2: df, dr = 1, 0
                elif d == 3: df, dr = -1, 0
                elif d == 4: df, dr = 1, 1
                elif d == 5: df, dr = 1, -1
                elif d == 6: df, dr = -1, 1
                elif d == 7: df, dr = -1, -1

                cf, cr = f + df, r + dr
                while 0 <= cf <= 7 and 0 <= cr <= 7:
                    tsq = cr * 8 + cf
                    target = pos.board[tsq]
                    if target == EMPTY:
                        moves.append(Move(sq, tsq))
                    else:
                        target_is_enemy = (color == Color.WHITE and target > 6) or (color == Color.BLACK and target <= 6 and target != 0)
                        if target_is_enemy:
                            moves.append(Move(sq, tsq))
                        break
                    cf += df
                    cr += dr

    return moves

def generate_king_moves(pos, color):
    moves = []
    piece = wK if color == Color.WHITE else bK

    for sq in range(64):
        if pos.board[sq] == piece:
            for offset in KING_OFFSETS:
                nsq = sq + offset
                if is_valid_square(nsq) and file_distance(sq, nsq) <= 1:
                    target = pos.board[nsq]
                    if target == EMPTY:
                        moves.append(Move(sq, nsq))
                    elif (color == Color.WHITE and target > 6) or (color == Color.BLACK and target <= 6 and target != 0):
                        moves.append(Move(sq, nsq))

            if color == Color.WHITE:
                if pos.castle_rights[0] & CASTLE_WK:
                    if pos.board[5] == EMPTY and pos.board[6] == EMPTY:
                        if not is_in_check(pos, Color.WHITE):
                            if not is_attacked_by(pos, 5, Color.BLACK) and not is_attacked_by(pos, 6, Color.BLACK):
                                moves.append(Move(4, 6, FLAG_CASTLE))
                if pos.castle_rights[0] & CASTLE_WQ:
                    if pos.board[1] == EMPTY and pos.board[2] == EMPTY and pos.board[3] == EMPTY:
                        if not is_in_check(pos, Color.WHITE):
                            if not is_attacked_by(pos, 2, Color.BLACK) and not is_attacked_by(pos, 3, Color.BLACK):
                                moves.append(Move(4, 2, FLAG_CASTLE))
            else:
                if pos.castle_rights[0] & CASTLE_BK:
                    if pos.board[61] == EMPTY and pos.board[62] == EMPTY:
                        if not is_in_check(pos, Color.BLACK):
                            if not is_attacked_by(pos, 61, Color.WHITE) and not is_attacked_by(pos, 62, Color.WHITE):
                                moves.append(Move(60, 62, FLAG_CASTLE))
                if pos.castle_rights[0] & CASTLE_BQ:
                    if pos.board[57] == EMPTY and pos.board[58] == EMPTY and pos.board[59] == EMPTY:
                        if not is_in_check(pos, Color.BLACK):
                            if not is_attacked_by(pos, 58, Color.WHITE) and not is_attacked_by(pos, 59, Color.WHITE):
                                moves.append(Move(60, 58, FLAG_CASTLE))

    return moves

def generate_pseudo_legal_moves(pos):
    moves = []
    color = Color.WHITE if pos.side_to_move[0] == 0 else Color.BLACK

    moves.extend(generate_pawn_moves(pos, color))
    moves.extend(generate_knight_moves(pos, color))
    moves.extend(generate_sliding_moves(pos, PieceType.BISHOP, color))
    moves.extend(generate_sliding_moves(pos, PieceType.ROOK, color))
    moves.extend(generate_sliding_moves(pos, PieceType.QUEEN, color))
    moves.extend(generate_king_moves(pos, color))

    return moves

init_tables()