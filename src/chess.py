import pygame
import copy

pygame.init()

win = pygame.display.set_mode((640,640))

selected_check = False
is_pawn_promoting = False
white_moving = True
wcastle = [True, True]
bcastle = [True, True]

board_img = pygame.image.load("../assets/board.png")
(wpawn, bpawn) = (pygame.image.load("../assets/wpawn.png"), pygame.image.load("../assets/bpawn.png"))
(wknight, bknight) = (pygame.image.load("../assets/wknight.png"), pygame.image.load("../assets/bknight.png"))
(wbishop, bbishop) = (pygame.image.load("../assets/wbishop.png"), pygame.image.load("../assets/bbishop.png"))
(wrook, brook) = (pygame.image.load("../assets/wrook.png"), pygame.image.load("../assets/brook.png"))
(wqueen, bqueen) = (pygame.image.load("../assets/wqueen.png"), pygame.image.load("../assets/bqueen.png"))
(wking, bking) = (pygame.image.load("../assets/wking.png"), pygame.image.load("../assets/bking.png"))

board = [[brook, bknight, bbishop, bqueen, bking, bbishop, bknight, brook],
        [bpawn, bpawn, bpawn, bpawn, bpawn, bpawn, bpawn, bpawn],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [wpawn, wpawn, wpawn, wpawn, wpawn, wpawn, wpawn, wpawn],
        [wrook, wknight, wbishop, wqueen, wking, wbishop, wknight, wrook]]

new_board = [[0,0,0,0,0,0,0,0] for _ in range(8)]
previous_board = [[0,0,0,0,0,0,0,0] for _ in range(8)]

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
    if board[coords[1]][coords[0]] == wking:
        if board[7][6] == 0 and board[7][5] == 0 and wcastle[1]: res.append((6,7))
        if board[7][1] == 0 and board[7][2] == 0 and board[7][3] == 0 and wcastle[0]: res.append((2,7))
    if board[coords[1]][coords[0]] == bking:
        if board[0][6] == 0 and board[0][5] == 0 and bcastle[1]: res.append((6,0))
        if board[0][1] == 0 and board[0][2] == 0 and board[0][3] == 0 and bcastle[0]: res.append((2,0))
    return res

def moves(coords, board):
    '''Returns a list of tuples with the possible moves for a certain piece on the board'''
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
    '''Filters the list of moves'''
    res = list(filter(lambda x: not threat_move(selected, x), coords_list))    
    if board[selected[1]][selected[0]] == wking:
        if threat_move(find_king('white', board), (5,7)) and (6,7) in res and wcastle[1]: res.remove((6,7))
        if threat_move(find_king('white', board), (3,7)) and (2,7) in res and wcastle[0]: res.remove((2,7))
    if board[selected[1]][selected[0]] == bking:
        if threat_move(find_king('black', board), (5,0)) and (6,0) in res and bcastle[1]: res.remove((6,0))
        if threat_move(find_king('black', board), (3,0)) and (2,0) in res and bcastle[0]: res.remove((2,0))
    return res

def draw_moves(coords_list):
    for coords in coords_list:
        pygame.draw.circle(win, (0,0,0), (coords[0] * 64 + 96, coords[1] * 64 + 96), 7)

def draw_pawn_promotion(coords):
    if board[coords[1]][coords[0]] == wpawn:
        for i in enumerate([wqueen, wrook, wbishop, wknight]):
            win.blit(i[1], (0, 64 + 64*i[0]))
    if board[coords[1]][coords[0]] == bpawn:
        for i in enumerate([bqueen, brook, bbishop, bknight]):
            win.blit(i[1], (576, 320 + 64*i[0]))

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

run = True
while run:
    pygame.time.delay(27)
    mouse = pygame.mouse.get_pos()    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not is_pawn_promoting:
                if not inside_board(mouse): continue
                if selected_check and hitbox(mouse) != selected and hitbox(mouse) in possible_moves(moves(selected, board), selected): #select the square to move to
                #if selected_check and hitbox(mouse) != selected and hitbox(mouse): #used for debugging
                    if (white_moving and is_white(board[selected[1]][selected[0]])) or (not white_moving and is_black(board[selected[1]][selected[0]])):
                        new = hitbox(mouse)
                        for (x,y) in [(x,y) for x in range(8) for y in range(8)]:
                            previous_board[y][x] = board[y][x]
                        board[new[1]][new[0]] = board[selected[1]][selected[0]]
                        board[selected[1]][selected[0]] = 0
                        selected_check = False
                        if board[new[1]][new[0]] == wpawn and new[1] == 0: #pawn promotion
                            is_pawn_promoting = True
                            pawn_promoting = new
                        if board[new[1]][new[0]] == bpawn and new[1] == 7:
                            is_pawn_promoting = True
                            pawn_promoting = new
                        white_moving = not white_moving
                        if board[new[1]][new[0]] == wking and new == (2,7) and wcastle[0]: (board[7][3], board[7][0]) = (wrook, 0) #castling
                        if board[new[1]][new[0]] == wking and new == (6,7) and wcastle[1]: (board[7][5], board[7][7]) = (wrook, 0)
                        if board[new[1]][new[0]] == bking and new == (2,0) and bcastle[0]: (board[0][3], board[0][0]) = (brook, 0)
                        if board[new[1]][new[0]] == bking and new == (6,0) and bcastle[1]: (board[0][5], board[0][7]) = (brook, 0)
                        if board[new[1]][new[0]] == wking: wcastle = [False, False]
                        if board[new[1]][new[0]] == bking: bcastle = [False, False]
                        if board[new[1]][new[0]] == wrook:
                            if selected == (0,7): wcastle[0] = False
                            if selected == (7,7): wcastle[1] = False
                        if board[new[1]][new[0]] == brook:
                            if selected == (0,0): bcastle[0] = False
                            if selected == (7,0): bcastle[1] = False
                        #en passant
                        if previous_board[selected[1]][selected[0]] == wpawn and board[new[1] + 1][new[0]] == bpawn and previous_board[new[1]][new[0]] == 0:
                            board[new[1] + 1][new[0]] = 0
                        if previous_board[selected[1]][selected[0]] == bpawn and board[new[1] - 1][new[0]] == wpawn and previous_board[new[1]][new[0]] == 0:
                            board[new[1] - 1][new[0]] = 0
                        if check(board):
                            if checkmate(board) != '':
                                pygame.time.delay(3000)
                                restart_game()
                elif selected_check and hitbox(mouse) == selected: selected_check = False
                else: #select a piece to move
                    selected = hitbox(mouse)
                    if board[selected[1]][selected[0]] != 0: selected_check = True
            else:
                if hitbox(mouse)[0] == -1 and is_white(board[pawn_promoting[1]][pawn_promoting[0]]) and 0 <= hitbox(mouse)[1] <= 3:
                    board[pawn_promoting[1]][pawn_promoting[0]] = [wqueen, wrook, wbishop, wknight][hitbox(mouse)[1]]
                    is_pawn_promoting = False
                if hitbox(mouse)[0] == 8 and is_black(board[pawn_promoting[1]][pawn_promoting[0]]) and 4 <= hitbox(mouse)[1] <= 7:
                    board[pawn_promoting[1]][pawn_promoting[0]] = [bqueen, brook, bbishop, bknight][hitbox(mouse)[1]]
                    is_pawn_promoting = False

    win.blit(board_img, (0,0))
    if is_pawn_promoting: draw_pawn_promotion(pawn_promoting)  
    draw_board(board)
    if selected_check:
        if (white_moving and is_white(board[selected[1]][selected[0]])) or (not white_moving and is_black(board[selected[1]][selected[0]])):
            draw_moves(possible_moves(moves(selected, board), selected))
    pygame.display.update()

pygame.quit()
