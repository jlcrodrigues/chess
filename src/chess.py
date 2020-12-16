import pygame

pygame.init()

win = pygame.display.set_mode((640,640))

selected_check = False

board_img = pygame.image.load("../libs/board.png")
(wpawn, bpawn) = (pygame.image.load("../libs/wpawn.png"),pygame.image.load("../libs/bpawn.png"))
(wknight, bknight) = (pygame.image.load("../libs/wknight.png"),pygame.image.load("../libs/bknight.png"))
(wbishop, bbishop) = (pygame.image.load("../libs/wbishop.png"),pygame.image.load("../libs/bbishop.png"))
(wrook, brook) = (pygame.image.load("../libs/wrook.png"),pygame.image.load("../libs/brook.png"))
(wqueen, bqueen) = (pygame.image.load("../libs/wqueen.png"),pygame.image.load("../libs/bqueen.png"))
(wking, bking) = (pygame.image.load("../libs/wking.png"),pygame.image.load("../libs/bking.png"))

board = [[brook, bknight, bbishop, bqueen, bking, bbishop, bknight, brook],
[bpawn, bpawn, bpawn, bpawn, bpawn, bpawn, bpawn, bpawn],
[0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0],
[wpawn, wpawn, wpawn, wpawn, wpawn, wpawn, wpawn, wpawn],
[wrook, wknight, wbishop, wqueen, wking, wbishop, wknight, wrook]]

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

def possible_moves(coords):
    '''Returns a list of tuples with the possible moves for a certain piece on the board'''
    piece = board[coords[1]][coords[0]]
    res = []
    if piece == wpawn and coords[1] > 0:
        if board[coords[1] - 1][coords[0]] == 0:
            res.append((coords[0], coords[1] - 1))
            if coords[1] == 6: res.append((coords[0], coords[1] - 2)) #first move
        if coords[0] < 7:
            if board[coords[1] - 1][coords[0] + 1] != 0: res.append((coords[0] + 1, coords[1] - 1)) #left capture
        if board[coords[1] - 1][coords[0] - 1] != 0: res.append((coords[0] - 1, coords[1] - 1)) #right capture
        
    if piece == bpawn and coords[1] < 7:
        if board[coords[1] + 1][coords[0]] == 0:
            res.append((coords[0], coords[1] + 1))
            if coords[1] == 1: res.append((coords[0], coords[1] + 2)) #first move
        if coords[0] < 7:
            if board[coords[1] + 1][coords[0] + 1] != 0: res.append((coords[0] + 1, coords[1] + 1)) #left capture
        if board[coords[1] + 1][coords[0] - 1] != 0: res.append((coords[0] - 1, coords[1] + 1)) #right capture

    if piece in [wknight, bknight]:
        for x, y in [(x, y) for x in (1,-1) for y in (2, -2)]:
            res.append((coords[0] + x, coords[1] + y))
        for x, y in [(x, y) for y in (1,-1) for x in (2, -2)]:
            res.append((coords[0] + x, coords[1] + y))

    if piece in [wbishop, bbishop, wqueen, bqueen]: #WIP   
        for i in range(1, 10):
            if 0 <= coords[0] + i <= 7 and 0 <= coords[1] + i <= 7:
                res.append((coords[0] + i, coords[1] + i))
                if board[coords[1] + i][coords[0] + i] != 0: break
        for i in range(1, 10):
            if 0 <= coords[0] + i <= 7 and 0 <= coords[1] - i <= 7:
                res.append((coords[0] + i, coords[1] - i))
                if board[coords[1] - i][coords[0] + i] != 0: break
        for i in range(1, 10):
            if 0 <= coords[0] - i <= 7 and 0 <= coords[1] + i <= 7:
                res.append((coords[0] - i, coords[1] + i))
                if board[coords[1] + i][coords[0] - i] != 0: break
        for i in range(1, 10):
            if 0 <= coords[0] - i <= 7 and 0 <= coords[1] - i <= 7:
                res.append((coords[0] - i, coords[1] - i))
                if board[coords[1] - i][coords[0] - i] != 0: break

    if piece in [wrook, brook, wqueen, bqueen]:
        pass

    if piece in [wking, bking]:
        pass
    
    res = list(filter(lambda x: x[1] >= 0 and x[1] <= 7 and x[0] >= 0 and x[0] <= 7, res))
    if is_white(piece): res = list(filter(lambda x: not is_white(board[x[1]][x[0]]), res)) #cant capture own
    if is_black(piece): res = list(filter(lambda x: not is_black(board[x[1]][x[0]]), res))
    #print(res)
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
            if selected_check and hitbox(mouse) != selected and hitbox(mouse) in possible_moves(selected): #select the square to move to
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
    if selected_check: draw_moves(possible_moves(selected))
    pygame.display.update()

pygame.quit()

