import random
import chess

import logger
from evaluate import evaluate
from result import Result
import utils
from quiescence_search import quiescence_search
from transposition_table import TranspositionTable
from constants import Constants

tt = TranspositionTable()


def maxi(depth, board, alpha, beta, root_dist, zobrist_hash=None, *, best_move=None) -> Result:
    if not zobrist_hash:
        zobrist_hash = tt.zobrist_array.positional_hash(board)

    nodes_searched = 0

    entry = tt.probe(zobrist_hash)
    if entry:
        if entry.depth >= depth and entry.best_move:
            return entry.result()

    if depth == 0 or board.outcome():
        result = Result(quiescence_search(board, alpha, beta), depth, None, 1)

        return result

    b_search_pv = True

    ordered_moves = utils.order_moves(board, board.legal_moves, best_move)
    best_move = ordered_moves[0]  # just in case

    for move in ordered_moves:
        zobrist_hash = tt.zobrist_array.push(zobrist_hash, move, board)
        board.push(move)
        if b_search_pv:
            result = mini(depth - 1, board, alpha, beta, root_dist + 1, zobrist_hash)   # Find the opponent's (black's)
        else:
            result = mini(depth - 1, board, alpha, alpha + 1, root_dist + 1, zobrist_hash)
            if result.score > alpha:
                result = mini(depth - 1, board, alpha, beta, root_dist + 1, zobrist_hash)  # re-search

        # best move
        board.pop()
        zobrist_hash = tt.zobrist_array.pop(zobrist_hash, move, board)

        nodes_searched += result.nodes

        # Mate Distance Pruning

        if result.score == Constants.SCORE_MATE:
            result.score -= 1

            mating_value = Constants.SCORE_MATE - root_dist

            if mating_value < beta:
                beta = mating_value
                if alpha >= mating_value:
                    return Result(mating_value, depth, best_move)

        elif result.score == -Constants.SCORE_MATE:
            result.score += 1

            mating_value = -Constants.SCORE_MATE + root_dist

            if mating_value > alpha:
                alpha = mating_value
                if beta <= mating_value:
                    return Result(mating_value, depth, best_move)

        if result.score >= beta:
            best_move = move
            result = Result(beta, depth, best_move, nodes_searched)
            tt.generate_add_entry(result, board, alpha, beta, zobrist_hash)

            return result  # fail hard beta-cutoff
        if result.score > alpha:
            alpha = result.score
            best_move = move
            b_search_pv = False

    result = Result(alpha, depth, best_move, nodes_searched)
    tt.generate_add_entry(result, board, alpha, beta, zobrist_hash)
    return result


def mini(depth, board, alpha, beta, root_dist, zobrist_hash=None, *, best_move=None) -> Result:
    if not zobrist_hash:
        zobrist_hash = tt.zobrist_array.positional_hash(board)

    nodes_searched = 0

    entry = tt.probe(zobrist_hash)
    if entry:
        if entry.depth >= depth and entry.best_move:
            return entry.result()

    if depth == 0 or board.outcome():
        result = Result(quiescence_search(board, alpha, beta), depth, None, 1)
        return result

    b_search_pv = True

    ordered_moves = utils.order_moves(board, board.legal_moves, best_move)
    best_move = ordered_moves[0]  # just in case
    for move in ordered_moves:
        zobrist_hash = tt.zobrist_array.push(zobrist_hash, move, board)
        board.push(move)

        if b_search_pv:
            result = maxi(depth - 1, board, alpha, beta, root_dist + 1, zobrist_hash)
        else:
            result = maxi(depth - 1, board, beta - 1, beta, root_dist + 1, zobrist_hash)
            if result.score < beta:
                result = maxi(depth - 1, board, alpha, beta, root_dist + 1, zobrist_hash)  # re-search

        board.pop()
        zobrist_hash = tt.zobrist_array.pop(zobrist_hash, move, board)

        nodes_searched += result.nodes

        if result.score == Constants.SCORE_MATE:
            result.score -= 1

            mating_value = Constants.SCORE_MATE - root_dist

            if mating_value < beta:
                beta = mating_value
                if alpha >= mating_value:
                    return Result(mating_value, depth, best_move)

        elif result.score == -Constants.SCORE_MATE:
            result.score += 1

            mating_value = -Constants.SCORE_MATE + root_dist

            if mating_value > alpha:
                alpha = mating_value
                if beta <= mating_value:
                    return Result(mating_value, depth, best_move)

        if result.score <= alpha:
            best_move = move
            result = Result(alpha, depth, best_move, nodes_searched)
            tt.generate_add_entry(result, board, alpha, beta, zobrist_hash)

            return result  # fail hard beta-cutoff
        if result.score < beta:
            beta = result.score
            best_move = move
            b_search_pv = False

    result = Result(beta, depth, best_move, nodes_searched)
    tt.generate_add_entry(result, board, alpha, beta, zobrist_hash)
    return result
