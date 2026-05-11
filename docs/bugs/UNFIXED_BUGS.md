# UNFIXED BUGS - DETAILED ANALYSIS

**Analysis Date:** 2026-05-11  
**Total Analyzed:** 37 non-critical bugs  
**Status:** Determining which are actually unfixed

---

## HIGH SEVERITY BUGS (12)

### H1: FEN String Parsing ✅ FIXED
- **File:** `chess/uci.py:23-32`
- **Status:** FIXED - properly joins all 6 FEN parts
- **Evidence:** Code uses `args.index("moves")` to find delimiter, then `" ".join(args[1:moves_idx])`

### H2: Bare Exception Handling ✅ FIXED
- **File:** `chess/uci.py:70-74`
- **Status:** FIXED - uses specific `(ValueError, IndexError)` exceptions
- **Evidence:** Code at line 73 shows proper exception types

### H3: Race Condition ✅ FIXED
- **File:** `chess/uci.py:180-182`
- **Status:** FIXED - search_worker always prints bestmove once
- **Evidence:** No check-then-set pattern, always outputs

### H4: Invalid Protocol Responses ✅ FIXED
- **File:** `chess/uci.py:219-225`
- **Status:** FIXED - no responses sent to position/ucinewgame
- **Evidence:** Comments explicitly state "No response expected"

### H5: Duplicate UCI Identification ✅ FIXED
- **File:** `chess/uci.py:196-215`
- **Status:** FIXED - only sends on uci command, not at startup
- **Evidence:** run() method doesn't print until uci command received

### H6: Time Management Not Used ✅ FIXED
- **File:** `chess/uci.py:162-170`
- **Status:** FIXED - time limit checked in search loop
- **Evidence:** `if time_limit and time.time() - start_time > time_limit: break`

### H7: Stop No Output ✅ FIXED
- **File:** `chess/uci.py:232-241`
- **Status:** FIXED - always outputs bestmove on stop
- **Evidence:** Falls back to first legal move if best_move is None

### H8: TT Hash Collision ✅ FIXED (Milestone 11)
- **File:** `chess/tt.py:49`
- **Status:** FIXED - key verification added
- **Evidence:** Documented in CRITICAL_FIXES_COMPLETE.md

### H9: No Move Legality Validation ✅ FIXED
- **File:** `chess/uci.py:41-52`
- **Status:** FIXED - validates against legal moves before making
- **Evidence:** Generates legal_moves and checks match before apply

### H10: Same Square Moves ✅ FIXED
- **File:** `chess/uci.py:67-68`
- **Status:** FIXED - rejects if from_sq == to_sq
- **Evidence:** `if uci_str[:2] == uci_str[2:4]: return None`

### H11: Code Quality - Duplicate Logic ✅ FIXED
- **File:** `chess/uci.py:92-97`
- **Status:** FIXED - uses move.promo_char property
- **Evidence:** No duplicate logic, clean implementation

### H12: Dead Code ✅ FIXED
- **File:** `chess/uci.py:165-178`
- **Status:** FIXED - iterative deepening loop implemented cleanly
- **Evidence:** No duplicate if/else, proper loop structure

**SUMMARY: ALL 12 HIGH SEVERITY BUGS ARE FIXED ✅**

---

## MEDIUM SEVERITY BUGS (18)

### Already Fixed in Milestone 11
- M2: History not cleaned ✅
- M3: Book bare except ✅
- M4: Zobrist EP collision ✅
- M5: Shared position unsafe ✅

### Already Fixed in Recent Commits
- M1: Bare except masks ValueError ✅ (fixed with H2)
- M6: Best move not reset ✅ (chess/uci.py:192)
- M7: parse_go edge cases ✅ (chess/uci.py:125-126 has try/except)

### Remaining (Need Investigation)
- **M8:** No error handling for make_move failures
- **M9:** Move ordering improvements (search.py)
- **M10:** Insufficient pruning (search.py)
- **M11:** Evaluation lacks pawn structure (evaluate.py)
- **M12:** Repetition detection (position.py)
- **M13-M18:** Various other issues

---

## LOW SEVERITY BUGS (7)

### Already Fixed
- L1: Best move state not reset ✅ (chess/uci.py:192)

### Remaining (Need Investigation)
- **L2:** parse_go index bounds (fragile but works)
- **L3:** No error handling for make_move (similar to M8)
- **L4:** main_uci.py path setup (works but not robust)
- **L5:** Move history pop() edge case (appears fine)
- **L6:** EN-passant rank validation incomplete (chess/fen.py)
- **L7:** PST symmetry not verified (chess/evaluate.py)

---

## TRULY UNFIXED BUGS - PRIORITY RANKING

### CRITICAL TO FIX (2-3 hours)
1. **M8/L3:** Error handling for make_move failures
   - Location: `chess/uci.py:51-52`
   - Impact: Could crash on corrupted position
   - Fix: Add try/except around make_move

2. **M9:** Move ordering improvements
   - Location: `chess/search.py:45-55`
   - Impact: Search efficiency (not correctness)
   - Fix: Could use killer moves, history heuristics

3. **M10:** Insufficient pruning
   - Location: `chess/search.py:84-140`
   - Impact: Search is slower than needed
   - Fix: Could add iterative deepening with time management (already done?)

### IMPORTANT (4-6 hours)
4. **M11:** Evaluation lacks pawn structure
   - Location: `chess/evaluate.py`
   - Impact: Weaker evaluation, suboptimal move choices
   - Fix: Add pawn structure terms to evaluation

5. **M12:** Repetition detection issues
   - Location: `chess/position.py` (is_threefold_repetition)
   - Impact: Might not handle all repetition cases correctly
   - Fix: Verify implementation

### NICE TO HAVE (3-5 hours)
6. **L4:** Path setup not robust
   - Location: `main_uci.py:6-7`
   - Fix: Use proper package imports

7. **L6:** EN-passant validation
   - Location: `chess/fen.py:49-53`
   - Fix: Add pawn existence check

8. **L7:** PST symmetry
   - Location: `chess/evaluate.py`
   - Fix: Add verification that PST is symmetric

---

## VERIFICATION NEEDED

Before marking bugs as "unfixed", verify:
1. Is the bug actually present in current code?
2. Does it affect correctness or just efficiency?
3. Has it been implicitly fixed by other changes?
4. Is it worth fixing before moving to optimization?

---

## NEXT STEPS

1. Test M8/L3 (make_move error handling)
2. Test M9 (move ordering)
3. Test M10 (pruning)
4. Test M11 (evaluation)
5. Test M12 (repetition detection)
6. Create fixes for truly unfixed bugs only
7. Run perft regression after each fix
8. Move to optimization phase

