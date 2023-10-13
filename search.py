"""
Run this file directly while passing a FEN string to get a result.Result
"""

import random
import time
import sys
import chess
import chess.polyglot
from minimax import mini, maxi
from constants import Constants
from logger import filajabot_logger
from result import Result


def opening_book(board) -> chess.Move:
    """
    Probes an opening book and returns a random opening move.
    :param board: The board to do the book move on.
    :return: A chess.Move
    """

    reader = chess.polyglot.MemoryMappedReader("assets/book/opening_book.bin")
    return reader.choice(board).move


def search(board, *, log=True, max_depth=Constants.DEPTH, max_time=Constants.SEARCH_TIME) -> Result:
    """
    Conducts an iterative-deepening minimax search of a board.
    :param max_time:
    :param max_depth:
    :param log: bool: Whether to log
    :param board: The board to search.
    :return: A result.Result containing score, depth, and best move.
    """

    book = opening_book(board)

    if book:
        return Result(Result.BOOK, Constants.DEPTH, book, None, best_move_san=board.san(book))

    start_time = time.time()

    for depth in range(1, max_depth):
        # Engine is white
        if board.turn == chess.WHITE:
            result = maxi(depth, board, float("-inf"), float("inf"))
        else:
            result = mini(depth, board, float("-inf"), float("inf"))

        elapsed_time = time.time() - start_time

        if log:
            filajabot_logger.debug(f"Best move found in {round(elapsed_time, 2)} seconds at {board.fen()} on depth "
                                   f"{depth}: {result.best_move}")

        if elapsed_time > max_time:
            break

    if log:
        filajabot_logger.info(f"Search completed at {board.fen()} at depth {max_depth}\n"
                              f"\tBest move: {result.best_move}\n"
                              f"\tNodes searched: {result.nodes}\n"
                              f"\tElapsed time: {elapsed_time}\n"
                              f"\tTime per 100 nodes: {elapsed_time / result.nodes * 100}")

    return Result(result.score, max_depth, result.best_move, None, best_move_san=board.san(result.best_move))


if __name__ == '__main__':
    # search.exe [FEN] [max_time]
    board = chess.Board(fen=sys.argv[1])
    result = search(board, log=False, max_time=sys.argv[2])

    sys.stdout.write(result.best_move_san)
    sys.stdout.flush()
