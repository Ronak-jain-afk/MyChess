#!/usr/bin/env python3
"""Test that book parser uses specific exceptions, not bare except."""

from chess.book import OpeningBook
from chess.position import Position

def test_book_specific_exceptions():
    """Verify that specific exceptions are caught, not all exceptions."""
    book = OpeningBook()
    pos = Position()
    
    # Valid move string should work
    move = book.move_from_uci(pos, "e2e4")
    assert move is not None, "Valid move string should return a Move"
    assert move.frm == 12 and move.to == 28, "Move e2e4 should be from 12 to 28"
    
    # Invalid square notation should return None
    move = book.move_from_uci(pos, "zzzzzz")
    assert move is None, "Invalid square should return None"
    
    # Out of bounds should return None
    move = book.move_from_uci(pos, "h8h9")
    assert move is None, "Out of bounds should return None"
    
    # Short string should return None
    move = book.move_from_uci(pos, "e2")
    assert move is None, "Short string should return None"
    
    print("✅ Book exceptions test passed")

if __name__ == "__main__":
    test_book_specific_exceptions()
