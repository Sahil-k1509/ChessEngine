import pygame as p
import os
from board import Board


WIDTH = HEIGHT = 600
BOARD_WIDTH = 552
DIMENSION = 8
SQ_SIZE = BOARD_WIDTH // DIMENSION
startX = startY = (WIDTH - BOARD_WIDTH) // 2
FPS = 15
bo = Board(DIMENSION, DIMENSION)


def drawboard(screen):
    '''
    Draw the checkered pattern chess board.
    '''
    colors = [p.Color(232, 235, 239), p.Color(125, 135, 150)]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[(r+c)&1]
            p.draw.rect(screen, color, p.Rect(startX + c*SQ_SIZE, startY + r*SQ_SIZE, SQ_SIZE, SQ_SIZE))


def end_screen(bo, screen):
    '''
    Check if the game has ended and display the text on screen.
    '''
    font = p.font.SysFont('Arial', 20)
    
    whitecm = font.render('White Checkmated. (R to restart)', True, (0, 0, 0))
    blackcm = font.render('Black Checkmated. (R to restart)', True, (0, 0, 0))
    whitesm = font.render('White Stalemated. (R to restart)', True, (0, 0, 0))
    blacksm = font.render('Black Stalemated. (R to restart)', True, (0, 0, 0))
    
    if bo.is_checkmate('w'): screen.blit(whitecm, (150, 285))
    elif bo.is_checkmate('b'): screen.blit(blackcm, (150, 285))
    elif bo.is_stalemate('w'): screen.blit(whitesm, (150, 285))
    elif bo.is_stalemate('b'): screen.blit(blacksm, (150, 285))
    

def redraw_gamewindow(screen):
    '''
    Draw board, add pieces and update screen.
    '''
    global bo
    drawboard(screen)
    bo.draw(screen)
    end_screen(bo, screen)
    
    p.display.update()
    
    
def click(pos):
    '''
    return index of cell on board given mouse click.
    '''
    x, y = pos
    row, col = -1, -1
    if startX < x < startX + BOARD_WIDTH:
        if startY < y < startY + BOARD_WIDTH:
            x -= startX
            y -= startY
            row = y // SQ_SIZE
            col = x // SQ_SIZE
            
    # print(row, col)
    return (row, col)
        

def main():
    print("Select Game Mode:\n(1) Against Computer\n(2) Against Player")
    gamemode = input()
    if gamemode == '1': gamemode = int(gamemode)
    else: gamemode = 2
    
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    p.display.set_caption('Chess Game')
    
    clock = p.time.Clock()
    screen.fill(p.Color(59, 1, 60))
    
    
    running = True
    start = (None, None)
    while running:
        redraw_gamewindow(screen)
        
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
                break
            if e.type == p.KEYDOWN:
                if e.key == p.K_z and gamemode == 2:
                    bo.undomove()
                    start = (None, None)
                if e.key == p.K_r:
                    bo.reset_board()
                    start = (None, None)
                    
            if e.type == p.MOUSEBUTTONDOWN:
                '''
                # If the click is outside board unselect all pieces
                # If there is no piece already selected, then select this one.
                # Otherwise if the cell is in valid moves, move the piece.
                # Otherwise unselect the piece or select other piece.
                '''
                pos = p.mouse.get_pos()
                row, col = click(pos)
                
                if (row, col) != (-1, -1):
                    if start != (None, None):
                        if (col, row) in bo.board[start[0]][start[1]].valid_moves(bo):
                            if gamemode == 2:
                                bo.make_move(start, (row, col))
                            else:
                                bo.make_move_computer(start, (row, col))
                            start = (None, None)    
                        else: start = bo.select(row, col)
                    else: start = bo.select(row, col)
                else: bo.unselectall()
                        
            
        clock.tick(FPS)
        p.display.flip()
        
    p.quit()
    
    
if __name__ == "__main__":
    main()