import pygame
import copy

pygame.init()

win = pygame.display.set_mode((640,640))

selected_check = False

board_img = pygame.image.load("../assets/board.png")
(wpawn, bpawn) = (pygame.image.load("../assets/wpawn.png"),pygame.image.load("../assets/bpawn.png"))
(wknight, bknight) = (pygame.image.load("../assets/wknight.png"),pygame.image.load("../assets/bknight.png"))
(wbishop, bbishop) = (pygame.image.load("../assets/wbishop.png"),pygame.image.load("../assets/bbishop.png"))
(wrook, brook) = (pygame.image.load("../assets/wrook.png"),pygame.image.load("../assets/brook.png"))
(wqueen, bqueen) = (pygame.image.load("../assets/wqueen.png"),pygame.image.load("../assets/bqueen.png"))
(wking, bking) = (pygame.image.load("../assets/wking.png"),pygame.image.load("../assets/bking.png"))

board = [[brook, bknight, bbishop, bqueen, bking, bbishop, bknight, brook],
[bpawn, bpawn, bpawn, bpawn, bpawn, bpawn, bpawn, bpawn],
[0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0],
[wpawn, wpawn, wpawn, wpawn, wpawn, wpawn, wpawn, wpawn],
[wrook, wknight, wbishop, wqueen, wking, wbishop, wknight, wrook]]

new_board = [[0,0,0,0,0,0,0,0] for _ in range(8)]

def print_board(board): #for debugging
    s = ["wpawn","wknight","wbishop","wrook","wqueen","wking", "bpawn","bknight","bbishop","brook","bqueen","bking",0]
    p = [wpawn,wknight,wbishop,wrook,wqueen,wking, bpawn,bknight,bbishop,brook,bqueen,bking,0]
    for line in board:
        print(list(map(lambda x: s[p.index(x)], line)))

def draw_board(board):
    '''Function that renders the pieces on the board'''
    for i in range(8):
        for j in range(8):
            if board[i][j] != 0: win.blit(board[i][j], (64 + 64*j, 64 + 64*i))

def inside_board(mouse):
    '''Checks if the mouse is in a square'''
    coords = (mouse[0]//64 - 1, mouse[1]//64 - 1)
    return (-1 not in coords and 8 not in coords)

def hitbox(mouse):
    '''Returns the square where the mouse clicked'''
    #print((mouse[0]//64 - 1, mouse[1]//64 - 1))
    return (mouse[0]//64 - 1, mouse[1]//64 - 1)

def is_white(piece):
    return piece in [wrook, wknight, wbishop, wqueen, wking, wpawn]

def is_black(piece):
    return piece in [brook, bknight, bbishop, bqueen, bking, bpawn]

def find_side(piece):
    return "white" * is_white(piece) + "black" * is_black(piece)

def find_king(side, board):
    for (x,y) in [(x,y) for x in range(8) for y in range(8)]:
        if side == "white" and board[y][x] == wking: return(x,y)
        if side == "black" and board[y][x] == bking: return(x,y)

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
    return res

def moves(coords, board):
    '''Returns a list of tuples with the possible moves for a certain piece on the board'''
    piece = board[coords[1]][coords[0]]
    res = []
    if piece == wpawn and coords[1] > 0:
        if board[coords[1] - 1][coords[0]] == 0:
            res.append((coords[0], coords[1] - 1))
        if coords[1] == 6:
            if board[coords[1] - 2][coords[0]] == 0: res.append((coords[0], coords[1] - 2)) #first move
        if coords[0] < 7:
            if board[coords[1] - 1][coords[0] + 1] != 0: res.append((coords[0] + 1, coords[1] - 1)) #left capture
        if board[coords[1] - 1][coords[0] - 1] != 0: res.append((coords[0] - 1, coords[1] - 1)) #right capture
        
    if piece == bpawn and coords[1] < 7:
        if board[coords[1] + 1][coords[0]] == 0:
            res.append((coords[0], coords[1] + 1))
        if coords[1] == 1:
            if board[coords[1] + 2][coords[0]] == 0: res.append((coords[0], coords[1] + 2)) #first move
        if coords[0] < 7:
            if board[coords[1] + 1][coords[0] + 1] != 0: res.append((coords[0] + 1, coords[1] + 1)) #left capture
        if board[coords[1] + 1][coords[0] - 1] != 0: res.append((coords[0] - 1, coords[1] + 1)) #right capture

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
    #res = list(filter(lambda x: not threat_move(coords, x), res)) #cant endanger king
    #print(res)
    return res

def possible_moves(coords_list, selected):
    '''A piece cant move leaving the king threatened'''
    res = list(filter(lambda x: not threat_move(selected, x), coords_list))
    return res
    
def draw_moves(coords_list):
    for coords in coords_list:
        pygame.draw.circle(win, (0,0,0), (coords[0] * 64 + 96, coords[1] * 64 + 96), 7)

run = True
while run:
    pygame.time.delay(27)
    mouse = pygame.mouse.get_pos()    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not inside_board(mouse): continue
            if selected_check and hitbox(mouse) != selected and hitbox(mouse) in possible_moves(moves(selected, board), selected): #select the square to move to
                new = hitbox(mouse)
                board[new[1]][new[0]] = board[selected[1]][selected[0]]
                board[selected[1]][selected[0]] = 0
                selected_check = False
            elif selected_check and hitbox(mouse) == selected: selected_check = False
            else: #select a piece to move
                selected = hitbox(mouse)
                if board[selected[1]][selected[0]] != 0: selected_check = True

    
    win.blit(board_img, (0,0))
    
    draw_board(board)
    if selected_check: draw_moves(possible_moves(moves(selected, board), selected))
    pygame.display.update()

pygame.quit()
