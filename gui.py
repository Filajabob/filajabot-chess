"""
Thanks to https://blog.devgenius.io/simple-interactive-chess-gui-in-python-c6d6569f7b6c for all the code
"""
import time
import threading

import pygame
import chess
import math

import utils
from search import search

# initialise display
X = 800
Y = 800
screen = pygame.display.set_mode((X, Y))
pygame.init()

search_done = False

# basic colours
WHITE = (255, 255, 255)
GREY = (128, 128, 128)
YELLOW = (204, 204, 0)
BLUE = (50, 255, 255)
BLACK = (0, 0, 0)
BROWN = (204, 183, 174)

# load piece images
pieces = {
    'p': pygame.image.load('assets/gui/b_pawn.svg').convert_alpha(),
    'n': pygame.image.load('assets/gui/b_knight.svg').convert_alpha(),
    'b': pygame.image.load('assets/gui/b_bishop.svg').convert_alpha(),
    'r': pygame.image.load('assets/gui/b_rook.svg').convert_alpha(),
    'q': pygame.image.load('assets/gui/b_queen.svg').convert_alpha(),
    'k': pygame.image.load('assets/gui/b_king.svg').convert_alpha(),
    'P': pygame.image.load('assets/gui/w_pawn.svg').convert_alpha(),
    'N': pygame.image.load('assets/gui/w_knight.svg').convert_alpha(),
    'B': pygame.image.load('assets/gui/w_bishop.svg').convert_alpha(),
    'R': pygame.image.load('assets/gui/w_rook.svg').convert_alpha(),
    'Q': pygame.image.load('assets/gui/w_queen.svg').convert_alpha(),
    'K': pygame.image.load('assets/gui/w_king.svg').convert_alpha(),
}


def update(screen, board):
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece is None:
            pass
        else:
            screen.blit(pieces[str(piece.symbol())], ((square % 8) * 100, 700 - (square // 8) * 100))

    for i in range(7):
        i = i + 1
        pygame.draw.line(screen, WHITE, (0, i * 100), (800, i * 100))
        pygame.draw.line(screen, WHITE, (i * 100, 0), (i * 100, 800))

    pygame.display.flip()



def main(board, engine_color):
    # make background black
    screen.fill(BROWN)
    # name window
    pygame.display.set_caption('Filajabot GUI')

    # variable to be used later
    index_moves = []

    status = True
    while status:
        # update screen
        update(screen, board)

        if board.turn == engine_color:
            start = time.time()

            result = search(board, use_pygame_sleep=True)
            san = board.san(result.best_move)
            board.push(result.best_move)
            screen.fill(BROWN)

            if result.mate_in:
                print(f"M{result.mate_in}")

            print(f"Depth: {result.depth} | Score: {utils.smart_round(result.score, 2)} | Move: {san} | "
                  f"Elapsed: {round(time.time() - start, 2)}s")

        else:
            for event in pygame.event.get():

                # if event object type is QUIT
                # then quitting the pygame
                # and program both.
                if event.type == pygame.QUIT:
                    status = False

                # if mouse clicked
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # reset previous screen from clicks
                    screen.fill(BROWN)
                    # get position of mouse
                    pos = pygame.mouse.get_pos()

                    # find which square was clicked and index of it
                    square = (math.floor(pos[0] / 100), math.floor(pos[1] / 100))
                    index = (7 - square[1]) * 8 + (square[0])

                    # if we have already highlighted moves and are making a move
                    if index in index_moves:
                        move = moves[index_moves.index(index)]
                        # print(board)
                        # print(move)
                        board.push(move)
                        index = None
                        index_moves = []

                    # show possible moves
                    else:

                        piece = board.piece_at(index)

                        if piece is None:
                            pass
                        else:
                            all_moves = list(board.legal_moves)
                            moves = []
                            for m in all_moves:
                                if m.from_square == index:
                                    moves.append(m)

                                    t = m.to_square

                                    TX1 = 100 * (t % 8)
                                    TY1 = 100 * (7 - t // 8)

                                    pygame.draw.rect(screen, BLUE, pygame.Rect(TX1, TY1, 100, 100), 5)
                            # print(moves)
                            index_moves = [a.to_square for a in moves]

        # deactivates the pygame library
        if board.outcome() is not None:
            outcome = board.outcome()
            print(f"Termination: {outcome.termination}")
            print(f"FEN: {board.fen()}")

            status = False
            print(board)

    pygame.quit()


if __name__ == '__main__':
    print("Welcome to the Filajabot GUI!")
    engine_color = input("Select your color (white or black): ") == "black"
    main(chess.Board(), engine_color)
