import random
import time
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

    with chess.polyglot.open_reader("assets/book/opening_book.bin") as reader:
        try:
            return random.choice(list(reader.find_all(board))).move
        except IndexError:
            return None


def search(board) -> Result:
    """
    Conducts a depth-first minimax search of a board.
    :param board: The board to search.
    :return: A result.Result containing score, depth, and best move.
    """

    book = opening_book(board)

    if book:
        return Result(Result.BOOK, Constants.DEPTH, book, None, best_move_san=board.san(book))

    start_time = time.time()

    # Engine is white
    if board.turn == chess.WHITE:
        result = maxi(Constants.DEPTH, board)
    else:
        result = mini(Constants.DEPTH, board)

    elapsed_time = time.time() - start_time

    filajabot_logger.info(f"Search completed at {board.fen()} at depth {Constants.DEPTH}\n"
                f"Best move: {result.best_move}\n"
                f"Nodes searched: {result.nodes}\n"
                f"Elapsed time: {elapsed_time}\n"
                f"Seconds per node: {result.nodes / elapsed_time}")

    return Result(result.score, Constants.DEPTH, result.best_move, None, best_move_san=board.san(result.best_move))
