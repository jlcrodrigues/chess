import pygame

pygame.init()

win = pygame.display.set_mode((640,640))

selected_check = False

board_img = pygame.image.load("libs/board.png")
(wpawn, bpawn) = (pygame.image.load("libs/wpawn.png"),pygame.image.load("libs/bpawn.png"))
(wknight, bknight) = (pygame.image.load("libs/wknight.png"),pygame.image.load("libs/bknight.png"))
(wbishop, bbishop) = (pygame.image.load("libs/wbishop.png"),pygame.image.load("libs/bbishop.png"))
(wrook, brook) = (pygame.image.load("libs/wrook.png"),pygame.image.load("libs/brook.png"))
(wqueen, bqueen) = (pygame.image.load("libs/wqueen.png"),pygame.image.load("libs/bqueen.png"))
(wking, bking) = (pygame.image.load("libs/wking.png"),pygame.image.load("libs/bking.png"))

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

def possible_moves(coords):
    '''Returns a list of tuples with the possible moves for a certain piece on the board'''
    piece = board[coords[1]][coords[0]]
    res = []
    #print(coords)
    if piece == wpawn and coords[1] > 0:
        res.append((coords[1] - 1, coords[0]))
        if coords[1] == 6: res.append((coords[1] - 2, coords[0])) #first move
        if board[coords[1] - 1][coords[0] + 1] != 0: res.append((coords[1] - 1, coords[0] + 1)) #captures
        if board[coords[1] - 1][coords[0] - 1] != 0: res.append((coords[1] - 1, coords[0] - 1))
    if piece == bpawn: 
        res.append((coords[1] + 1, coords[0]))
        if coords[1] == 1: res.append((coords[1] + 2, coords[0])) #first move
        if board[coords[1] + 1][coords[0] + 1] != 0: res.append((coords[1] + 1, coords[0] + 1)) #captures
        if board[coords[1] + 1][coords[0] - 1] != 0: res.append((coords[1] + 1, coords[0] - 1))
    print(res)
    return res
    
def draw_moves(coords_list):
    #print(coords_list)
    for coords in coords_list:
        pygame.draw.circle(win, (0,0,0), (coords[1] * 64 + 96, coords[0] * 64 + 96), 7)
        
possible_moves((1,2))

run = True
while run:
    pygame.time.delay(27)
    mouse = pygame.mouse.get_pos()    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not inside_board(mouse): continue
            if selected_check and hitbox(mouse) != selected and hitbox(mouse)[::-1] in possible_moves(selected): #select the square to move to
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