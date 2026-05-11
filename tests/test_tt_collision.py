#!/usr/bin/env python3
"""Test that TT hash collisions don't corrupt entries."""

from chess.tt import TranspositionTable, EXACT

def test_tt_collision_no_corruption():
    """Test that colliding keys don't overwrite different positions."""
    tt = TranspositionTable(size=10)  # Small size to force collisions
    
    # Store entry for key 1
    tt.store(1, 100, 3, EXACT, None)
    
    # Store entry for key 11 (collides with 1 due to modulo 10)
    tt.store(11, 200, 2, EXACT, None)
    
    # Verify key 1 is not corrupted (key check should prevent overwrite)
    result1, _ = tt.probe(1, 3, float('-inf'), float('inf'))
    assert result1 == 100, f"Position 1 corrupted by collision (got {result1})"
    
    # Verify key 11 was stored
    result11, _ = tt.probe(11, 2, float('-inf'), float('inf'))
    assert result11 == 200, f"Position 11 not stored correctly (got {result11})"
    
    print("✅ TT collision test passed")

if __name__ == "__main__":
    test_tt_collision_no_corruption()
