import sys
import threading
import time
from chess.position import Position, PositionState
from chess import search
from chess.move import Move, move_from_string

class UCIController:
    def __init__(self):
        self.position = Position()
        self.search_position = None  # Snapshot for search thread
        self.search_thread = None
        self.stop_event = threading.Event()
        self.best_move = None
        self.score = 0
        self.depth = 3
        self.infinite = False

    def parse_position(self, args):
        if args[0] == "startpos":
            self.position = Position()
            moves_start = 1
        elif args[0] == "fen":
            # FEN is 6 parts, need to join them
            try:
                moves_idx = args.index("moves")
                fen = " ".join(args[1:moves_idx])
            except ValueError:
                fen = " ".join(args[1:])
                moves_idx = len(args)
            self.position = Position(fen)
            moves_start = moves_idx
        else:
            return

        # Apply moves if present
        if len(args) > moves_start and args[moves_start] == "moves":
            for move_str in args[moves_start + 1:]:
                move = self.move_from_uci(move_str)
                if move:
                    # Validate move is legal before making it
                    legal_moves = self.position.generate_legal_moves()
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
                        # Silently skip illegal moves in production
                        import sys
                        if sys.flags.debug:
                            print(f"DEBUG: Skipped illegal move {move_str}", file=sys.stderr)

    def move_from_uci(self, uci_str):
        from chess.square import square_from_string
        from chess.move import Move, FLAG_PROMO_QUEEN, FLAG_PROMO_ROOK, FLAG_PROMO_BISHOP, FLAG_PROMO_KNIGHT

        if len(uci_str) < 4:
            return None

        # Validate same square (from == to)
        if uci_str[:2] == uci_str[2:4]:
            return None

        try:
            from_sq = square_from_string(uci_str[:2])
            to_sq = square_from_string(uci_str[2:4])
        except (ValueError, IndexError):
            return None

        flags = 0
        if len(uci_str) == 5:
            promo = uci_str[4].lower()
            if promo == 'q':
                flags = FLAG_PROMO_QUEEN
            elif promo == 'r':
                flags = FLAG_PROMO_ROOK
            elif promo == 'b':
                flags = FLAG_PROMO_BISHOP
            elif promo == 'n':
                flags = FLAG_PROMO_KNIGHT
            else:
                return None  # Invalid promotion piece

        return Move(from_sq, to_sq, flags)

    def move_to_uci(self, move):
        if move is None:
            return "0000"

        from chess.square import square_to_string
        return square_to_string(move.frm) + square_to_string(move.to) + move.promo_char

    def parse_go(self, args):
        wtime = None
        btime = None
        winc = 0
        binc = 0
        self.depth = 3
        nodes = None
        self.infinite = False

        i = 0
        while i < len(args):
            try:
                if args[i] == "wtime" and i + 1 < len(args):
                    wtime = int(args[i + 1])
                elif args[i] == "btime" and i + 1 < len(args):
                    btime = int(args[i + 1])
                elif args[i] == "winc" and i + 1 < len(args):
                    winc = int(args[i + 1])
                elif args[i] == "binc" and i + 1 < len(args):
                    binc = int(args[i + 1])
                elif args[i] == "depth" and i + 1 < len(args):
                    self.depth = int(args[i + 1])
                elif args[i] == "nodes" and i + 1 < len(args):
                    nodes = int(args[i + 1])
                elif args[i] == "infinite":
                    self.infinite = True
            except (ValueError, IndexError):
                pass  # Silently skip malformed parameters
            i += 1

        if not self.infinite and wtime is not None and btime is not None:
            if self.position.side_to_move[0] == 0:
                time_limit = wtime // 20 + winc
            else:
                time_limit = btime // 20 + binc
            self.search_time = time_limit / 1000.0
        else:
            self.search_time = None

        self.stop_event.clear()
        # Create snapshot of position before search thread starts
        self.search_position = PositionState(self.position)
        self.search_thread = threading.Thread(target=self.search_worker)
        self.search_thread.start()

    def search_worker(self):
        """Search worker with time management and iterative deepening."""
        # Reconstruct position from snapshot to avoid race conditions
        pos = Position()
        pos.board = self.search_position.board.copy()
        pos.side_to_move[0] = self.search_position.side_to_move
        pos.castle_rights[0] = self.search_position.castle_rights
        pos.ep_square[0] = self.search_position.ep_square
        pos.halfmove_clock[0] = self.search_position.halfmove_clock
        pos.fullmove_number[0] = self.search_position.fullmove_number
        
        # CRITICAL: Restore history for proper legal move generation
        pos.history.keys = self.search_position.history_keys.copy()
        pos.history.reversible = self.search_position.history_reversible.copy()
        pos.history.moves = self.search_position.history_moves.copy()
        pos.history.last_from_sq = self.search_position.history_last_from_sq
        pos.history.last_to_sq = self.search_position.history_last_to_sq
        
        # Validate that we can generate legal moves (sanity check)
        try:
            legal_moves = pos.generate_legal_moves()
            if not legal_moves:
                # Position is checkmate or stalemate
                print(f"bestmove 0000")  # Null move if no legal moves
                sys.stdout.flush()
                return
        except Exception as e:
            # Position reconstruction failed - shouldn't happen
            print(f"bestmove 0000")
            sys.stdout.flush()
            return
        
        start_time = time.time()

        if self.infinite:
            max_depth = 100
        else:
            max_depth = self.depth

        time_limit = self.search_time if self.search_time else None
        previous_best = None

        for d in range(1, max_depth + 1):
            if self.stop_event.is_set():
                break

            if time_limit and time.time() - start_time > time_limit:
                break

            self.best_move, self.score = search.negamax_root(pos, d, previous_best)

            if self.best_move:
                previous_best = self.best_move

            if search.is_checkmate(self.score):
                break

        # Validate best_move is actually legal before outputting
        if self.best_move:
            legal = pos.generate_legal_moves()
            is_legal = any(m.frm == self.best_move.frm and m.to == self.best_move.to for m in legal)
            if not is_legal:
                # Fallback to first legal move if search returned illegal
                if legal:
                    self.best_move = legal[0]
                else:
                    self.best_move = None
        
        # Always print bestmove exactly once (no race condition)
        move_uci = self.move_to_uci(self.best_move) if self.best_move else "0000"
        print(f"bestmove {move_uci}")
        sys.stdout.flush()

    def stop_search(self):
        if self.search_thread and self.search_thread.is_alive():
            self.stop_event.set()
            self.search_thread.join()

    def reset(self):
        self.stop_search()
        self.position = Position()
        self.best_move = None
        self.score = 0
        search.clear_tt()

    def run(self):
        """Main UCI command loop - don't send anything until 'uci' command."""
        while True:
            line = sys.stdin.readline()
            if not line:
                break

            line = line.strip()
            if not line:
                continue

            parts = line.split()
            if not parts:
                continue

            if parts[0] == "uci":
                print("id name OpenCodeChess")
                print("id author Developer")
                print("uciok")
                sys.stdout.flush()
            elif parts[0] == "isready":
                print("readyok")
                sys.stdout.flush()
            elif parts[0] == "ucinewgame":
                self.reset()
                # No response expected
            elif parts[0] == "position":
                self.stop_search()
                self.parse_position(parts[1:])
                # No response expected
            elif parts[0] == "go":
                self.parse_go(parts[1:])
                # Response comes from search_worker
            elif parts[0] == "stop":
                self.stop_search()
                # Ensure we always output bestmove
                if self.best_move is None:
                    legal_moves = self.position.generate_legal_moves()
                    if legal_moves:
                        self.best_move = legal_moves[0]
                
                if self.best_move:
                    print(f"bestmove {self.move_to_uci(self.best_move)}")
                else:
                    print("bestmove 0000")  # Null move if no legal moves
                sys.stdout.flush()
            elif parts[0] == "quit":
                self.stop_search()
                break


def uci_loop():
    controller = UCIController()
    controller.run()


if __name__ == "__main__":
    uci_loop()