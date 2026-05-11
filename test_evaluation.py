#!/usr/bin/env python3
"""Evaluation function test suite."""

from chess.position import Position
from chess import evaluate

def test_evaluate():
    print("=== Evaluation Tests ===\n")

    # Test 1: Start position - should be 0 (balanced)
    pos = Position()
    result = evaluate.evaluate(pos)
    assert result == 0, f"Start position: expected 0, got {result}"
    print("1. Start position: PASS")

    # Test 2: White has extra queen
    pos2 = Position()
    pos2.board[59] = 0  # Remove black queen at d8
    result2 = evaluate.evaluate(pos2)
    assert 800 < result2 < 1000, f"Extra queen: expected ~900, got {result2}"
    print("2. White extra queen: PASS")

    # Test 3: White has extra rook
    pos3 = Position()
    pos3.board[56] = 0  # Remove black rook at a8
    result3 = evaluate.evaluate(pos3)
    assert 400 < result3 < 600, f"Extra rook: expected ~500, got {result3}"
    print("3. White extra rook: PASS")

    # Test 4: Black to move with advantage
    pos4 = Position()
    pos4.side_to_move[0] = 1  # Black to move
    pos4.board[8] = 0  # Remove white pawn a2
    result4 = evaluate.evaluate(pos4)
    assert 100 < result4 < 200, f"Black to move: expected ~150, got {result4}"
    print("4. Black to move, white down pawn: PASS")

    print("\n=== All Tests Passed ===")
    return True

if __name__ == "__main__":
    test_evaluate()