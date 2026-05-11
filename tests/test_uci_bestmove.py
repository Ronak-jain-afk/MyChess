#!/usr/bin/env python3
"""Test that bestmove is printed exactly once (no race condition)."""

import io
import sys
import time
from chess.uci import UCIController

def test_bestmove_once():
    """Verify bestmove is always printed exactly once."""
    # Capture stdout
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    
    try:
        controller = UCIController()
        
        # Start a search
        controller.parse_go(["depth", "1"])
        
        # Wait for search to complete
        time.sleep(0.5)
        
        # Stop search (should trigger bestmove output)
        controller.stop_search()
        
        # Get output
        output = sys.stdout.getvalue()
        
    finally:
        sys.stdout = old_stdout
    
    # Count bestmove occurrences
    bestmove_count = output.count("bestmove")
    assert bestmove_count == 1, f"Expected 1 bestmove, got {bestmove_count}. Output:\n{output}"
    
    print("✅ UCI race condition test passed")

if __name__ == "__main__":
    test_bestmove_once()
