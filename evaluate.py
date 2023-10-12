import chess
from constants import Constants
from result import Result


def evaluate(board) -> float:
    outcome = board.outcome()
    if outcome:
        # If the game is over, return inf/-inf or 0
        if outcome.result() in ["1-0", "0-1", "1/2-1/2"]:
            if outcome.result() == "1-0":
                return float("inf")
            elif outcome.result() == "0-1":
                return float("-inf")
            elif outcome.result() == "1/2-1/2":
                return 0.0
    else:
        # If the game is not over, evaluate material
        white = board.occupied_co[chess.WHITE]
        black = board.occupied_co[chess.BLACK]

        material_score = (
                Constants.PieceValues.PAWN * chess.popcount(white & board.pawns) - chess.popcount(black & board.pawns) +
                Constants.PieceValues.KNIGHT * (chess.popcount(white & board.knights) - chess.popcount(black & board.knights)) +
                Constants.PieceValues.BISHOP * (chess.popcount(white & board.bishops) - chess.popcount(black & board.bishops)) +
                Constants.PieceValues.ROOK * (chess.popcount(white & board.rooks) - chess.popcount(black & board.rooks)) +
                Constants.PieceValues.QUEEN * (chess.popcount(white & board.queens) - chess.popcount(black & board.queens))
        )
        if board.turn == chess.WHITE:
            white_mobility = board.legal_moves.count()
            board.push(chess.Move.null())
            black_mobility = board.legal_moves.count()
            board.pop()
        else:
            black_mobility = board.legal_moves.count()
            board.push(chess.Move.null())
            white_mobility = board.legal_moves.count()
            board.pop()

        mobility_score = Constants.PieceValues.MOBILITY * (white_mobility - black_mobility)

        return material_score + mobility_score
