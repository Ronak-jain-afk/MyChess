# Quick Start: Using openchess with Cutechess

## Running with Cutechess

### Option 1: Using Batch File (Recommended for Windows)

1. **In Cutechess**, go to **Engines → Manage → New Engine**
2. Set these values:
   - **Name**: openchess
   - **Command**: `path/to/batch/file`
   - **Working Directory**: `path/to/repo`
   - **Protocol**: UCI

3. Click **OK**
4. The engine is ready to use in matches!

### Option 2: Manual Testing

Run the engine directly:
```bash
cd C:\Users\ronak\OneDrive\Desktop\projects\chess
python3 -u main_uci.py
```

Then type UCI commands:
```
uci
position startpos
go depth 3
quit
```

## Engine Specs

- **Search**: Negamax with alpha-beta pruning
- **Search Depth**: Configurable (default 3, can go to 10+)
- **Time Management**: Supports timed games with wtime/btime
- **Opening Book**: 12 positions included
- **Evaluation**: Material + Piece-Square Tables
- **Special Moves**: Castling, en passant, promotion support

## Performance

- **Depth 1**: <0.1 seconds
- **Depth 2**: <0.5 seconds
- **Depth 3**: 1-5 seconds
- **Depth 4**: ~10-20 seconds

## Questions?

Check the documentation in the project root:
- `README.md` - Full documentation
- `FIX_SUMMARY.md` - Details of what was fixed
- `tests/` - Test suite to verify correctness
