"""
Run this file directly while passing a FEN string to get a result.Result
"""

import time
import asyncio
import sys
import multiprocessing as mp
import chess
import chess.polyglot
import requests
from minimax import mini, maxi
from constants import Constants
from logger import filajabot_logger
from result import Result

try:
    import pygame
except ImportError:
    print("WARNING: PyGame is not installed. Ignore if you do not use the GUI.")


def opening_book(board) -> chess.Move:
    """
    Probes an opening book and returns a random opening move.
    :param board: The board to do the book move on.
    :return: A chess.Move
    """

    reader = chess.polyglot.MemoryMappedReader("assets/book/opening_book.bin")

    try:
        return reader.choice(board).move
    except IndexError:
        return


def iterative_deepening(board, max_time, max_depth, log=True):
    result = Result(None, 0, None)
    start_time = time.time()

    for depth in range(1, max_depth):
        # Engine is white
        if board.turn == chess.WHITE:
            result = maxi(depth, board, float("-inf"), float("inf"), 1, best_move=result.best_move)
        else:
            result = mini(depth, board, float("-inf"), float("inf"), 1, best_move=result.best_move)

        elapsed_time = time.time() - start_time

        if log:
            filajabot_logger.debug(f"Best move found in {round(elapsed_time, 2)} seconds at {board.fen()} on depth "
                                   f"{depth}: {result.best_move}")

        if elapsed_time > max_time:
            return result


def search(board, *, log=True, max_depth=Constants.DEPTH, max_time=Constants.SEARCH_TIME, use_pygame_sleep=False) -> Result:
    """
    Conducts an iterative-deepening minimax search of a board, also including opening/endgame probing.
    :param use_pygame_sleep:
    :param max_time:
    :param max_depth:
    :param log: bool: Whether to log
    :param board: The board to search.
    :return: A result.Result containing score, depth, and best move.
    """

    book = opening_book(board)

    if book:
        return Result(Result.BOOK, Result.BOOK, book, None, best_move_san=board.san(book))
    if sum([1 for square in chess.SQUARES if board.piece_at(square) is not None]) <= 7:
        # probe tablebase
        try:
            r = requests.get(url=f"http://tablebase.lichess.ovh/standard/mainline?fen={board.fen()}")
            entry = r.json()

            if chess.Move.from_uci(entry[0]["uci"]) in board.legal_moves:
                return Result(Result.TABLEBASE, Result.BOOK, chess.Move.from_uci(entry[0]["uci"]))
        except:
            pass

    result = iterative_deepening(board, max_time, max_depth, log)

    if result.best_move is None:
        if log:
            filajabot_logger.debug(f"Engine resigned at {board.fen()} with score {result.score}")
        return Result(result.score, max_depth, result.best_move, None, best_move_san=board.san(result.best_move),
                      engine_resign=True)

    if log:
        if result.nodes == 0:
            filajabot_logger.info(f"Search completed at {board.fen()} at depth {result.depth}\n"
                                  f"\tBest move: {result.best_move}\n"
                                  f"\tScore: {result.score}"
                                  f"\tNodes searched: {result.nodes}\n"
                                  f"\tElapsed time: {elapsed_time}\n"
                                  f"\tTime per 100 nodes: N/A")
        else:
            filajabot_logger.info(f"Search completed at {board.fen()} at depth {result.depth}\n"
                                  f"\tBest move: {result.best_move}\n"
                                  f"\tScore: {result.score}"
                                  f"\tNodes searched: {result.nodes}\n"
                                  f"\tElapsed time: {elapsed_time}\n"
                                  f"\tTime per 100 nodes: {elapsed_time / result.nodes * 100}")

    mate_in = None
    if result.score > Constants.SCORE_MATE - Constants.DEEPEST_MATE \
            or result.score < -Constants.SCORE_MATE + Constants.DEEPEST_MATE:
        mate_in = Constants.SCORE_MATE - result.score

    return Result(result.score, result.depth, result.best_move, None, best_move_san=board.san(result.best_move),
                  mate_in=mate_in)


if __name__ == '__main__':
    # version010.exe [FEN] [max_time]
    board = chess.Board(fen=sys.argv[1])
    result = search(board, log=False, max_time=float(sys.argv[2]))

    sys.stdout.write(result.best_move_san)
    sys.stdout.flush()
