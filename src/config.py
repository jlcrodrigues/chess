import pygame

win = pygame.display.set_mode((640,640))

#defines initial variables

selected_check = False
is_pawn_promoting = False
white_moving = True
wcastle = [True, True]
bcastle = [True, True]
holding = False
checkmated = False
restart_game = False
rotated = False
menu = True

menu_img = pygame.image.load("../assets/menu.png")
board_img = pygame.image.load("../assets/board.png")
target = pygame.image.load("../assets/target.png")
cross = pygame.image.load("../assets/cross.png")
rotate = pygame.image.load("../assets/rotate.png")
arrow_backwards = pygame.image.load("../assets/arrow_backwards.png")
arrow_forward = pygame.image.load("../assets/arrow_forward.png")
return_menu = pygame.image.load("../assets/return.png")
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

board = [[brook, bknight, bbishop, bqueen, bking, bbishop, bknight, brook],
        [bpawn, bpawn, bpawn, bpawn, bpawn, bpawn, bpawn, bpawn],
        [0, brook, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [wrook, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [wrook, 0, 0, 0, wking, 0, 0, wrook]] 

new_board = [[0,0,0,0,0,0,0,0] for _ in range(8)]
previous_board = [[0,0,0,0,0,0,0,0] for _ in range(8)]
board_history = {}
prev_board = [[0,0,0,0,0,0,0,0] for _ in range(8)]
for (x,y) in [(x,y) for x in range(8) for y in range(8)]:
    prev_board[y][x] = board[y][x]
move = 0
board_history[move] = prev_board

