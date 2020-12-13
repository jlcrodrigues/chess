import pygame

pygame.init()

win = pygame.display.set_mode((640,640))

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
[0, 0, 0, bqueen, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0],
[wpawn, wpawn, wpawn, wpawn, wpawn, wpawn, wpawn, wpawn],
[wrook, wknight, wbishop, wqueen, wking, wbishop, wknight, wrook]]

def draw_board(board):
    for i in range(8):
        for j in range(8):
            if board[i][j] != 0: win.blit(board[i][j], (64 + 64*j, 64 + 64*i))

run = True
while run:
    pygame.time.delay(27)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    
    
    win.blit(board_img, (0,0))
    
    draw_board(board)
    pygame.display.update()

pygame.quit()
