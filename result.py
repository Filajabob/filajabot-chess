import chess


class Result:
    def __init__(self, score: float, depth: int, best_move: chess.Move=None, nodes: int=0, *, best_move_san: str=None,
                 mate_in: int=None, elapsed_time: float=None, engine_resign=False):
        """
        The result of a minimax search.
        :param score: float: The score of the position, positive being good for white, and vice versa.
        :param depth: int: The depth of the search
        :param best_move: The best move for the player to move found by the search
        :param nodes: The amount of nodes searched
        :param best_move_san: The best move, in SAN format
        :param mate_in: The shortest amount of half-moves until checkmate, for the player that the score is in favor for
        """
        self.score = score
        self.depth = depth
        self.best_move = best_move
        self.nodes = nodes
        self.best_move_san = best_move_san
        self.mate_in = mate_in
        self.elapsed_time = elapsed_time
        self.engine_resign = engine_resign

    BOOK = None
    TABLEBASE = None
    DRAW = 0
    WHITE_CHECKMATE = float("inf")
    BLACK_CHECKMATE = float("-inf")
