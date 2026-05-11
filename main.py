from chess.position import Position
from chess.fen import set_fen, get_fen, STARTING_FEN
from chess.square import square_from_string, square_to_string

def main():
    pos = Position()
    print("=== Starting Position ===")
    print(pos)
    print()

    print("=== FEN ===")
    print(pos.fen())
    print()

    print("=== Pseudo-legal moves ===")
    moves = pos.generate_pseudo_legal_moves()
    print(f"Count: {len(moves)}")
    print("First 5:", [str(m) for m in moves[:5]])
    print()

    print("=== Legal moves ===")
    legal = pos.generate_legal_moves()
    print(f"Count: {len(legal)}")
    print("First 5:", [str(m) for m in legal[:5]])
    print()

    print("=== Make a move ===")
    move = legal[0]
    state = pos.make_move(move)
    print(f"Moved: {move}")
    print(pos)
    print()

    print("=== Unmake move ===")
    pos.unmake_move(state, move)
    print(pos)

if __name__ == "__main__":
    main()