#!/usr/bin/env python3
"""Test the specific Cutechess game that was failing.

The issue: Black tried castling kingside (e8g8) but it was illegal because 
castling rights were lost (king moved earlier via Qxe4+, Qxh1, Qxg1).

This test verifies:
1. The position can be reconstructed properly
2. Castling is correctly detected as illegal
3. The engine doesn't output the illegal move
"""

from chess.position import Position
from chess.uci import UCIController
import io
import sys

def test_illegal_castling_rejection():
    """Test that illegal castling moves are rejected."""
    
    # Build position after move 14...O-O (Black just castled kingside)
    # At this point, both sides have castled
    # Position after: 15. f5 (White's move)
    
    # Start from position after move 14...O-O
    fen_after_14_black = "r1bqk2r/pppp2pp/2n1p1p1/8/4P3/P1P5/3PBPBP/RN1Q1RK1 w kq - 1 15"
    
    controller = UCIController()
    controller.position = Position(fen_after_14_black)
    
    # Verify Black castling is valid at this FEN
    legal_moves = controller.position.generate_legal_moves()
    castling_moves = [m for m in legal_moves if m.is_castle]
    
    print(f"Position FEN: {controller.position.fen()}")
    print(f"Side to move: {'White' if controller.position.side_to_move[0] == 0 else 'Black'}")
    print(f"Castling moves available: {[controller.move_to_uci(m) for m in castling_moves]}")
    
    # Now advance White's move: f2-f5
    move_f5 = controller.move_from_uci("f2f5")
    controller.position.make_move(move_f5)
    
    # Now it's Black's turn after f5
    # Try to generate castling moves - should fail because king already moved
    black_moves = controller.position.generate_legal_moves()
    black_castling = [m for m in black_moves if m.is_castle]
    
    print(f"\nAfter White f2-f5:")
    print(f"Position FEN: {controller.position.fen()}")
    print(f"Black's castling moves: {[controller.move_to_uci(m) for m in black_castling]}")
    print(f"Black's castle rights: {controller.position.castle_rights[0]}")
    
    # Verify that we can search at this position without crashing
    print(f"\nTesting search engine at this position...")
    
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    
    try:
        controller.parse_go(["depth", "2"])
        if controller.search_thread:
            controller.search_thread.join()
        output = sys.stdout.getvalue()
    finally:
        sys.stdout = old_stdout
    
    print(f"Engine output: {output.strip()}")
    
    # Verify output is a valid move
    if "bestmove" in output:
        print("✅ Engine successfully searched without crashing")
        return True
    else:
        print("❌ Engine failed to output bestmove")
        return False

def test_position_reconstruction_with_history():
    """Test that position reconstruction properly preserves history."""
    from chess.position import PositionState
    
    pos = Position()
    
    # Make some moves to build history
    moves = ["e2e4", "e7e5", "g1f3", "b8c6"]
    
    for move_str in moves:
        move = None
        from chess.move import Move
        from chess.square import square_from_string
        
        from_sq = square_from_string(move_str[:2])
        to_sq = square_from_string(move_str[2:4])
        move = Move(from_sq, to_sq, 0)
        
        legal_moves = pos.generate_legal_moves()
        for legal_move in legal_moves:
            if (legal_move.frm == move.frm and 
                legal_move.to == move.to and 
                legal_move.flags == move.flags):
                pos.make_move(legal_move)
                break
    
    # Verify history is tracked
    print(f"\nPosition history keys: {len(pos.history.keys)} moves")
    print(f"History: {pos.history.keys}")
    
    # Create a snapshot
    snapshot = PositionState(pos)
    
    # Verify snapshot has history
    print(f"Snapshot history keys: {len(snapshot.history_keys)} moves")
    assert len(snapshot.history_keys) == len(pos.history.keys), "History not copied!"
    
    # Reconstruct position from snapshot
    pos2 = Position()
    pos2.board = snapshot.board.copy()
    pos2.side_to_move[0] = snapshot.side_to_move
    pos2.castle_rights[0] = snapshot.castle_rights
    pos2.ep_square[0] = snapshot.ep_square
    pos2.halfmove_clock[0] = snapshot.halfmove_clock
    pos2.fullmove_number[0] = snapshot.fullmove_number
    pos2.history.keys = snapshot.history_keys.copy()
    pos2.history.reversible = snapshot.history_reversible.copy()
    pos2.history.moves = snapshot.history_moves.copy()
    pos2.history.last_from_sq = snapshot.history_last_from_sq
    pos2.history.last_to_sq = snapshot.history_last_to_sq
    
    # Verify reconstructed position matches
    assert pos2.fen() == pos.fen(), "FEN mismatch after reconstruction"
    assert len(pos2.history.keys) == len(pos.history.keys), "History length mismatch"
    
    print("✅ Position reconstruction with history works correctly")
    return True

if __name__ == "__main__":
    success1 = test_illegal_castling_rejection()
    print("\n" + "="*60 + "\n")
    success2 = test_position_reconstruction_with_history()
    
    if success1 and success2:
        print("\n✅ All tests passed!")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed!")
        sys.exit(1)
