from chess.position import Position

def perft(pos: Position, depth: int) -> int:
    """Count all leaf nodes at given depth."""
    if depth == 0:
        return 1
    moves = pos.generate_legal_moves()
    if depth == 1:
        return len(moves)
    total = 0
    for move in moves:
        state = pos.make_move(move)
        total += perft(pos, depth - 1)
        pos.unmake_move(state, move)
    return total

def perft_divide(pos: Position, depth: int) -> dict:
    """Return dict of move -> count for debugging."""
    moves = pos.generate_legal_moves()
    if depth == 1:
        return {str(m): 1 for m in moves}
    result = {}
    for move in moves:
        state = pos.make_move(move)
        count = perft(pos, depth - 1)
        result[str(move)] = count
        pos.unmake_move(state, move)
    return result

PERFT_RESULTS = {
    "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1": {
        1: 20,
        2: 400,
        3: 8902,
    },
}