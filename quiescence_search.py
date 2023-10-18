import chess
from evaluate import evaluate
import utils
from constants import Constants
import utils


def quiescence_search(board, alpha, beta):
    stand_pat = evaluate(board)

    if board.turn is chess.WHITE:
        if stand_pat >= beta:
            return beta

        alpha = max(alpha, stand_pat)

        for capture in [move for move in board.legal_moves
                        if board.is_capture(move) and not utils.see_capture(move, board) < 0]:
            board.push(capture)
            score = quiescence_search(board, alpha, beta)
            board.pop()

            if score >= beta:
                return beta
            if score > alpha:
                alpha = score

        return alpha
    else:
        if stand_pat <= alpha:
            return alpha

        beta = min(beta, stand_pat)

        for capture in [move for move in board.legal_moves
                        if board.is_capture(move) and not utils.see_capture(move, board) < 0]:
            board.push(capture)
            score = quiescence_search(board, alpha, beta)
            board.pop()

            if score <= alpha:
                return alpha
            if score > beta:
                beta = score

        return beta

