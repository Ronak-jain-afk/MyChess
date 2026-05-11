#!/usr/bin/env python3
"""UCI-compatible chess engine entry point."""

if __name__ == "__main__":
    from chess.uci import uci_loop
    uci_loop()