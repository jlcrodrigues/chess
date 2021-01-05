import pygame

from config import *

def print_board(board): #for debugging
    s = ["wpawn","wknight","wbishop","wrook","wqueen","wking", "bpawn","bknight","bbishop","brook","bqueen","bking",0]
    p = [wpawn,wknight,wbishop,wrook,wqueen,wking, bpawn,bknight,bbishop,brook,bqueen,bking,0]
    for line in board:
        print(list(map(lambda x: s[p.index(x)], line)))

def inside_board(mouse):
    '''Checks if the mouse is in a square'''
    coords = (mouse[0]//64 - 1, mouse[1]//64 - 1)
    return (-1 not in coords and 8 not in coords)

def hitbox(mouse):
    '''Returns the square where the mouse clicked'''
    return (mouse[0]//64 - 1, mouse[1]//64 - 1)

def is_white(piece):
    return piece in [wrook, wknight, wbishop, wqueen, wking, wpawn]

def is_black(piece):
    return piece in [brook, bknight, bbishop, bqueen, bking, bpawn]

def find_side(piece):
    return "white" * is_white(piece) + "black" * is_black(piece)

def find_turn(white_moving):
    return white_moving * 'white'  + 'black' * (not white_moving)

def find_king(side, board):
    for (x,y) in [(x,y) for x in range(8) for y in range(8)]:
        if side == "white" and board[y][x] == wking: return(x,y)
        if side == "black" and board[y][x] == bking: return(x,y)

############ movements ############

def threat(coords, board):
    '''Checks if a piece is threatened'''
    for (x,y) in [(x,y) for x in range(8) for y in range(8) if board[y][x] != 0]: #iterates de pieces of the board
        if find_side(board[coords[1]][coords[0]]) == "white":
            if board[y][x] in [wking,bking]:
                if is_black(board[y][x]) and coords in king_moves((x,y)): return True
            elif is_black(board[y][x]) and coords in moves((x,y), board): return True
        if find_side(board[coords[1]][coords[0]]) == "black":
            if board[y][x] in [wking,bking]:
                if is_white(board[y][x]) and coords in king_moves((x,y)): return True
            elif is_white(board[y][x]) and coords in moves((x,y), board): return True
    return False

def threat_move(coords, new_coords):
    '''Checks if moving a piece will endanger the king'''
    for (x,y) in [(x,y) for x in range(8) for y in range(8)]:
        new_board[y][x] = board[y][x]
    new_board[new_coords[1]][new_coords[0]] = new_board[coords[1]][coords[0]]
    new_board[coords[1]][coords[0]] = 0
    side = find_side(new_board[new_coords[1]][new_coords[0]])
    return threat(find_king(side, new_board), new_board)

def king_moves(coords):
    '''Return all possible moves for the king without restrictions'''
    res = []
    for (j, g) in [(j,g) for j in [-1,1,0] for g in [-1,1,0]]:
            if 0 <= coords[0] + j<= 7 and 0 <= coords[1] + g<= 7 and (coords[0] + j, coords[1] + g) != coords:
                res.append((coords[0] + j, coords[1] + g))
    for i in [(wking, 7), (bking, 0)]:
        if board[coords[1]][coords[0]] == i[0]:
            if board[i[1]][6] == 0 and board[i[1]][5] == 0 and wcastle[1]: res.append((6,i[1]))
            if board[i[1]][1] == 0 and board[i[1]][2] == 0 and board[i[1]][3] == 0 and wcastle[0]: res.append((2,i[1]))
    return res

def moves(coords, board):
    '''Returns a list of tuples (x,y) with the possible moves for a certain piece on the board'''
    piece = board[coords[1]][coords[0]]
    res = []
    if piece == wpawn and coords[1] > 0:
        if board[coords[1] - 1][coords[0]] == 0:
            res.append((coords[0], coords[1] - 1))
        if coords[1] == 6:
            if board[coords[1] - 2][coords[0]] == 0 and  board[coords[1] - 1][coords[0]] == 0: res.append((coords[0], coords[1] - 2)) #first move
        if coords[0] < 7:
            if board[coords[1] - 1][coords[0] + 1] != 0: res.append((coords[0] + 1, coords[1] - 1)) #left capture
        if board[coords[1] - 1][coords[0] - 1] != 0: res.append((coords[0] - 1, coords[1] - 1)) #right capture
        if coords[1] == 3 and coords[0] < 7: #en passant
            if board[coords[1]][coords[0] + 1] and previous_board[1][coords[0] + 1] == bpawn:
                res.append((coords[0] + 1, coords[1] - 1))
        if coords[1] == 3 and coords[0] > 0 and previous_board[1][coords[0] - 1] == bpawn:
            if  board[coords[1]][coords[0] - 1]:
                res.append((coords[0] - 1, coords[1] - 1))
        
    if piece == bpawn and coords[1] < 7:
        if board[coords[1] + 1][coords[0]] == 0:
            res.append((coords[0], coords[1] + 1))
        if coords[1] == 1:
            if board[coords[1] + 2][coords[0]] == 0 and board[coords[1] + 1][coords[0]] == 0: res.append((coords[0], coords[1] + 2)) #first move
        if coords[0] < 7:
            if board[coords[1] + 1][coords[0] + 1] != 0: res.append((coords[0] + 1, coords[1] + 1)) #left capture
        if board[coords[1] + 1][coords[0] - 1] != 0: res.append((coords[0] - 1, coords[1] + 1)) #right capture
        if coords[1] == 4 and coords[0] < 7: #en passant
            if board[coords[1]][coords[0] + 1] and previous_board[6][coords[0] + 1] == wpawn:
                res.append((coords[0] + 1, coords[1] + 1))
        if coords[1] == 4 and coords[0] > 0 and previous_board[6][coords[0] - 1] == wpawn:
            if  board[coords[1]][coords[0] - 1]:
                res.append((coords[0] - 1, coords[1] + 1))

    if piece in [wknight, bknight]:
        for x, y in [(x, y) for x in (1,-1) for y in (2, -2)]:
            res.append((coords[0] + x, coords[1] + y))
        for x, y in [(x, y) for y in (1,-1) for x in (2, -2)]:
            res.append((coords[0] + x, coords[1] + y))

    if piece in [wbishop, bbishop, wqueen, bqueen]: 
        for j, g in [(j, g) for j in (-1, 1) for g in (-1, 1)]:
            for i in range(1, 10):
                if 0 <= coords[0] + i * g<= 7 and 0 <= coords[1] + i * j <= 7:
                    res.append((coords[0] + i * g, coords[1] + i * j))
                    if board[coords[1] + i * j][coords[0] + i * g] != 0: break

    if piece in [wrook, brook, wqueen, bqueen]:
        for j in [-1, 1]:
            for i in range(1, 10):
                if 0 <= coords[0] <= 7 and 0 <= coords[1] + i * j <= 7:
                    res.append((coords[0] , coords[1] + i * j))
                    if board[coords[1] + i * j][coords[0]] != 0: break

            for i in range(1, 10):
                if 0 <= coords[0] + i * j<= 7 and 0 <= coords[1]<= 7:
                    res.append((coords[0] + i * j, coords[1]))
                    if board[coords[1]][coords[0] + i * j] != 0: break

    if piece in [wking, bking]:
        for (x,y) in king_moves(coords):
            res.append((x,y))
    
    res = list(filter(lambda x: x[1] >= 0 and x[1] <= 7 and x[0] >= 0 and x[0] <= 7, res)) #check if move is inside the board
    if is_white(piece): res = list(filter(lambda x: not is_white(board[x[1]][x[0]]), res)) #cant capture own
    if is_black(piece): res = list(filter(lambda x: not is_black(board[x[1]][x[0]]), res))
    return res

def possible_moves(coords_list, selected):
    '''Filters the list of possible moves'''
    res = list(filter(lambda x: not threat_move(selected, x), coords_list))    
    if board[selected[1]][selected[0]] == wking and True in wcastle:
        if threat_move(find_king('white', board), (5,7)) and (6,7) in res: res.remove((6,7))
        if threat_move(find_king('white', board), (3,7)) and (2,7) in res: res.remove((2,7))
    if board[selected[1]][selected[0]] == bking and True in bcastle:
        if threat_move(find_king('black', board), (5,0)) and (6,0) in res: res.remove((6,0))
        if threat_move(find_king('black', board), (3,0)) and (2,0) in res: res.remove((2,0))
    return res

############ image rendering ############

def draw_board(win, board):
    '''Function that renders the pieces on the board'''
    for i in range(8):
        for j in range(8):
            if board[i][j] != 0: win.blit(board[i][j], (64 + 64*j, 64 + 64*i))

def draw_moves(win, coords_list, selected):
    '''Draws every square the selected piece can move to'''
    for coords in coords_list:
        if board[coords[1]][coords[0]] != 0: win.blit(target, (64 + 64*coords[0], 64 + 64*coords[1]))
        else: pygame.draw.circle(win, (20, 23, 25), (coords[0] * 64 + 96, coords[1] * 64 + 96), 7)
        if board[selected[1]][selected[0]] == wking and coords == (2,7) and wcastle[0]: win.blit(target, (64, 512)) #castling
        if board[selected[1]][selected[0]] == wking and coords == (6,7) and wcastle[1]: win.blit(target, (512, 512))
        if board[selected[1]][selected[0]] == bking and coords == (2,0) and bcastle[0]: win.blit(target, (64, 64))
        if board[selected[1]][selected[0]] == bking and coords == (6,0) and bcastle[1]: win.blit(target, (512, 512))

def draw_pawn_promotion(win, coords):
    '''Draws the pieces the pawn can promote to'''
    if board[coords[1]][coords[0]] == wpawn:
        for i in enumerate([wqueen, wrook, wbishop, wknight]):
            win.blit(i[1], (0, 64 + 64*i[0]))
    if board[coords[1]][coords[0]] == bpawn:
        for i in enumerate([bqueen, brook, bbishop, bknight]):
            win.blit(i[1], (576, 320 + 64*i[0]))

############ board evaluation ############

def check(board):
    (white, black) = (False, False)
    for (x,y) in [(x,y) for x in range(8) for y in range(8) if board[y][x] != 0]:
        possible_moves = res = list(filter(lambda z: not threat_move((x,y), z), moves((x,y),board)))
        if is_white(board[y][x]) and find_king('black', board) in possible_moves: black = True
        if is_black(board[y][x]) and find_king('white', board) in possible_moves: white = True
    return 'white' * white + 'black' * black

def checkmate(board):
    (white, black) = (True, True)
    for (x,y) in [(x,y) for x in range(8) for y in range(8) if board[y][x] != 0]:
        if possible_moves(moves((x,y), board), (x,y)) != []:
            if is_white(board[y][x]): white = False
            if is_black(board[y][x]): black = False
    return 'white' * white + 'black' * black

def restart_game():
    global board
    global selected_check
    global white_moving
    selected_check = False
    white_moving = True
    board = [[brook, bknight, bbishop, bqueen, bking, bbishop, bknight, brook],
            [bpawn, bpawn, bpawn, bpawn, bpawn, bpawn, bpawn, bpawn],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [wpawn, wpawn, wpawn, wpawn, wpawn, wpawn, wpawn, wpawn],
            [wrook, wknight, wbishop, wqueen, wking, wbishop, wknight, wrook]] 
