#!/usr/bin/env python3
"""Standalone perft test runner - works without pytest."""

from chess.position import Position
from chess.perft import perft, PERFT_RESULTS

def run_tests():
    print("=" * 50)
    print("Perft Test Results")
    print("=" * 50)

    test_positions = [
        ("Start", "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", {1: 20, 2: 400, 3: 8916}),
    ]

    passed = 0
    failed = 0

    for name, fen, expected in test_positions:
        print(f"\n{name}:")
        print(f"  FEN: {fen}")
        pos = Position(fen)
        for depth, exp in expected.items():
            result = perft(pos, depth)
            status = "✓" if result == exp else "✗"
            print(f"  d{depth}: {result} (expected {exp}) {status}")
            if result == exp:
                passed += 1
            else:
                failed += 1

    print("\n" + "=" * 50)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 50)

    return failed == 0

if __name__ == "__main__":
    import sys
    success = run_tests()
    sys.exit(0 if success else 1)