class Constants:
    DEPTH = 3

    class PieceValues:
        KING = float("inf")
        QUEEN = 9
        ROOK = 5
        BISHOP = 3
        KNIGHT = 3
        PAWN = 1

        BAD_PAWN = -0.5
        MOBILITY = 0.1
