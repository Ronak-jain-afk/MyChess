# Detailed Bug Report with Code Snippets

## BUG #1: FEN Parsing - Incorrect Token Handling

### Location
`chess/uci.py`, lines 18-26

### Current Code (BROKEN)
```python
def parse_position(self, args):
    if args[0] == "startpos":
        self.position = Position()
        moves_start = 1
    elif args[0] == "fen":
        fen = args[1]  # ❌ WRONG: Takes only first token!
        self.position = Position(fen)  # ❌ ValueError!
        moves_start = 2  # ❌ WRONG: Should be 7 (1 + 6 FEN parts)
    else:
        return

    if len(args) > moves_start and args[moves_start] == "moves":
        for move_str in args[moves_start + 1:]:
            move = self.move_from_uci(move_str)
            if move:
                self.position.make_move(move)
```

### Problem Explanation
When the main loop receives:
```
position fen rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1 moves e2e4
```

It splits and calls:
```python
parse_position(["fen", "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR", "w", "KQkq", "-", "0", "1", "moves", "e2e4"])
```

The code then does:
```python
fen = args[1]  # Gets only: "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"
Position(fen)  # Passes incomplete FEN string!
```

The Position constructor expects:
```
"rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
```

But gets:
```
"rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"
```

### Proposed Fix
```python
def parse_position(self, args):
    if args[0] == "startpos":
        self.position = Position()
        moves_start = 1
    elif args[0] == "fen":
        # Find the "moves" keyword to know where FEN ends
        try:
            moves_idx = args.index("moves")
            fen = " ".join(args[1:moves_idx])  # Join all FEN parts
        except ValueError:
            # No "moves" keyword found, FEN goes to end
            fen = " ".join(args[1:])
            moves_idx = len(args)
        
        self.position = Position(fen)
        moves_start = moves_idx
    else:
        return

    if len(args) > moves_start and args[moves_start] == "moves":
        for move_str in args[moves_start + 1:]:
            move = self.move_from_uci(move_str)
            if move:
                self.position.make_move(move)
```

---

## BUG #2: Bare Exception Handling

### Location
`chess/uci.py`, lines 42-46

### Current Code (WRONG)
```python
def move_from_uci(self, uci_str):
    from chess.square import square_from_string
    from chess.move import Move, FLAG_PROMO_QUEEN, FLAG_PROMO_ROOK, FLAG_PROMO_BISHOP, FLAG_PROMO_KNIGHT

    if len(uci_str) < 4:
        return None

    try:
        from_sq = square_from_string(uci_str[:2])
        to_sq = square_from_string(uci_str[2:4])
    except:  # ❌ WRONG: Catches ALL exceptions!
        return None

    # ...rest of function
```

### Problem
- Catches KeyboardInterrupt (Ctrl+C) → Can't shut down engine
- Catches SystemExit → Can't exit program
- Catches GeneratorExit → Blocks cleanup
- Swallows all exceptions silently → Hard to debug

### Proposed Fix
```python
try:
    from_sq = square_from_string(uci_str[:2])
    to_sq = square_from_string(uci_str[2:4])
except (ValueError, IndexError):
    return None
```

---

## BUG #3: Race Condition in search_worker

### Location
`chess/uci.py`, lines 120-128

### Current Code (RACE CONDITION)
```python
def search_worker(self):
    if self.infinite:
        self.best_move, self.score = search.negamax_root(self.position, self.depth)
    else:
        self.best_move, self.score = search.negamax_root(self.position, self.depth)

    if not self.stop_event.is_set():  # ❌ Check
        print(f"bestmove {self.move_to_uci(self.best_move)}")  # ❌ Print (NOT atomic!)
        sys.stdout.flush()
```

### Race Scenario
```
Time 1: search_worker thread: if not self.stop_event.is_set()  → Returns False (OK to print)
Time 2: main thread: stop() → sets stop_event
Time 3: search_worker thread: print(bestmove)  → Prints after stop!
```

### Proposed Fix
```python
def search_worker(self):
    self.best_move, self.score = search.negamax_root(self.position, self.depth)
    
    # Make check and output atomic
    if not self.stop_event.is_set():
        self.stop_event.set()  # Claim output right
        print(f"bestmove {self.move_to_uci(self.best_move)}")
        sys.stdout.flush()
```

---

## BUG #4 & #5: Invalid Protocol Responses

### Location
`chess/uci.py`, lines 140-142, 157-160, 164-167, 171-172

### Current Code (WRONG)
```python
def run(self):
    # ❌ WRONG: Sends on startup before command received
    print("id name OpenCodeChess")
    print("id author Developer")
    print("uciok")
    sys.stdout.flush()

    while True:
        # ...
        if parts[0] == "uci":
            # ❌ WRONG: Sends AGAIN here
            print("id name OpenCodeChess")
            print("id author Developer")
            print("uciok")
            sys.stdout.flush()
        elif parts[0] == "isready":
            print("readyok")
            sys.stdout.flush()
        elif parts[0] == "ucinewgame":
            self.reset()
            print("readyok")  # ❌ WRONG: ucinewgame expects NO response
            sys.stdout.flush()
        elif parts[0] == "position":
            self.stop_search()
            self.parse_position(parts[1:])
            print("readyok")  # ❌ WRONG: position expects NO response
            sys.stdout.flush()
```

### UCI Protocol Requirements
```
uci              → "id name\nid author\nuciok\n" (CORRECT when handled here)
ucinewgame       → (no response)
isready          → "readyok"
position         → (no response)
go               → (starts search)
stop             → "bestmove ..."
quit             → (shutdown)
```

### Proposed Fix
```python
def run(self):
    # Don't send anything until "uci" command received
    
    while True:
        line = sys.stdin.readline()
        if not line:
            break

        line = line.strip()
        if not line:
            continue

        parts = line.split()

        if parts[0] == "uci":
            # ✅ CORRECT: Only send here
            print("id name OpenCodeChess")
            print("id author Developer")
            print("uciok")
            sys.stdout.flush()
        elif parts[0] == "isready":
            print("readyok")
            sys.stdout.flush()
        elif parts[0] == "ucinewgame":
            self.reset()
            # ✅ NO RESPONSE
        elif parts[0] == "position":
            self.stop_search()
            self.parse_position(parts[1:])
            # ✅ NO RESPONSE
        elif parts[0] == "go":
            self.parse_go(parts[1:])
            # Response comes from search_worker
        elif parts[0] == "stop":
            self.stop_search()
            if self.best_move:
                print(f"bestmove {self.move_to_uci(self.best_move)}")
                sys.stdout.flush()
        elif parts[0] == "quit":
            self.stop_search()
            break
```

---

## BUG #6: Time Limit Never Used

### Location
`chess/uci.py`, lines 80-124

### Current Code
```python
def parse_go(self, args):
    # ... parsing ...
    
    if not self.infinite and wtime and btime:
        if self.position.side_to_move[0] == 0:
            time_limit = wtime // 20 + winc
        else:
            time_limit = btime // 20 + binc
        self.search_time = time_limit / 1000.0  # ❌ Calculated but never used!
    else:
        self.search_time = None

    self.stop_event.clear()
    self.search_thread = threading.Thread(target=self.search_worker)
    self.search_thread.start()

def search_worker(self):
    if self.infinite:
        self.best_move, self.score = search.negamax_root(self.position, self.depth)
    else:
        self.best_move, self.score = search.negamax_root(self.position, self.depth)
    # ❌ WRONG: search_time is never consulted!
    
    if not self.stop_event.is_set():
        print(f"bestmove {self.move_to_uci(self.best_move)}")
        sys.stdout.flush()
```

### Problem
- Engine always searches to fixed depth (3)
- Completely ignores time constraints
- Cannot play timed games correctly
- GUI has no control over search duration

### Proposed Fix
```python
def search_worker(self):
    if self.infinite:
        max_depth = 100  # Effectively infinite
    else:
        max_depth = self.depth
    
    start_time = time.time()
    
    # Iterative deepening with time check
    for d in range(1, max_depth + 1):
        if self.search_time:
            elapsed = time.time() - start_time
            if elapsed > self.search_time:
                break  # Stop if time exceeded
        
        self.best_move, self.score = search.negamax_root(self.position, d)
        
        if self.stop_event.is_set():
            break
    
    if not self.stop_event.is_set():
        self.stop_event.set()  # Prevent main thread race
        print(f"bestmove {self.move_to_uci(self.best_move)}")
        sys.stdout.flush()
```

---

## BUG #7: Stop Command Produces No Output

### Location
`chess/uci.py`, lines 130-133, 175-179

### Current Code
```python
def stop_search(self):
    if self.search_thread and self.search_thread.is_alive():
        self.stop_event.set()
        self.search_thread.join()
    # ❌ No output!

# In run():
elif parts[0] == "stop":
    self.stop_search()
    if self.best_move:  # ❌ Only outputs if best_move exists
        print(f"bestmove {self.move_to_uci(self.best_move)}")
        sys.stdout.flush()
```

### Problem
- UCI spec requires "bestmove" response to every "stop"
- Current code only outputs if best_move is not None
- If no search was active: no output → GUI hangs
- If best_move is None: no output → GUI hangs

### Proposed Fix
```python
elif parts[0] == "stop":
    self.stop_search()
    
    # Always output bestmove, even if no search active
    if self.best_move is None:
        # Get first legal move as fallback
        legal_moves = self.position.generate_legal_moves()
        if legal_moves:
            self.best_move = legal_moves[0]
    
    if self.best_move:
        print(f"bestmove {self.move_to_uci(self.best_move)}")
    else:
        print("bestmove 0000")  # Null move if nothing available
    
    sys.stdout.flush()
```

---

## BUG #9: No Move Legality Validation

### Location
`chess/uci.py`, lines 29-33

### Current Code
```python
if len(args) > moves_start and args[moves_start] == "moves":
    for move_str in args[moves_start + 1:]:
        move = self.move_from_uci(move_str)
        if move:
            self.position.make_move(move)  # ❌ No legality check!
```

### Problem Example
```
position startpos moves e2e5
```

- e2e5 is ILLEGAL (pawn can't move 3 squares)
- move_from_uci only checks format ("e2e5" is valid format)
- make_move accepts it and corrupts position
- Position is now in undefined state

### Proposed Fix
```python
if len(args) > moves_start and args[moves_start] == "moves":
    for move_str in args[moves_start + 1:]:
        move = self.move_from_uci(move_str)
        if move:
            # Check if move is legal
            legal_moves = self.position.generate_legal_moves()
            
            # Need to compare Move objects properly
            move_found = False
            for legal_move in legal_moves:
                if (legal_move.frm == move.frm and 
                    legal_move.to == move.to and 
                    legal_move.flags == move.flags):
                    move_found = True
                    break
            
            if move_found:
                self.position.make_move(move)
            else:
                # Log error or silently skip?
                # For now, silently skip illegal moves
                pass
```

---

## Summary of All Bugs

| # | File | Lines | Issue | Fix Complexity |
|---|------|-------|-------|---|
| 1 | uci.py | 18-26 | FEN parsing broken | Medium |
| 2 | uci.py | 42-46 | Bare except | Low |
| 3 | uci.py | 120-128 | Race condition | Medium |
| 4 | uci.py | 166, 171 | Invalid responses | Low |
| 5 | uci.py | 140-160 | Duplicate ID | Low |
| 6 | uci.py | 80-124 | Time unused | Medium |
| 7 | uci.py | 130-179 | Stop no output | Low |
| 8 | uci.py | 42-46 | Exception mask | Low |
| 9 | uci.py | 29-33 | No legality check | Medium |
| 10 | uci.py | 39-46 | Same square moves | Low |
| 11 | uci.py | 62-78 | Code quality | Low |
| 12 | uci.py | 121-124 | Dead code | Low |
| 13 | uci.py | 135-137 | State leak | Low |
| 14 | uci.py | 89-105 | Index bounds | None |
| 15 | uci.py | 29-33 | No error handle | Low |
| 16 | main_uci.py | 6-7 | Path setup | Low |
| 17 | uci.py | 127 | (Not a bug) | — |

