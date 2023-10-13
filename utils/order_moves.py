import chess
from .get_piece_value import get_piece_value


def get_lowest_valued_piece_square(board, squares):
    lowest_value = float('inf')
    lowest_square = None

    for square in squares:
        piece_value = get_piece_value(board.piece_at(square))
        if piece_value < lowest_value:
            lowest_value = piece_value
            lowest_square = square

    return lowest_square


def see(board, square):
    value = 0
    piece = get_lowest_valued_piece_square(board, board.attackers(board.turn, square))

    if piece:
        captured_piece = board.piece_at(square)

        if not captured_piece: return 0  # TODO: Support en passant

        board.push(chess.Move(piece, square))
        value = max(0, get_piece_value(captured_piece) - see(board, square))
        board.pop()

    return value


def see_capture(move, board):
    captured_piece = board.piece_at(move.to_square)

    if captured_piece is None:
        return

    board.push(move)
    value = get_piece_value(captured_piece) - see(board, move.to_square)
    board.pop()

    return value


def score_move(move, board):
    if board.is_capture(move):
        # Use MVV-LVA

        aggressor = board.piece_at(move.from_square)

        if not board.is_en_passant(move):
            victim = board.piece_at(move.to_square)
        else:
            victim = chess.Piece(piece_type=1, color=not board.turn)

        score = get_piece_value(aggressor) - get_piece_value(victim)

        see_score = see_capture(move, board)

        if see_score:
            score += see_score

        return score
    else:
        return 0


def order_moves(board, moves):
    scored_moves = []

    for move in moves:
        scored_moves.append((move, score_move(move, board)))

    sorted_scored_moves = sorted(scored_moves, key=lambda x: x[1], reverse=True)
    scored_moves = [move[0] for move in sorted_scored_moves]

    return scored_moves
