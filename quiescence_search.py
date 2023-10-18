import chess
from evaluate import evaluate
import utils
from constants import Constants
import utils


def tactical_move(move, board):
    return (board.is_capture(move) and not utils.see_capture(move, board) < 0) \
           or board.gives_check(move) or board.is_check()


def quiescence_search(board, alpha, beta):
    stand_pat = evaluate(board)

    if board.turn is chess.WHITE:
        if stand_pat >= beta:
            return beta

        if not utils.is_endgame(board):
            big_delta = Constants.BIG_DELTA
            if board.peek().promotion:
                big_delta += 7.75

            if stand_pat < alpha - big_delta:
                return alpha

        alpha = max(alpha, stand_pat)

        for capture in [move for move in board.legal_moves if tactical_move(move, board)]:
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

        if not utils.is_endgame(board):
            big_delta = Constants.BIG_DELTA
            if board.peek().promotion:
                big_delta += 7.75

            if stand_pat > beta + big_delta:
                return beta

        beta = min(beta, stand_pat)

        for capture in [move for move in board.legal_moves if tactical_move(move, board)]:
            board.push(capture)
            score = quiescence_search(board, alpha, beta)
            board.pop()

            if score <= alpha:
                return alpha
            if score > beta:
                beta = score

        return beta

