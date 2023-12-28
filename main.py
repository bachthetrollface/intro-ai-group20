import pygame
import chess
from time import sleep
from Board import GUI_Board
import Bot

def draw(display):
    display.fill('white')
    board.draw(display)
    pygame.display.update()

WINDOW_SIZE = (600, 600)

if __name__ == '__main__':
    Bot.initialize_openings()
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)

    board = GUI_Board(*WINDOW_SIZE)
    sequence = []
    opening = True

    running = True
    while running:
        if board.turn == chess.BLACK:
            print("Board value after player has moved:", Bot.get_board_val(board.chess_board))
            move_made = None
            if opening and len(sequence) < 6:
                move_made = Bot.opening_search(board, sequence)
            
            if move_made is None:
                move_made = Bot.minimax_search(board, 4, board.turn == chess.WHITE)
                opening = False

            status = (move_made is not None)
            if opening:
                sequence.append(move_made)
            print("Board value after bot has moved:", Bot.get_board_val(board.chess_board))
            #print(sequence)
            print("--------------------------------------")

            if not status:
                print(board.is_end_game())
                sleep(5)
                break
            draw(screen)
            sleep(0.01)
            continue
            
        if board.is_end_game() is not False:
            print(board.is_end_game())
            sleep(5)
            break
        
        mx, my = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    move_made = board.handle_click(mx, my)
                    if move_made is not None and opening: 
                        sequence.append(move_made)
        draw(screen)
        sleep(0.01)