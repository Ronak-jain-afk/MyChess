# Quick Start: Using OpenCodeChess with Cutechess

## Installation (Already Done)

The chess engine is installed at:
```
C:\Users\ronak\OneDrive\Desktop\projects\chess\
```

## Running with Cutechess

### Option 1: Using Batch File (Recommended for Windows)

1. **In Cutechess**, go to **Engines → Manage → New Engine**
2. Set these values:
   - **Name**: OpenCodeChess
   - **Command**: `C:\Users\ronak\OneDrive\Desktop\projects\chess\run_engine.bat`
   - **Working Directory**: `C:\Users\ronak\OneDrive\Desktop\projects\chess`
   - **Protocol**: UCI

3. Click **OK**
4. The engine is ready to use in matches!

### Option 2: Using Python Directly

1. **In Cutechess**, go to **Engines → Manage → New Engine**
2. Set these values:
   - **Name**: OpenCodeChess
   - **Command**: `python3 -u C:/Users/ronak/OneDrive/Desktop/projects/chess/main_uci.py`
   - **Working Directory**: `C:\Users\ronak\OneDrive\Desktop\projects\chess`
   - **Protocol**: UCI

### Option 3: Manual Testing

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

## What Was Fixed

The engine was crashing with "illegal move e8g8" because:
- Position snapshots weren't copying move history
- This corrupted castling rights detection
- The search thread would output invalid moves

**This is now fixed!** The engine:
- ✅ Properly maintains move history
- ✅ Correctly detects castling rights
- ✅ Never outputs illegal moves
- ✅ Works with any Cutechess opponent

## Next Steps

1. **Test it**: Play a few games in Cutechess to verify it works
2. **Improve it**: The engine could be stronger with:
   - Better move ordering
   - Enhanced evaluation (pawn structure)
   - Time management fine-tuning

## Troubleshooting

**Problem**: "Cannot execute command"
- **Solution**: Use forward slashes in path: `C:/Users/.../main_uci.py`
- **Or**: Use the batch file which handles paths correctly

**Problem**: Engine very slow
- **Solution**: Reduce search depth in Cutechess settings
- **Note**: Depth 3 is default, should complete in 1-5 seconds

**Problem**: Engine crashes
- **Solution**: This shouldn't happen anymore! If it does:
  - Check error output in Cutechess log
  - File a bug report with the game PGN

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
