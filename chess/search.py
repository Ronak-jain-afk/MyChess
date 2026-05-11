from chess.position import Position
from chess.move import Move
from chess import evaluate
from chess.constants import Color

INF = 100000000

def negamax(pos: Position, depth: int, alpha: int, beta: int) -> int:
    if depth == 0:
        return evaluate.evaluate(pos)

    moves = pos.generate_legal_moves()
    if not moves:
        if pos.is_check(Color.WHITE if pos.side_to_move[0] == 0 else Color.BLACK):
            return -INF + (10 - depth)  # Checkmate favor sooner
        return 0  # Stalemate/draw

    max_eval = -INF
    for move in moves:
        state = pos.make_move(move)
        eval = -negamax(pos, depth - 1, -beta, -alpha)
        pos.unmake_move(state, move)

        if eval > max_eval:
            max_eval = eval
        if max_eval > alpha:
            alpha = max_eval
        if beta <= alpha:
            break

    return max_eval


def negamax_root(pos: Position, depth: int) -> tuple[Move, int]:
    moves = pos.generate_legal_moves()
    if not moves:
        return None, 0

    best_move = None
    best_score = -INF
    alpha = -INF
    beta = INF

    for move in moves:
        state = pos.make_move(move)
        score = -negamax(pos, depth - 1, -beta, -alpha)
        pos.unmake_move(state, move)

        if score > best_score:
            best_score = score
            best_move = move
        if best_score > alpha:
            alpha = best_score
        if alpha >= beta:
            break

    return best_move, best_score


def search_best_move(pos: Position, max_depth: int = 3) -> tuple[Move, int]:
    """Iterative deepening search."""
    best_move = None
    best_score = 0

    for depth in range(1, max_depth + 1):
        move, score = negamax_root(pos, depth)
        if move is not None:
            best_move = move
            best_score = score

    return best_move, best_score