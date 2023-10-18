import json
import chess


class Constants:
    DEPTH = 5  # Maximum depth
    SEARCH_TIME = 3  # Maximum search time
    BIG_DELTA = 9.75  # https://www.chessprogramming.org/Delta_Pruning

    class PieceValues:
        # Thanks to https://www.chessprogramming.org/Simplified_Evaluation_Function and
        # https://www.chessprogramming.org/PeSTO%27s_Evaluation_Function
        KING = float("inf")
        QUEEN = 9
        ROOK = 5
        BISHOP = 3.3
        KNIGHT = 3.2
        PAWN = 1

        BAD_PAWN = -0.5
        MOBILITY = 0.1

        # https://www.chessprogramming.org/PeSTO%27s_Evaluation_Function

        class MiddleGame:
            KING = 0
            QUEEN = 10.25
            ROOK = 4.77
            BISHOP = 3.65
            KNIGHT = 3.37
            PAWN = 0.82

        MIDDLE_GAME = {
            "1": MiddleGame.PAWN,
            "2": MiddleGame.KNIGHT,
            "3": MiddleGame.BISHOP,
            "4": MiddleGame.ROOK,
            "5": MiddleGame.QUEEN,
            "6": MiddleGame.KING
        }

        class EndGame:
            KING = 0
            QUEEN = 9.36
            ROOK = 5.12
            BISHOP = 2.97
            KNIGHT = 2.81
            PAWN = 0.94

        END_GAME = {
            "1": EndGame.PAWN,
            "2": EndGame.KNIGHT,
            "3": EndGame.BISHOP,
            "4": EndGame.ROOK,
            "5": EndGame.QUEEN,
            "6": EndGame.KING
        }

    PIECE_VALUES = {
        "1": PieceValues.PAWN,
        "2": PieceValues.KNIGHT,
        "3": PieceValues.BISHOP,
        "4": PieceValues.ROOK,
        "5": PieceValues.QUEEN,
        "6": PieceValues.KING
    }

    # https://www.chessprogramming.org/PeSTO%27s_Evaluation_Function

    with open("assets/evaluation/piece_value_tables.json", 'r') as f:
        PESTO_TABLES = json.load(f)

    # eg. PIECE_TABLES[color][piece][square]
    PIECE_TABLES = {
        chess.WHITE: {
            "mg": {},
            "eg": {}
        },
        chess.BLACK: {
            "mg": {},
            "eg": {}
        }
    }

    # Init piece tables
    for piece in chess.PIECE_TYPES:
        PIECE_TABLES[chess.WHITE]["mg"][str(piece)] = [0] * 64
        PIECE_TABLES[chess.BLACK]["mg"][str(piece)] = [0] * 64

        PIECE_TABLES[chess.WHITE]["eg"][str(piece)] = [0] * 64
        PIECE_TABLES[chess.BLACK]["eg"][str(piece)] = [0] * 64

        for square in chess.SQUARES:
            PIECE_TABLES[chess.WHITE]["mg"][str(piece)][square] = PESTO_TABLES["mg"][str(piece)][square ^ 56] / 100
            PIECE_TABLES[chess.WHITE]["eg"][str(piece)][square] = PESTO_TABLES["eg"][str(piece)][square ^ 56] / 100

            PIECE_TABLES[chess.BLACK]["mg"][str(piece)][square] = PESTO_TABLES["mg"][str(piece)][square] / 100
            PIECE_TABLES[chess.BLACK]["eg"][str(piece)][square] = PESTO_TABLES["eg"][str(piece)][square] / 100

    GAME_PHASE_INC = [0, 1, 1, 2, 4, 0]
