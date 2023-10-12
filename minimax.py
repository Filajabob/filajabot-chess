import chess
from evaluate import evaluate
from result import Result


def maxi(depth, board) -> Result:
    nodes_searched = 0

    if depth == 0:
        return Result(evaluate(board), depth, None, 1)

    max = -float("inf")
    best_move = chess.Move.null()

    for move in board.legal_moves:
        board.push(move)
        result = mini(depth - 1, board)   # Find the opponent's (black's) best move
        board.pop()

        nodes_searched += result.nodes

        if result.score > max:
            max = result.score
            best_move = move

    return Result(max, depth, best_move, nodes_searched)


def mini(depth, board) -> Result:
    nodes_searched = 0

    if depth == 0:
        return Result(evaluate(board), depth, None, 1)

    min = float("inf")
    best_move = chess.Move.null()

    for move in board.legal_moves:
        board.push(move)
        result = maxi(depth - 1, board)
        board.pop()

        nodes_searched += result.nodes

        if result.score < min:
            min = result.score
            best_move = move

    return Result(min, depth, best_move, nodes_searched)
