# OpenCodeChess

A Python-based UCI-compatible chess engine with search, evaluation, and opening book support.

## Quick Start

### Option 1: Using the .exe (Recommended for Windows)

Download `chess_engine.exe` from the [Releases](https://github.com/Ronak-jain-afk/MyChess/releases/tag/OpenChessV1) page and use it directly in any UCI-compatible chess GUI (Cutechess, Arena, Chessbase, etc.).

### Option 2: Using Python

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

### For .exe
- Windows 10/11 (64-bit)
- No Python required - fully standalone!

### For Python
- Python 3.8+
- No external dependencies (pure Python)

## Running the Engine

### .exe (Standalone)

Simply run `chess_engine.exe` - it accepts UCI commands via stdin:

```batch
chess_engine.exe
```

### Python Source

```bash
python3 -u main_uci.py
```

### With custom opening book (Python only)

Create or edit `book.txt` with your opening lines:
```
rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR e2e4 d2d4
```

The engine will automatically use moves from the book when available.

## Cutechess Setup

See [CUTECHESS_GUIDE.md](CUTECHESS_GUIDE.md) for detailed setup instructions.

Quick setup with .exe:
1. Open Cutechess → Engines → Manage → New Engine
2. Set:
   - **Name**: OpenCodeChess
   - **Command**: `C:\path\to\chess_engine.exe`
   - **Working Directory**: `C:\path\to\`
   - **Protocol**: UCI

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

Pass depth via UCI:
```
go depth 10
```

### Opening Book (Python only)

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