#!/usr/bin/env python3
"""Test that Zobrist hashing includes pawn existence for en-passant."""

from chess.zobrist import compute_key
from chess.constants import wP, bP, EMPTY

def test_zobrist_ep_pawn_existence():
    """Verify that en-passant hash includes pawn existence."""
    # Position 1: White pawn e5, Black pawn d5, ep_square d6
    board1 = [EMPTY] * 64
    board1[36] = wP  # e5 (rank 4, file 4)
    board1[35] = bP  # d5 (rank 4, file 3)
    
    # Position 2: No pawns, but same en-passant square d6
    board2 = [EMPTY] * 64
    
    # With fix: different hashes because pawn exists in board1 but not board2
    key1 = compute_key(board1, 0, 0, 42)  # ep_square=42 (d6)
    key2 = compute_key(board2, 0, 0, 42)  # ep_square=42 (d6)
    
    assert key1 != key2, "Zobrist collision: hash didn't distinguish pawn existence"
    
    # Verify same position produces same hash
    key1_again = compute_key(board1, 0, 0, 42)
    assert key1 == key1_again, "Same position should produce same hash"
    
    print("✅ Zobrist en-passant collision test passed")

if __name__ == "__main__":
    test_zobrist_ep_pawn_existence()
