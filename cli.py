import chess
import chess.pgn
from search import search

__version__ = '0.2.1-beta'


def print_board(board):
    print(board)


def main():
    print(f"Welcome to the Filajabot {__version__} CLI!")
    print("Input 'FEN' for a FEN string of the current position")
    color = input("Choose your colour (white or black): ").lower()
    if color == "white":
        player_color = chess.WHITE
    else:
        player_color = chess.BLACK

    board = chess.Board()

    while not board.is_game_over():
        if board.turn == player_color:
            print_board(board)
            move = input(">> ")
            if move == "FEN":
                print(board.fen())
                continue
            try:
                board.push_san(move)
            except:
                print("Invalid move. Try again.")
        else:
            print("Searching...")
            result = search(board)
            print(f"Depth: {result.depth} | Score: {result.score}")
            print(f"-- {result.best_move_san}")
            board.push(result.best_move)

    result = board.result()
    print_board(board)

    if result == "1-0" and player_color == chess.WHITE:
        print("You win!")
    elif result == "0-1" and player_color == chess.BLACK:
        print("You win!")
    elif result == "1-0" and player_color == chess.BLACK:
        print("Engine wins!")
    elif result == "0-1" and player_color == chess.WHITE:
        print("Engine wins!")
    else:
        print("It's a draw!")


if __name__ == "__main__":
    main()
