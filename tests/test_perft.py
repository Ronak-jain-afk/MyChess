import pytest
from chess.position import Position
from chess.perft import perft, PERFT_RESULTS


class TestPerftStart:
    """Test perft from standard starting position."""

    def test_depth_1(self):
        pos = Position()
        result = perft(pos, 1)
        assert result == 20, f"Expected 20, got {result}"

    def test_depth_2(self):
        pos = Position()
        result = perft(pos, 2)
        assert result == 400, f"Expected 400, got {result}"

    def test_depth_3(self):
        pos = Position()
        result = perft(pos, 3)
        assert result == 8916, f"Expected 8916, got {result}"


class TestPerftKiwipete:
    """Test perft from Kiwipete position (castling rights)."""

    def test_depth_1(self):
        pos = Position("r3k2r/pppppppp/8/8/8/8/PPPPPPPP/R3K2R w KQkq - 0 1")
        result = perft(pos, 1)
        assert result == 48, f"Expected 48, got {result}"

    def test_depth_2(self):
        pos = Position("r3k2r/pppppppp/8/8/8/8/PPPPPPPP/R3K2R w KQkq - 0 1")
        result = perft(pos, 2)
        assert result == 2039, f"Expected 2039, got {result}"


class TestPerftRuyLopez:
    """Test perft from Ruy Lopez position."""

    def test_depth_1(self):
        pos = Position("r1bqkbnr/pppp1ppp/2n5/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 0 3")
        result = perft(pos, 1)
        assert result == 24, f"Expected 24, got {result}"

    def test_depth_2(self):
        pos = Position("r1bqkbnr/pppp1ppp/2n5/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 0 3")
        result = perft(pos, 2)
        assert result == 496, f"Expected 496, got {result}"


class TestPerftCheckPosition:
    """Test perft from position with check threat."""

    def test_depth_1(self):
        pos = Position("r1bqk2r/pppp1ppp/2n2n2/2b1p3/2B1P2Q/5N2/PPPP1PPP/RNBQK2R w KQkq - 4 8")
        result = perft(pos, 1)
        assert result == 32, f"Expected 32, got {result}"

    def test_depth_2(self):
        pos = Position("r1bqk2r/pppp1ppp/2n2n2/2b1p3/2B1P2Q/5N2/PPPP1PPP/RNBQK2R w KQkq - 4 8")
        result = perft(pos, 2)
        assert result == 1266, f"Expected 1266, got {result}"


class TestPerftKnownResults:
    """Comprehensive test using PERFT_RESULTS dictionary."""

    @pytest.mark.parametrize("fen,expected", [
        ("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", {1: 20, 2: 400, 3: 8916}),
        ("r1bqkbnr/pppp1ppp/2n5/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 0 3", {1: 24, 2: 496, 3: 9483}),
    ])
    def test_all_depths(self, fen, expected):
        pos = Position(fen)
        for depth, exp in expected.items():
            result = perft(pos, depth)
            assert result == exp, f"FEN: {fen}, depth {depth}: expected {exp}, got {result}"