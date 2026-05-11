# OpenChess

A Python-based UCI-compatible chess engine with search, evaluation, and opening book support.

## Quick Start

**Using with Cutechess GUI?** See [CUTECHESS_GUIDE.md](CUTECHESS_GUIDE.md)

**Just want to run it?**
```bash
python3 -u main_uci.py
```

## Features

- **Move Generation**: Full legal move generation including castling, en passant, and promotions
- **Search**: Negamax with alpha-beta pruning, iterative deepening, and transposition table
- **Evaluation**: Material values + piece-square tables
- **Opening Book**: Configurable opening book support
- **UCI Protocol**: Compatible with any UCI-compatible chess GUI
- **Threefold Repetition**: Draw detection for repeated positions
- **Insufficient Material**: Draw detection for K vs K, K+N vs K, etc.

## Requirements

- Python 3.8+
- No external dependencies (pure Python)

## Running the Engine

### Basic (from project root)

```bash
python3 -u main_uci.py
```

### With custom opening book

Create or edit `book.txt` with your opening lines:
```
rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR e2e4 d2d4
```

The engine will automatically use moves from the book when available.

## UCI Commands Supported

| Command | Description |
|---------|-------------|
| `uci` | Engine identification |
| `isready` | Ready check |
| `ucinewgame` | Reset for new game |
| `position [fen\|startpos]` | Set position |
| `position ... moves ...` | Set position and apply moves |
| `go depth N` | Search to depth N |
| `go wtime N btime N` | Time-controlled search |
| `stop` | Stop searching |
| `quit` | Exit |

## Testing

```bash
# Run perft tests
python3 run_perft_tests.py
```

Expected results:
- Perft depth 1: 20
- Perft depth 2: 400
- Perft depth 3: 8,902

## Project Structure

```
chess/
├── __init__.py           # Package init
├── constants.py          # Piece constants, colors
├── square.py            # Square math utilities
├── move.py              # Move representation
├── position.py          # Board state
├── fen.py               # FEN parsing/generation
├── zobrist.py           # Zobrist hashing
├── history.py           # Threefold repetition
├── moves.py             # Move generation
├── evaluate.py          # Position evaluation
├── search.py            # Negamax search + TT
├── tt.py                # Transposition table
├── book.py              # Opening book
├── uci.py               # UCI protocol handler
└── main_uci.py          # Entry point
```

## Configuration

### Search Depth

Modify `main_uci.py` or pass depth via UCI:
```
go depth 10
```

### Opening Book

Edit `book.txt` in the format:
```
<position_fen> move1 move2 ...
```

Example:
```
rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR e2e4 d2d4 c2c4
```

## Performance

- Search depth 1-3 in <1 second
- Search depth 4 in ~5 seconds
- Transposition table with 1M entries

## Documentation

| File | Description |
|------|-------------|
| [CUTECHESS_GUIDE.md](CUTECHESS_GUIDE.md) | Setup guide for Cutechess GUI |
| [FIX_SUMMARY.md](FIX_SUMMARY.md) | Technical details of bug fixes |
| [docs/bugs/](docs/bugs/) | Historical bug reports |
| [docs/audits/](docs/audits/) | Code audit reports |

## License

MIT License

## Credits

- Chess Programming Wiki (chessprogramming.org) for algorithms
- UCI protocol specification