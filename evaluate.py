import chess
from constants import Constants
import utils


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
        # https://www.chessprogramming.org/PeSTO%27s_Evaluation_Function

        game_phase = 0

        mg_score = 0
        eg_score = 0

        # If the game is not over, evaluate material / piece value table
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece is not None:
                if piece.color is chess.WHITE:
                    mg_score += Constants.PieceValues.MIDDLE_GAME[str(piece.piece_type)] + \
                                Constants.PIECE_TABLES[piece.color]["mg"][str(piece.piece_type)][square]

                    eg_score += Constants.PieceValues.END_GAME[str(piece.piece_type)] + \
                                Constants.PIECE_TABLES[piece.color]["eg"][str(piece.piece_type)][square]
                else:
                    mg_score -= Constants.PieceValues.MIDDLE_GAME[str(piece.piece_type)] + \
                                Constants.PIECE_TABLES[piece.color]["mg"][str(piece.piece_type)][square]

                    eg_score -= Constants.PieceValues.END_GAME[str(piece.piece_type)] + \
                                Constants.PIECE_TABLES[piece.color]["eg"][str(piece.piece_type)][square]

                game_phase += Constants.GAME_PHASE_INC[piece.piece_type - 1]

        # tapered eval
        mg_phase = max(game_phase, 24)  # in case of early promotion
        eg_phase = 24 - mg_phase

        return (mg_score * mg_phase + eg_score * eg_phase) / 24
