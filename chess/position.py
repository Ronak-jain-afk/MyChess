from chess.constants import EMPTY, wP, bP, wN, bN, wB, bB, Color, CASTLE_WK, CASTLE_WQ, CASTLE_BK, CASTLE_BQ
import chess.zobrist as zobrist
from chess.history import PositionHistory
from chess.fen import set_fen, get_fen, STARTING_FEN
from chess.square import file_of, rank_of, square

class Position:
    def __init__(self, fen: str = STARTING_FEN):
        self.board = [EMPTY] * 64
        self.side_to_move = [0]
        self.castle_rights = [CASTLE_WK | CASTLE_WQ | CASTLE_BK | CASTLE_BQ]
        self.ep_square = [-1]
        self.halfmove_clock = [0]
        self.fullmove_number = [1]
        self.history = PositionHistory()

        set_fen(fen, self.board, self.side_to_move, self.castle_rights,
                self.ep_square, self.halfmove_clock, self.fullmove_number)

    @property
    def key(self) -> int:
        return zobrist.compute_key(
            self.board,
            self.side_to_move[0],
            self.castle_rights[0],
            self.ep_square[0]
        )

    def is_reversible(self) -> bool:
        """Check if the last move was reversible (not a pawn move or capture)."""
        if len(self.history.keys) == 0:
            return True  # No moves made yet, position is reversible
        
        # Get the last move info
        from_sq = self.history.last_from_sq
        to_sq = self.history.last_to_sq
        
        if from_sq < 0 or to_sq < 0:
            return True  # Invalid move info
        
        # Get the piece that was moved (we need to look at current board state)
        # Since the move was already made, we need to check the state
        # Actually, we should check the history of what was captured and what piece moved
        # For now, we rely on the reversible flag in history
        if len(self.history.reversible) > 0:
            return self.history.reversible[-1]
        
        return True

    def is_threefold_repetition(self) -> bool:
        return self.history.is_threefold(self.key)

    def has_insufficient_material(self) -> bool:
        """Check if position has insufficient material to checkmate."""
        pieces = [p for p in self.board if p != EMPTY]
        white_pieces = [p for p in pieces if 1 <= p <= 6]
        black_pieces = [p for p in pieces if 7 <= p <= 12]

        # King vs King
        if len(white_pieces) == 1 and len(black_pieces) == 1:
            return True
        
        # King + Knight vs King
        if len(white_pieces) == 2 and len(black_pieces) == 1:
            if any(p == wN for p in white_pieces):  # wN = 2
                return True
        if len(white_pieces) == 1 and len(black_pieces) == 2:
            if any(p == bN for p in black_pieces):  # bN = 8
                return True
        
        # King + Bishop vs King
        if len(white_pieces) == 2 and len(black_pieces) == 1:
            if any(p == wB for p in white_pieces):  # wB = 3
                return True
        if len(white_pieces) == 1 and len(black_pieces) == 2:
            if any(p == bB for p in black_pieces):  # bB = 9
                return True
        
        return False

    def __str__(self):
        lines = []
        for rank in range(7, -1, -1):
            line = []
            for file in range(8):
                sq = rank * 8 + file
                piece = self.board[sq]
                if piece == EMPTY:
                    line.append('.')
                else:
                    from chess.constants import PIECE_TO_CHAR
                    line.append(PIECE_TO_CHAR.get(piece, '?'))
            lines.append(' '.join(line))
        return '\n'.join(lines)

    def __repr__(self):
        return f"Position('{self.fen()}')"

    def fen(self) -> str:
        return get_fen(self.board, self.side_to_move, self.castle_rights,
                       self.ep_square, self.halfmove_clock, self.fullmove_number)

    def generate_pseudo_legal_moves(self):
        import chess.moves as moves
        return moves.generate_pseudo_legal_moves(self)

    def is_check(self, color):
        import chess.moves as moves
        return moves.is_in_check(self, color)

    def generate_legal_moves(self):
        import chess.moves as moves
        pseudo = moves.generate_pseudo_legal_moves(self)
        legal = []
        for move in pseudo:
            color = Color.WHITE if self.side_to_move[0] == 0 else Color.BLACK
            state = self.make_move(move)
            # After move, side_to_move flips - check the side that just moved
            if not self.is_check(color):
                legal.append(move)
            self.unmake_move(state, move)
        return legal

    def make_move(self, move):
        from chess.move import MoveState
        from chess.constants import wP, bP, wK, bK, wR, bR

        color = Color.WHITE if self.side_to_move[0] == 0 else Color.BLACK

        state = MoveState(
            captured=self.board[move.to],
            promoted=0,
            old_ep=self.ep_square[0],
            old_castle=self.castle_rights[0],
            old_halfmove=self.halfmove_clock[0],
            old_fullmove=self.fullmove_number[0],
            from_piece=self.board[move.frm]
        )

        if move.is_promotion:
            state.promoted = self.board[move.to]
            self.board[move.to] = move.get_promotion_piece(self.side_to_move[0])
            self.board[move.frm] = EMPTY
        elif move.is_en_passant:
            # En passant: white captures down (pawns move north), black captures up (pawns move south)
            capture_sq = move.to - 8 if color == Color.WHITE else move.to + 8
            state.captured = self.board[capture_sq]
            self.board[capture_sq] = EMPTY
            self.board[move.to] = self.board[move.frm]
            self.board[move.frm] = EMPTY
        elif move.is_castle:
            self.board[move.to] = self.board[move.frm]
            self.board[move.frm] = EMPTY
            if move.to > move.frm:
                self.board[move.to - 1] = self.board[move.to + 1]
                self.board[move.to + 1] = EMPTY
            else:
                self.board[move.to + 1] = self.board[move.to - 2]
                self.board[move.to - 2] = EMPTY
        else:
            self.board[move.to] = self.board[move.frm]
            self.board[move.frm] = EMPTY

        self.ep_square[0] = -1

        from_piece = state.from_piece
        if from_piece in (wP, bP) and abs(move.to - move.frm) == 16:
            self.ep_square[0] = (move.to + move.frm) // 2

        if from_piece == wK:
            self.castle_rights[0] &= ~(CASTLE_WK | CASTLE_WQ)
        elif from_piece == bK:
            self.castle_rights[0] &= ~(CASTLE_BK | CASTLE_BQ)
        elif from_piece == wR:
            if move.frm == 0:
                self.castle_rights[0] &= ~CASTLE_WQ
            elif move.frm == 7:
                self.castle_rights[0] &= ~CASTLE_WK
        elif from_piece == bR:
            if move.frm == 56:
                self.castle_rights[0] &= ~CASTLE_BQ
            elif move.frm == 63:
                self.castle_rights[0] &= ~CASTLE_BK

        if move.to == 0:
            self.castle_rights[0] &= ~CASTLE_WQ
        elif move.to == 7:
            self.castle_rights[0] &= ~CASTLE_WK
        elif move.to == 56:
            self.castle_rights[0] &= ~CASTLE_BQ
        elif move.to == 63:
            self.castle_rights[0] &= ~CASTLE_BK

        if from_piece in (wP, bP) or state.captured != EMPTY:
            self.halfmove_clock[0] = 0
        else:
            self.halfmove_clock[0] += 1

        self.side_to_move[0] = 1 - self.side_to_move[0]

        if self.side_to_move[0] == 0:
            self.fullmove_number[0] += 1

        reversible = not (from_piece in (wP, bP) or state.captured != EMPTY)
        self.history.push(self.key, reversible, move.frm, move.to)

        return state

    def unmake_move(self, state, move):
        from chess.constants import wP, bP

        # Determine color of moving side (it's already flipped, so use opposite)
        color = Color.BLACK if self.side_to_move[0] == 0 else Color.WHITE

        if move.is_en_passant:
            # Calculate captured pawn square based on moving color
            if color == Color.WHITE:
                capture_sq = move.to - 8  # Captured pawn is 8 squares back
            else:
                capture_sq = move.to + 8  # Captured pawn is 8 squares forward
            self.board[move.frm] = state.from_piece
            self.board[move.to] = EMPTY
            self.board[capture_sq] = state.captured
        elif move.is_castle:
            self.board[move.frm] = state.from_piece
            self.board[move.to] = EMPTY
            if move.to > move.frm:
                self.board[move.to + 1] = self.board[move.to - 1]
                self.board[move.to - 1] = EMPTY
            else:
                self.board[move.to - 2] = self.board[move.to + 1]
                self.board[move.to + 1] = EMPTY
        elif move.is_promotion:
            self.board[move.frm] = wP if state.from_piece <= 6 else bP
            self.board[move.to] = state.captured
        else:
            self.board[move.frm] = state.from_piece
            self.board[move.to] = state.captured

        self.ep_square[0] = state.old_ep
        self.castle_rights[0] = state.old_castle
        self.halfmove_clock[0] = state.old_halfmove
        self.fullmove_number[0] = state.old_fullmove
        self.side_to_move[0] = 1 - self.side_to_move[0]

    def push(self, move):
        return self.make_move(move)

    def pop(self, state, move):
        self.unmake_move(state, move)


class PositionState:
    def __init__(self, pos: Position):
        self.board = pos.board.copy()
        self.side_to_move = pos.side_to_move[0]
        self.castle_rights = pos.castle_rights[0]
        self.ep_square = pos.ep_square[0]
        self.halfmove_clock = pos.halfmove_clock[0]
        self.fullmove_number = pos.fullmove_number[0]
        self.key = pos.key
