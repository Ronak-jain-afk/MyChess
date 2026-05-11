# BUG FIX IMPLEMENTATION PLAN

**Status:** Building comprehensive bug fix roadmap  
**Total Non-Critical Bugs:** 37 (12 HIGH + 18 MEDIUM + 7 LOW)  
**Already Fixed (Milestone 11):** 8 CRITICAL  
**Already Fixed (Pre-Audit):** H1, H9, H10, H12, L1

---

## QUICK STATUS CHECK

### Already Fixed (No Action Needed)
- ✅ H1: FEN String Parsing (chess/uci.py:23-32)
- ✅ H3: Race Condition (chess/uci.py:180-182)
- ✅ H7: Stop No Output (chess/uci.py:232-241)
- ✅ H8: TT Hash Collision (chess/tt.py) - Milestone 11
- ✅ H9: Move Legality Validation (chess/uci.py:41-52)
- ✅ H10: Same Square Moves (chess/uci.py:67-68)
- ✅ H12: Dead Code (chess/uci.py:165-178)
- ✅ L1: Best Move Reset (chess/uci.py:192)
- ✅ M2: History Cleanup (chess/position.py) - Milestone 11
- ✅ M3: Book Bare Exceptions (chess/book.py) - Milestone 11
- ✅ M4: Zobrist EP Hash (chess/zobrist.py) - Milestone 11
- ✅ M5: Shared Position Safety (chess/uci.py:140,147-153) - Milestone 11

### Still Need Fixing (8 HIGH + remaining MEDIUM + remaining LOW)

---

## PRIORITY 1: HIGH SEVERITY BUGS (8 REMAINING)

### H2: Bare Exception Handling
**File:** `chess/uci.py:70-74`  
**Current:** `except (ValueError, IndexError):`  
**Status:** ✅ ALREADY FIXED

### H4: Invalid Protocol Responses
**File:** `chess/uci.py:219-225`  
**Current Code:**
```python
elif parts[0] == "ucinewgame":
    self.reset()
    # No response expected ✅ FIXED

elif parts[0] == "position":
    self.stop_search()
    self.parse_position(parts[1:])
    # No response expected ✅ FIXED
```
**Status:** ✅ ALREADY FIXED

### H5: Duplicate UCI Identification
**File:** `chess/uci.py:196-215`  
**Current:** Only sends identification on `uci` command (no startup response)  
**Status:** ✅ ALREADY FIXED

### H6: Time Management Not Used
**File:** `chess/uci.py:162-170`  
**Current Code:**
```python
time_limit = self.search_time if self.search_time else None
# ... later ...
if time_limit and time.time() - start_time > time_limit:
    break
```
**Status:** ✅ ALREADY FIXED (iterative deepening with time check)

### H11: Code Quality - Duplicate move_to_uci Logic
**File:** `chess/uci.py:92-97`  
**Current Code:**
```python
def move_to_uci(self, move):
    if move is None:
        return "0000"
    from chess.square import square_to_string
    return square_to_string(move.frm) + square_to_string(move.to) + move.promo_char
```
**Status:** ✅ ALREADY FIXED (uses move.promo_char)

---

## PRIORITY 2: MEDIUM SEVERITY BUGS (remaining)

### M1: Bare except Masks ValueError Details
**File:** `chess/uci.py:70-74`  
**Current:** Uses specific exceptions `(ValueError, IndexError)`  
**Status:** ✅ ALREADY FIXED

### M6: Best Move Not Reset Between Games
**File:** `chess/uci.py:192`  
**Current:** `self.best_move = None` in reset()  
**Status:** ✅ ALREADY FIXED

### M7: parse_go Edge Cases
**File:** `chess/uci.py:109-127`  
**Status:** Has try/except for malformed parameters ✅ ALREADY FIXED

### M8: No Error Handling for make_move Failures
**File:** `chess/uci.py:51-52`  
**Status:** Silently skips illegal moves (acceptable for now)

### M9-M12: Other MEDIUM issues (search.py, evaluate.py, etc.)
**Status:** Need investigation

---

## PRIORITY 3: LOW SEVERITY BUGS (remaining)

### L2-L7: Various low-priority issues
**Status:** Need investigation

---

## SUMMARY

**Out of 37 non-critical bugs, approximately 18-20 have already been fixed!**

### What Still Needs Investigation:
1. M8: Error handling for make_move (may be acceptable as-is)
2. M9-M12: Search/evaluation improvements
3. L2-L7: Low-priority robustness issues

### Next Steps:
1. Create detailed investigation of remaining bugs
2. Create tiny tests for each unfixed bug
3. Implement fixes one by one
4. Run perft regression tests after each fix
5. Integration tests to verify functionality

---

## TESTING STRATEGY

For each remaining bug fix:
1. **Unit Test:** One tiny test file per bug (test_bug_Hx.py, etc.)
2. **Integration Test:** Verify it doesn't break related functionality
3. **Perft Test:** Run if bug touches move generation, make/unmake, or board setup
4. **Verification:** Manual testing with UCI commands

