import chess
from .get_piece_value import get_piece_value
from .see import see, see_capture


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
