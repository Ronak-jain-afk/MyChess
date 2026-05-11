import time
from chess.position import Position
from chess.move import Move
from chess import evaluate
from chess.constants import Color, wP, wN, wB, wR, wQ, wK, bP, bN, bB, bR, bQ, bK
import chess.tt as tt_module
from chess.tt import EXACT, LOWER, UPPER
import chess.book as book_module

tt = tt_module.tt

INF = 100000000
CHECKMATE_THRESHOLD = 90000
USE_BOOK = True

PIECE_VALUES = {
    0: 0,
    wP: 1, wN: 3, wB: 3, wR: 5, wQ: 9, wK: 100,
    bP: 1, bN: 3, bB: 3, bR: 5, bQ: 9, bK: 100,
}

def is_capture(move, pos):
    if move.is_en_passant:
        return True
    target = pos.board[move.to]
    return target != 0

def is_checkmate(score):
    return abs(score) > CHECKMATE_THRESHOLD

def mvv_lva(move, pos):
    victim = pos.board[move.to] if move.to is not None else 0

    if move.is_en_passant:
        victim = bP if pos.side_to_move[0] == 0 else wP
        victim_value = 1
    else:
        victim_value = PIECE_VALUES.get(victim, 0)

    attacker = pos.board[move.frm]
    attacker_cost = PIECE_VALUES.get(attacker, 0)

    return victim_value * 10 - attacker_cost

def order_moves(moves, pos, tt_move=None):
    scored = []
    for move in moves:
        score = 0
        if tt_move and move.frm == tt_move.frm and move.to == tt_move.to:
            score = 100000
        elif is_capture(move, pos):
            score = mvv_lva(move, pos)
        scored.append((score, move))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [m for _, m in scored]

def quiescence(pos: Position, alpha: int, beta: int) -> int:
    stand_pat = evaluate.evaluate(pos)

    if stand_pat >= beta:
        return beta
    if stand_pat > alpha:
        alpha = stand_pat

    captures = []
    for move in pos.generate_legal_moves():
        if is_capture(move, pos):
            captures.append(move)

    captures = order_moves(captures, pos)

    for move in captures:
        state = pos.make_move(move)
        score = -quiescence(pos, -beta, -alpha)
        pos.unmake_move(state, move)

        if score > alpha:
            alpha = score
        if alpha >= beta:
            break

    return alpha

def negamax(pos: Position, depth: int, alpha: int, beta: int, tt_move=None) -> int:
    if depth == 0:
        return quiescence(pos, alpha, beta)

    key = pos.key

    tt_score, tt_move_in_node = tt.probe(key, depth, alpha, beta)
    if tt_move_in_node is not None and tt_move is None:
        tt_move = tt_move_in_node

    moves = pos.generate_legal_moves()
    if not moves:
        if pos.is_check(Color.WHITE if pos.side_to_move[0] == 0 else Color.BLACK):
            return -INF + (10 - depth)
        return 0

    moves = order_moves(moves, pos, tt_move)

    max_eval = -INF
    best_move_in_node = None

    for move in moves:
        state = pos.make_move(move)
        eval = -negamax(pos, depth - 1, -beta, -alpha, None)
        pos.unmake_move(state, move)

        if eval > max_eval:
            max_eval = eval
            best_move_in_node = move

        if max_eval > alpha:
            alpha = max_eval
        if beta <= alpha:
            break

    if max_eval <= alpha:
        tt.store(key, max_eval, depth, UPPER, best_move_in_node)
    elif max_eval >= beta:
        tt.store(key, max_eval, depth, LOWER, best_move_in_node)
    else:
        tt.store(key, max_eval, depth, EXACT, best_move_in_node)

    return max_eval

def negamax_root(pos: Position, depth: int, previous_best: Move = None, use_book: bool = True) -> tuple[Move, int]:
    moves = pos.generate_legal_moves()
    if not moves:
        return None, 0

    if use_book and USE_BOOK:
        book_move = book_module.get_book_move(pos)
        if book_move:
            return book_move, 0

    tt_move = None
    if previous_best:
        tt_move = previous_best
    else:
        key = pos.key
        _, tt_move = tt.probe(key, depth, -INF, INF)

    moves = order_moves(moves, pos, tt_move)

    best_move = None
    best_score = -INF
    alpha = -INF
    beta = INF

    for move in moves:
        state = pos.make_move(move)
        score = -negamax(pos, depth - 1, -beta, -alpha, None)
        pos.unmake_move(state, move)

        if score > best_score:
            best_score = score
            best_move = move
        if best_score > alpha:
            alpha = best_score
        if alpha >= beta:
            break

    tt.store(pos.key, best_score, depth, EXACT, best_move)

    return best_move, best_score

def search_best_move(pos: Position, max_depth: int = 3, time_limit: float = None, use_book: bool = True) -> tuple[Move, int]:
    """Iterative deepening search with optional time limit."""
    start_time = time.time()
    best_move = None
    best_score = 0
    previous_best = None

    for depth in range(1, max_depth + 1):
        if time_limit and time.time() - start_time > time_limit:
            break

        move, score = negamax_root(pos, depth, previous_best, use_book)

        if move:
            best_move = move
            best_score = score
            previous_best = move

        if is_checkmate(score):
            break

    return best_move, best_score

def clear_tt():
    tt.clear()

def set_use_book(enabled: bool):
    global USE_BOOK
    USE_BOOK = enabled

def is_using_book():
    return USE_BOOK