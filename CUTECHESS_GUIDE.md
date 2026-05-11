# Cutechess Setup Guide

This guide explains how to set up OpenCodeChess in Cutechess.

## Option 1: Using .exe (Recommended - No Python Required!)

Download `chess_engine.exe` from the [Releases](https://github.com/yourusername/chess/releases) page.

### Setup Steps

1. **Open Cutechess**
2. **Go to Engines → Manage**
3. **Click "New Engine"**
4. **Configure the engine:**

| Setting | Value |
|---------|-------|
| Name | OpenCodeChess |
| Command | `C:\path\to\chess_engine.exe` |
| Working Directory | `C:\path\to\` |
| Protocol | UCI |

Example:
- **Command**: `C:\Users\Ronak\Downloads\chess_engine.exe`
- **Working Directory**: `C:\Users\Ronak\Downloads`

5. **Click OK**

That's it! The engine is ready to use.

---

## Option 2: Using Python (If you want to run from source)

If you want to run the Python source code instead of the .exe:

### Setup Steps

1. **Open Cutechess**
2. **Go to Engines → Manage**
3. **Click "New Engine"**
4. **Configure using the batch file:**

| Setting | Value |
|---------|-------|
| Name | OpenCodeChess |
| Command | `C:\path\to\chess\run_engine.bat` |
| Working Directory | `C:\path\to\chess\` |
| Protocol | UCI |

Or configure using Python directly:

| Setting | Value |
|---------|-------|
| Name | OpenCodeChess |
| Command | `python3 -u C:\path\to\chess\main_uci.py` |
| Working Directory | `C:\path\to\chess\` |
| Protocol | UCI |

**Note**: Use forward slashes in paths: `C:/Users/...` instead of `C:\Users\...`

---

## Starting a Match

1. **File → New Game** (or press Ctrl+N)
2. **Select your engine** as White or Black
3. **Select an opponent** (or add another engine)
4. **Configure time control** (optional)
5. **Click "Start"**

---

## Engine Configuration

### Setting Search Depth

In the game window, you can set the search depth in the engine configuration:

```
go depth 10
```

Or configure it in Cutechess:
- **Engines → Configure** → Set time or depth limits

### Opening Book

The Python version includes an opening book (`book.txt`). The .exe also includes the book.

---

## Troubleshooting

### "Cannot execute command" error

- **Solution**: Use forward slashes: `C:/Users/...`
- **Or**: Use the batch file `run_engine.bat`

### Engine very slow

- **Solution**: Reduce search depth in Cutechess settings
- **Default depth**: 3 (should complete in 1-5 seconds)
- **For faster games**: Set depth to 2

### Engine crashes

- If running Python: Ensure Python 3.8+ is installed
- Check that all required files are present
- Try running the engine manually to see error messages

### Manual Testing

To test the engine from command line:

```batch
cd C:\path\to\chess
chess_engine.exe
```

Then type UCI commands:
```
uci
position startpos
go depth 3
quit
```

---

## Performance Notes

| Depth | Approximate Time |
|-------|------------------|
| 1 | <0.1 seconds |
| 2 | <0.5 seconds |
| 3 | 1-5 seconds |
| 4 | 5-20 seconds |
| 5+ | Depends on hardware |

---

## Need Help?

- Check the main [README.md](README.md) for full documentation
- See [FIX_SUMMARY.md](FIX_SUMMARY.md) for technical details