from functions import *
from config import *
from random import choice


'''
The way the bot works is by evaluating the board for each move and
generating a numeric value. The value is higher if the position
grants advantage to the side playing.
Each piece has a relative value depending on the position and on
which piece it is. The values according to the positions were taken
from https://www.chessprogramming.org/Simplified_Evaluation_Function
and slightly altered.
'''

pawn = [[0,  0,  0,  0,  0,  0,  0,  0],
        [50, 50, 50, 50, 50, 50, 50, 50],
        [10, 10, 20, 15, 15, 20, 10, 10],
        [5,  5, 10, 20, 20, 10,  5,  5],
        [0,  0,  0, 25, 30,  0,  0,  0],
        [5, -5,-10,  0,  0,-10, -5,  5],
        [5, 10, 10,-20,-20, 10, 10,  5],
        [0,  0,  0,  0,  0,  0,  0,  0]]

knight = [[-50,-40,-30,-30,-30,-30,-40,-50],
         [-40,-20,  0,  0,  0,  0,-20,-40],
         [-30,  0, 10, 15, 15, 10,  0,-30],
         [-30,  5, 15, 20, 20, 15,  5,-30],
         [-30,  0, 15, 20, 20, 15,  0,-30],
         [-30,  5, 10, 15, 15, 10,  5,-30],
         [-40,-20,  0,  5,  5,  0,-20,-40],
         [-50,-40,-30,-30,-30,-30,-40,-50]]

bishop = [[-20,-10,-10,-10,-10,-10,-10,-20],
         [-10,  0,  0,  0,  0,  0,  0,-10],
         [-10,  0,  5, 10, 10,  5,  0,-10],
         [-10,  5,  5, 10, 10,  5,  5,-10],
         [-10,  0, 10, 10, 10, 10,  0,-10],
         [-10, 10, 10, 10, 10, 10, 10,-10],
         [-10,  5,  0,  0,  0,  0,  5,-10],
         [-20,-10,-10,-10,-10,-10,-10,-20]]

rook = [[0,  0,  0,  0,  0,  0,  0,  0],
        [5, 10, 10, 10, 10, 10, 10,  5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [0,  0,  0,  5,  5,  0,  0,  0]]

queen = [[-20,-10,-10, -5, -5,-10,-10,-20],
        [-10,  0,  0,  0,  0,  0,  0,-10],
        [-10,  0,  5,  5,  5,  5,  0,-10],
        [-5,  0,  5,  5,  5,  5,  0, -5],
        [0,  0,  5,  5,  5,  5,  0, -5],
        [-10,  5,  5,  5,  5,  5,  0,-10],
        [-10,  0,  5,  0,  0,  0,  0,-10],
        [-20,-10,-10, -5, -5,-10,-10,-20]]

king = [[-30,-40,-40,-50,-50,-40,-40,-30],
        [-30,-40,-40,-50,-50,-40,-40,-30],
        [-30,-40,-40,-50,-50,-40,-40,-30],
        [-30,-40,-40,-50,-50,-40,-40,-30],
        [-20,-30,-30,-40,-40,-30,-30,-20],
        [-10,-20,-20,-20,-20,-20,-20,-10],
        [20, 20,  0,  0,  0,  0, 20, 20],
        [20, 30, 10,  0,  0, 10, 30, 20]]

pieces_value = {**dict.fromkeys([wpawn, bpawn], 10),
                **dict.fromkeys([wknight, bknight], 30),
                **dict.fromkeys([wbishop, bbishop], 30),
                **dict.fromkeys([wrook, brook], 50),
                **dict.fromkeys([wqueen, bqueen], 90),
                **dict.fromkeys([wking, bking], 99999)}

pieces_pos_value = {**dict.fromkeys([wpawn, bpawn], pawn),
                    **dict.fromkeys([wknight, bknight], knight),
                    **dict.fromkeys([wbishop, bbishop], bishop),
                    **dict.fromkeys([wrook, brook], rook),
                    **dict.fromkeys([wqueen, bqueen], queen),
                    **dict.fromkeys([wking, bking], king)}

class Bot(object):
    def get_pieces(self, board, white_moving, wcastle, bcastle):
        '''Returns a list of coordinates with all the movable pieces'''
        res = []
        for (x,y) in [(x,y) for x in range(8) for y in range(8) if board[y][x] != 0]:
            if white_moving and is_white(board[y][x]): res.append((x,y))
            if not white_moving and is_black(board[y][x]): res.append((x,y))
        return list(filter(lambda x: possible_moves(moves(x, board), x, board, wcastle, bcastle) != [], res))

    def get_pos_value(self, piece, pos):
        '''Search the value for a piece according to its position in the board'''
        if is_white(piece): return pieces_pos_value[piece][pos[1]][pos[0]]
        return [x[::-1] for x in pieces_pos_value[piece]][::-1][pos[1]][pos[0]]

    def get_board_value(self, board, white_moving):
        '''Sum the total value on the board'''
        value = 0
        for (x,y) in [(x,y) for x in range(8) for y in range(8) if board[y][x] != 0]:
            if white_moving:
                if is_white(board[y][x]): value += self.get_pos_value(board[y][x], (x,y))
                else: value -= self.get_pos_value(board[y][x], (x,y))
            else:
                if is_white(board[y][x]): value -= self.get_pos_value(board[y][x], (x,y))
                else: value += self.get_pos_value(board[y][x], (x,y))
        return value

    def get_best_move(self, board, pieces, white_moving, wcastle, bcastle):
        '''Search for the move that defines the most valuable board'''
        max_value = -99999
        for piece in pieces:
            for x,y in possible_moves(moves(piece, board), piece, board, wcastle, bcastle):
                current_value = 0
                hold = board[y][x]
                board[y][x] = board[piece[1]][piece[0]]
                board[piece[1]][piece[0]] = 0
                if hold != 0: current_value += pieces_value[hold] #promote captures
                current_value += self.get_board_value(board, white_moving)
                if current_value == max_value: #so it doesnt play the same way everytime
                    switch = choice([False, True])
                    if switch:
                        best_piece = piece
                        best_move = (x,y)
                if current_value > max_value:
                    max_value = current_value
                    best_piece = piece
                    best_move = (x,y)
                board[piece[1]][piece[0]] = board[y][x]
                board[y][x] = hold
        return (best_piece, best_move)

    def play(self, board, white_moving, wcastle, bcastle):
        '''Returns the move as (best_piece, best_move)'''
        pieces = self.get_pieces(board, white_moving, wcastle, bcastle)
        if pieces == []: return False
        prev_board = copy_board(board)
        res = self.get_best_move(prev_board, pieces, white_moving, wcastle, bcastle)
        return (res[0], res[1])

