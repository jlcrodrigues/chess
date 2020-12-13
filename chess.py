import pygame

pygame.init()

win = pygame.display.set_mode((640,640))

board_img = pygame.image.load("imgs/board.png")
(wpawn, bpawn) = (pygame.image.load("imgs/wpawn.png"),pygame.image.load("imgs/bpawn.png"))
(wknight, bknight) = (pygame.image.load("imgs/wknight.png"),pygame.image.load("imgs/bknight.png"))
(wbishop, bbishop) = (pygame.image.load("imgs/wbishop.png"),pygame.image.load("imgs/bbishop.png"))
(wrook, brook) = (pygame.image.load("imgs/wrook.png"),pygame.image.load("imgs/brook.png"))
(wqueen, bqueen) = (pygame.image.load("imgs/wqueen.png"),pygame.image.load("imgs/bqueen.png"))
(wking, bking) = (pygame.image.load("imgs/wking.png"),pygame.image.load("imgs/bking.png"))

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
