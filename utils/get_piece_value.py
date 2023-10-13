from constants import Constants


def get_piece_value(piece):
    if piece is None:
        return

    return Constants.PIECE_VALUES[str(piece.piece_type)]
