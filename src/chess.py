import pygame
from random import choice
from functions import *
from config import *
from bot import Bot

pygame.init()
pygame.display.set_caption("Chess")
bot = Bot()
clock = pygame.time.Clock()

run = True
while run:
    clock.tick(60)
    click = pygame.mouse.get_pressed()
    mouse = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if menu:
                if 220 <= mouse[0] <= 420 and 275 <= mouse[1] <= 315: #1 player mode
                    (menu, multiplayer, turn) = (False, False, choice([True, False]))
                    rotated = not turn
                if 220 <= mouse[0] <= 420 and 350 <= mouse[1] <= 385: (menu, multiplayer) = (False, True) #2 player mode
            else:
                menu = False
                ######### buttons
                if 16 <= mouse[0] <= 48 and 16 <= mouse[1] <= 48: #return to menu
                        menu = True
                        restart_game = True
                if 80 <= mouse[0] <= 112 and 592 <= mouse[1] <= 624: restart_game = True #restart
                if 144 <= mouse[0] <= 176 and 592 <= mouse[1] <= 624: rotated = not rotated #rotate the board
                if 208 <= mouse[0] <= 240 and 592 <= mouse[1] <= 624 and move > 0: #go back a move
                    move -= 1
                    if not multiplayer: move -= 1
                    board = copy_board(board_history[move])
                    if multiplayer: white_moving = not white_moving
                if 272 <= mouse[0] <= 304 and 592 <= mouse[1] <= 624 and move < len(board_history) - 1: #advance a move.
                    move += 1
                    if not multiplayer: move += 1
                    board = copy_board(board_history[move])
                    if multiplayer: white_moving = not white_moving
                if not is_pawn_promoting:
                    if not inside_board(mouse): continue
                    square = hitbox(mouse, rotated)
                    if selected_check and square != selected and square in possible_moves(moves(selected, board), selected, board, wcastle, bcastle): #select the square to move to
                        if (white_moving and is_white(board[selected[1]][selected[0]])) or (not white_moving and is_black(board[selected[1]][selected[0]])):
                            new = square
                            play_move = True
                    elif multiplayer or turn: #select a piece to move
                        selected = square
                        if board[selected[1]][selected[0]] != 0: selected_check = True
                        else: selected_check = False
                else: #handles events while a pawn is promoting
                    hit = hitbox(mouse, rotated)
                    y = hit[1]
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
                    move += 1
                    board_history[move] = copy_board(board)
                    for i in range(move + 1, len(board_history)): #when a move is redone, all next moves are deleted
                        board_history.pop(i)

    if not multiplayer and not is_pawn_promoting:
        if not turn:
            prev_board = copy_board(board)
            chosen = bot.play(prev_board, white_moving, wcastle, bcastle)
            if chosen != False:
                play_move = True
                selected = chosen[0]
                new = chosen[1]

    if play_move:
        if not multiplayer: turn = not turn
        play_move = False
        for (x,y) in [(x,y) for x in range(8) for y in range(8)]:
            previous_board[y][x] = board[y][x]
        board[new[1]][new[0]] = board[selected[1]][selected[0]]
        board[selected[1]][selected[0]] = 0
        move += 1
        board_history[move] = copy_board(board)
        for i in range(move + 1, len(board_history)): #when a move is redone, all next moves are deleted
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
        c = [False, False]
        if board[new[1]][new[0]] == wking and new == (0,7) and wcastle[0]: (board[7][3], board[7][0], board[7][2], c[0]) = (wrook, 0, wking, True)
        if board[new[1]][new[0]] == wking and new == (7,7) and wcastle[1]: (board[7][5], board[7][7], board[7][6], c[0]) = (wrook, 0, wking, True)
        if board[new[1]][new[0]] == bking and new == (0,0) and bcastle[0]: (board[0][3], board[0][0], board[0][2], c[1]) = (brook, 0, bking, True)
        if board[new[1]][new[0]] == bking and new == (7,0) and bcastle[1]: (board[0][5], board[0][7], board[0][6], c[1]) = (brook, 0, bking, True)
        if c[0]: wcastle = [False, False]
        if c[1]: bcastle = [False, False]
        if board[new[1]][new[0]] == wrook:
            if selected == (0,7): wcastle[0] = False
            if selected == (7,7): wcastle[1] = False
        if board[new[1]][new[0]] == brook:
            if selected == (0,0): bcastle[0] = False
            if selected == (7,0): bcastle[1] = False
        if selected == (4,7): wcastle = [False, False]
        if selected == (4,0): bcastle = [False, False]
        #########en passant
        if previous_board[selected[1]][selected[0]] == wpawn and board[new[1] + 1][new[0]] == bpawn and previous_board[new[1]][new[0]] == 0:
            board[new[1] + 1][new[0]] = 0
        if previous_board[selected[1]][selected[0]] == bpawn and board[new[1] - 1][new[0]] == wpawn and previous_board[new[1]][new[0]] == 0:
            board[new[1] - 1][new[0]] = 0
        #########board evaluation
        '''
        if check(board):
            if checkmate(board) != '':
                checkmated = True
        '''

    if menu:
        win.blit(menu_img, (0,0))
    else:
        win.blit(board_img, (0,0))
        if is_pawn_promoting: draw_pawn_promotion(win, pawn_promoting)
        if selected_check:
            if find_side(board[selected[1]][selected[0]]) == find_turn(white_moving):
                if rotated: pygame.draw.rect(win, (47, 68, 77), (64 + (7 - selected[0]) * 64, 64 + (7 - selected[1]) * 64, 64, 64))
                else: pygame.draw.rect(win, (47, 68, 77), (64 + selected[0] * 64, 64 + selected[1] * 64, 64, 64))
            if (white_moving and is_white(board[selected[1]][selected[0]])) or (not white_moving and is_black(board[selected[1]][selected[0]])):
                draw_moves(win, possible_moves(moves(selected, board), selected, board, wcastle, bcastle), selected, board, rotated)
        if check(board) != '':
            king = find_king(check(board), board)
            if rotated: king = (7 - king[0], 7 - king[1])
            pygame.draw.rect(win, (236, 62, 19), (king[0] * 64 + 64, king[1]* 64 + 64, 64, 64))
        draw_buttons(win)
        draw_board(win, board, rotated)
    pygame.display.update()

    '''
    if checkmated:
        pygame.time.delay(3000)
        restart_game = True
        checkmated = False
    '''
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
        board_history = {}
        move = 0
        
pygame.quit()
