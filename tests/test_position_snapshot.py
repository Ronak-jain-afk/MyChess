#!/usr/bin/env python3
"""Test that position snapshot prevents race conditions."""

import time
import threading
from chess.position import Position, PositionState

def test_position_snapshot():
    """Verify that main thread can modify position while search has snapshot."""
    # Create initial position with a move
    pos = Position()
    moves = pos.generate_legal_moves()
    state = pos.make_move(moves[0])  # Make move e2e4
    
    fen_after_move = pos.fen()
    assert "4P" in fen_after_move, "Position should have white pawn on e4"
    
    # Create snapshot (simulating parse_go)
    snapshot = PositionState(pos)
    assert snapshot.board[28] == 1, "Snapshot should have white pawn at e4"
    
    # Main thread resets position (simulating next command)
    pos = Position()
    fen_reset = pos.fen()
    assert "PPPPPPPP" in fen_reset, "Reset position should be starting position"
    
    # Reconstruct position from snapshot (simulating search_worker)
    pos_search = Position()
    pos_search.board = snapshot.board.copy()
    pos_search.side_to_move[0] = snapshot.side_to_move
    pos_search.castle_rights[0] = snapshot.castle_rights
    pos_search.ep_square[0] = snapshot.ep_square
    
    # Verify snapshot has the old position
    assert pos_search.board[28] == 1, "Reconstructed position should have pawn at e4"
    assert pos_search.fen() == fen_after_move, "Snapshot should match original position"
    
    print("✅ Position snapshot test passed")

if __name__ == "__main__":
    test_position_snapshot()
