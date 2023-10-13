import random
import chess
from evaluate import evaluate
from result import Result


def maxi(depth, board, alpha, beta) -> Result:
    nodes_searched = 0

    if depth == 0:
        return Result(evaluate(board), depth, None, 1)

    best_move = chess.Move.null()

    for move in board.legal_moves:
        board.push(move)
        result = mini(depth - 1, board, alpha, beta)   # Find the opponent's (black's) best move
        board.pop()

        nodes_searched += result.nodes

        if result.score >= beta:
            best_move = move
            return Result(beta, depth, best_move, nodes_searched)  # fail hard beta-cutoff
        if result.score > alpha:
            alpha = result.score
            best_move = move

    return Result(alpha, depth, best_move, nodes_searched)


def mini(depth, board, alpha, beta) -> Result:
    nodes_searched = 0

    if depth == 0:
        return Result(evaluate(board), depth, None, 1)

    best_move = chess.Move.null()

    for move in board.legal_moves:
        board.push(move)
        result = maxi(depth - 1, board, alpha, beta)
        board.pop()

        nodes_searched += result.nodes

        if result.score <= alpha:
            best_move = move
            return Result(alpha, depth, best_move, nodes_searched)  # fail hard alpha-cutoff
        if result.score < beta:
            beta = result.score
            best_move = move

    return Result(beta, depth, best_move, nodes_searched)
