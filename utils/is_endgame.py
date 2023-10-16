import chess


def is_endgame(board):
    # https://chess.stackexchange.com/a/19319
    # ... End-game is slightly more straight forward, when there are less than 7 minor and major pieces on the board the
    # end-game has begun (so, perhaps 2 rooks and a bishop Vs 2 bishops and a knight). This is not technically where
    # everyone would draw the line, but it's a good indicator that either
    # 1. The end-game has begun
    # 2. The end-game will begin soon.

    pieces = 0
    pawns = 0

    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece is not None:
            piece_type = piece.piece_type
            if piece_type != chess.PAWN:
                pieces += 1
            else:
                pawns += 1

    if pieces < 7:
        return True
    if pawns <= 3:
        return True

    return False
