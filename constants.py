class Constants:
    DEPTH = 5  # Maximum depth
    SEARCH_TIME = 3  # Maximum search time

    class PieceValues:
        KING = float("inf")
        QUEEN = 9
        ROOK = 5
        BISHOP = 3
        KNIGHT = 3
        PAWN = 1

        BAD_PAWN = -0.5
        MOBILITY = 0.1
