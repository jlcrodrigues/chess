import pygame
from functions import *
from config import *

pygame.init()
pygame.display.set_caption("Chess")

run = True
while run:
    pygame.time.delay(27)
    click = pygame.mouse.get_pressed()
    mouse = pygame.mouse.get_pos()    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not is_pawn_promoting:
                ######### buttons
                if 80 <= mouse[0] <= 112 and 592 <= mouse[1] <= 624: restart_game = True #restart
                if 144 <= mouse[0] <= 176 and 592 <= mouse[1] <= 624: rotated = not rotated #rotate the board
                if 208 <= mouse[0] <= 240 and 592 <= mouse[1] <= 624 and move > 0: #go back a move
                    move -= 1
                    board = copy_board(board_history[move])
                    white_moving = not white_moving
                if 272 <= mouse[0] <= 304 and 592 <= mouse[1] <= 624 and move < len(board_history) - 1: #advance a move.
                    move += 1
                    board = copy_board(board_history[move])
                    white_moving = not white_moving
                if not inside_board(mouse): continue
                square = hitbox(mouse, rotated)
                if selected_check and square != selected and square in possible_moves(moves(selected, board), selected, board): #select the square to move to
                    if (white_moving and is_white(board[selected[1]][selected[0]])) or (not white_moving and is_black(board[selected[1]][selected[0]])):
                        new = square
                        for (x,y) in [(x,y) for x in range(8) for y in range(8)]:
                            previous_board[y][x] = board[y][x]
                        board[new[1]][new[0]] = board[selected[1]][selected[0]]
                        board[selected[1]][selected[0]] = 0
                        move += 1
                        board_history[move] = copy_board(board)
                        for i in range(move + 1, len(board_history)): #when a move is redone, all next moves deleted
                            board_history.pop(i)
                        selected_check = False
                        white_moving = not white_moving #changes turns
                        #########pawn promotion
                        if board[new[1]][new[0]] == wpawn and new[1] == 0: 
                            is_pawn_promoting = True
                            pawn_promoting = new
                        if board[new[1]][new[0]] == bpawn and new[1] == 7:
                            is_pawn_promoting = True
                            pawn_promoting = new
                        #########castling
                        if board[new[1]][new[0]] == wking and new == (2,7) and wcastle[0]: (board[7][3], board[7][0]) = (wrook, 0)
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
                        #########en passant
                        if previous_board[selected[1]][selected[0]] == wpawn and board[new[1] + 1][new[0]] == bpawn and previous_board[new[1]][new[0]] == 0:
                            board[new[1] + 1][new[0]] = 0
                        if previous_board[selected[1]][selected[0]] == bpawn and board[new[1] - 1][new[0]] == wpawn and previous_board[new[1]][new[0]] == 0:
                            board[new[1] - 1][new[0]] = 0
                        #########board evaluation
                        if check(board):
                            if checkmate(board) != '':
                                checkmated = True
                else: #select a piece to move
                    selected = square
                    if board[selected[1]][selected[0]] != 0: selected_check = True
                    else: selected_check = False
            else: #handles events while a pawn is promoting
                hit = hitbox(mouse, rotated)
                y = hit[1]
                print(hit)
                if hit[0] == -1 and is_white(board[pawn_promoting[1]][pawn_promoting[0]]) and 0 <= hit[1] <= 3:
                    if rotated: y = 3 - y
                    else: y -= 4
                    board[pawn_promoting[1]][pawn_promoting[0]] = [wqueen, wrook, wbishop, wknight][y]
                    is_pawn_promoting = False
                if hit[0] == 8 and is_black(board[pawn_promoting[1]][pawn_promoting[0]]) and 4 <= hit[1] <= 7:
                    if rotated: y = 7 - y
                    else: y -= 4
                    board[pawn_promoting[1]][pawn_promoting[0]] = [bqueen, brook, bbishop, bknight][y]
                    is_pawn_promoting = False

    win.blit(board_img, (0,0))
    if is_pawn_promoting: draw_pawn_promotion(win, pawn_promoting)
    if selected_check:
        if find_side(board[selected[1]][selected[0]]) == find_turn(white_moving):
            if rotated: pygame.draw.rect(win, (47, 68, 77), (64 + (7 - selected[0]) * 64, 64 + (7 - selected[1]) * 64, 64, 64))
            else: pygame.draw.rect(win, (47, 68, 77), (64 + selected[0] * 64, 64 + selected[1] * 64, 64, 64))
        if (white_moving and is_white(board[selected[1]][selected[0]])) or (not white_moving and is_black(board[selected[1]][selected[0]])):
            draw_moves(win, possible_moves(moves(selected, board), selected, board), selected, board, rotated)
    if check(board) != '':
        king = find_king(check(board), board)
        if rotated: king = (7 - king[0], 7 - king[1])
        pygame.draw.rect(win, (236, 62, 19), (king[0] * 64 + 64, king[1]* 64 + 64, 64, 64))
    draw_buttons(win)
    draw_board(win, board, rotated)
    pygame.display.update()

    if checkmated:
        pygame.time.delay(3000)
        restart_game = True
        checkmated = False

    if restart_game:
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
        new_board = [[0,0,0,0,0,0,0,0] for _ in range(8)]
        restart_game = False
        
pygame.quit()
