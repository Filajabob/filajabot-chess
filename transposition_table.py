import random
import time
import sys
import chess
from constants import Constants
import utils
from result import Result
from logger import filajabot_logger


class TranspositionTable:
    def __init__(self):
        self.zobrist_array = ZobristArray()
        self.entries = {}

    def generate_entry(self, result: Result, board, alpha, beta, zobrist_hash, move=None):
        if move:
            zobrist_hash = self.zobrist_array.push(zobrist_hash, move)

        entry = TranspositionEntry(zobrist_hash, result.best_move, result.depth, result.score,
                                   utils.NodeType.get_node_type(result.score, alpha, beta, board.turn), time.time())

        return entry

    def add_entry(self, entry):
        if entry.zobrist_hash in self.entries:
            # We will do a depth-preferred replacement scheme for simplicity -
            # https://www.chessprogramming.org/Transposition_Table
            if self.entries[entry.zobrist_hash].depth > entry.depth:
                return

        self.entries[entry.zobrist_hash] = entry

    def generate_add_entry(self, result: Result, board, alpha, beta, zobrist_hash, move=None):
        self.add_entry(self.generate_entry(result, board, alpha, beta, zobrist_hash, move))

    def probe(self, zobrist_hash):
        """Probes the transposition table for a zobrist_hash"""
        if zobrist_hash not in self.entries:
            return None
        else:
            return self.entries[zobrist_hash]


class TranspositionEntry:
    def __init__(self, zobrist_hash: int, best_move: chess.Move, depth: int, score: float, node_type: utils.NodeType,
                 time: float):
        self.zobrist_hash = zobrist_hash
        self.best_move = best_move
        self.depth = depth
        self.score = score
        self.node_type = node_type
        self.time = time

    def result(self):
        return Result(self.score, self.depth, self.best_move)


class ZobristArray:
    def __init__(self, bits=Constants.ZOBRIST_BITS):
        self.bits = bits
        self.piece_array = {}
        self.color = random.getrandbits(bits)
        self.castling_rights = []
        self.en_passant = []
        self.previous_move = None

        for piece in chess.PIECE_TYPES:
            self.piece_array[piece] = [None] * 64
            for square in chess.SQUARES:
                self.piece_array[piece][square] = random.getrandbits(bits)

        for i in range(4):
            self.castling_rights.append(random.getrandbits(bits))

        for file in range(8):
            self.en_passant.append(random.getrandbits(bits))

    def positional_hash(self, board):
        """
        Generates a Zobrist hash for a given position. Do not use for move making/unmaking.
        :param board:
        :return:
        """

        zobrist_hash = 0

        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece:
                zobrist_hash ^= self.piece_array[piece.piece_type][square]

        if board.has_kingside_castling_rights(chess.WHITE):
            zobrist_hash ^= self.castling_rights[0]
        if board.has_queenside_castling_rights(chess.WHITE):
            zobrist_hash ^= self.castling_rights[1]
        if board.has_kingside_castling_rights(chess.BLACK):
            zobrist_hash ^= self.castling_rights[2]
        if board.has_queenside_castling_rights(chess.BLACK):
            zobrist_hash ^= self.castling_rights[3]

        if board.has_legal_en_passant():
            for move in board.legal_moves:
                if board.is_en_passant(move):
                    zobrist_hash ^= self.en_passant[chess.square_file(move.from_square)]
                    break  # There should only be one valid en-passant

        return zobrist_hash

    def update(self, zobrist_hash, piece, square):
        return zobrist_hash ^ self.piece_array[piece.piece_type][square]

    def push(self, zobrist_hash, move, board):
        """Always do ZobristArray.push() BEFORE doing board.push()"""
        zobrist_hash = self.update(zobrist_hash, board.piece_at(move.from_square), move.from_square)  # Remove the
        # piece that moved

        if board.is_capture(move):
            if board.is_en_passant(move):
                if board.turn is chess.WHITE:
                    captured_square = move.to_square - 8
                else:
                    captured_square = move.to_square + 8

                zobrist_hash = self.update(zobrist_hash, board.piece_at(captured_square), captured_square)
            else:
                zobrist_hash = self.update(zobrist_hash, board.piece_at(move.to_square), move.to_square)  # Remove
                # the piece that was captured, if applicable

        zobrist_hash = self.update(zobrist_hash, board.piece_at(move.from_square), move.to_square)  # Add the piece
        # to the new square

        if board.has_legal_en_passant():
            for move in board.legal_moves:
                if board.is_en_passant(move):
                    zobrist_hash ^= self.en_passant[chess.square_file(move.from_square)]
                    break  # There should only be one valid en-passant

        # Castling logic
        if board.is_castling(move):
            if move.to_square == chess.G1:
                zobrist_hash ^= self.piece_array[chess.ROOK][chess.H1]
                zobrist_hash ^= self.piece_array[chess.ROOK][chess.F1]
            elif move.to_square == chess.C1:
                zobrist_hash ^= self.piece_array[chess.ROOK][chess.A1]
                zobrist_hash ^= self.piece_array[chess.ROOK][chess.D1]
            elif move.to_square == chess.G8:
                zobrist_hash ^= self.piece_array[chess.ROOK][chess.H8]
                zobrist_hash ^= self.piece_array[chess.ROOK][chess.F8]
            elif move.to_square == chess.C8:
                zobrist_hash ^= self.piece_array[chess.ROOK][chess.A8]
                zobrist_hash ^= self.piece_array[chess.ROOK][chess.D8]

        if board.turn is chess.BLACK:
            zobrist_hash ^= self.color

        self.previous_move = move

        return zobrist_hash

    pop = push
