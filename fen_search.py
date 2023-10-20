import chess
from search import search

fen = input("FEN: ")

result = search(chess.Board(fen=fen))

print(result.score)
print(result.best_move)


