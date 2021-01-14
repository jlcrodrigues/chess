from functions import *
from config import *
from random import choice

class Bot(object):
    def get_pieces(self, board, white_moving, wcastle, bcastle):
        res = []
        for (x,y) in [(x,y) for x in range(8) for y in range(8) if board[y][x] != 0]:
            if white_moving and board[y][x] in [wrook, wknight, wbishop, wqueen, wking, wpawn]: res.append((x,y))
            if not white_moving and board[y][x] in [brook, bknight, bbishop, bqueen, bking, bpawn]: res.append((x,y))
        return list(filter(lambda x: possible_moves(moves(x, board), x, board, wcastle, bcastle) != [], res))

    def play(self, board, white_moving, wcastle, bcastle):
        pieces = self.get_pieces(board, white_moving, wcastle, bcastle)
        if pieces == []: return False
        piece = choice(pieces)
        move = choice(possible_moves(moves(piece, board), piece, board, wcastle, bcastle))
        return (piece, move)
