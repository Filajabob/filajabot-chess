import json


class Constants:
    DEPTH = 5  # Maximum depth
    SEARCH_TIME = 3  # Maximum search time

    class PieceValues:
        # Thanks to https://www.chessprogramming.org/Simplified_Evaluation_Function
        KING = float("inf")
        QUEEN = 9
        ROOK = 5
        BISHOP = 3.3
        KNIGHT = 3.2
        PAWN = 1

        BAD_PAWN = -0.5
        MOBILITY = 0.1

    PIECE_VALUES = {
        "1": PieceValues.PAWN,
        "2": PieceValues.KNIGHT,
        "3": PieceValues.BISHOP,
        "4": PieceValues.ROOK,
        "5": PieceValues.QUEEN,
        "6": PieceValues.KING
    }

    with open("assets/evaluation/piece_value_tables.json", 'r') as f:
        PIECE_VALUE_TABLES = json.load(f)
