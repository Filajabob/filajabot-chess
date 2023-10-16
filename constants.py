class Constants:
    DEPTH = 5  # Maximum depth
    SEARCH_TIME = 3  # Maximum search time

    class PieceValues:
        KING = float("inf")
        QUEEN = 9
        ROOK = 5
        BISHOP = 3.5  # Encourage a bishop pair, making B > N
        # (https://www.chessprogramming.org/Simplified_Evaluation_Function)
        KNIGHT = 3
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

