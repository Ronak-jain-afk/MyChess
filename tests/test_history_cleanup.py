#!/usr/bin/env python3
"""Test that history is properly cleaned on unmake."""

from chess.position import Position
from chess.move import Move

def test_history_cleanup():
    """Verify history.pop() is called on unmake_move."""
    pos = Position()
    assert len(pos.history.keys) == 0, "Initial history should be empty"
    
    # Make a move
    moves = pos.generate_legal_moves()
    move1 = moves[0]
    state1 = pos.make_move(move1)
    assert len(pos.history.keys) == 1, "History should have 1 entry after move"
    
    # Make another move
    moves = pos.generate_legal_moves()
    move2 = moves[0]
    state2 = pos.make_move(move2)
    assert len(pos.history.keys) == 2, "History should have 2 entries after second move"
    
    # Unmake second move
    pos.unmake_move(state2, move2)
    assert len(pos.history.keys) == 1, "History should have 1 entry after unmake"
    
    # Unmake first move
    pos.unmake_move(state1, move1)
    assert len(pos.history.keys) == 0, "History should be empty after all unmakes"
    
    print("✅ History cleanup test passed")

if __name__ == "__main__":
    test_history_cleanup()
