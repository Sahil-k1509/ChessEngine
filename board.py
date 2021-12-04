import pygame as p
from piece import Pawn, Rook, Knight, Bishop, Queen, King

class Board:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        
        self.rep = [
            ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
            ['bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp'],
            ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR'],
        ]
        
        self.board = [[None for _ in range(cols)] for _ in range(rows)]
        
        change = {'p': Pawn, 'R': Rook, 'N': Knight, 'B': Bishop, 'Q': Queen, 'K': King}
        for i in range(rows):
            for j in range(cols):
                if self.rep[i][j] != '--':
                    self.board[i][j] = change[self.rep[i][j][1]](i, j, self.rep[i][j][0])
                    
        self.movelog = []
        self.movelogcomp = []
        self.turn = 'w'
        
    def reset_board(self):
        change = {'p': Pawn, 'R': Rook, 'N': Knight, 'B': Bishop, 'Q': Queen, 'K': King}
        for i in range(self.rows):
            for j in range(self.cols):
                if self.rep[i][j] != '--':
                    self.board[i][j] = change[self.rep[i][j][1]](i, j, self.rep[i][j][0])
                else:
                    self.board[i][j] = None
                    
        self.movelog = []
        self.movelogcomp = []
        self.turn = 'w'
                    
        
    def draw(self, screen):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] is not None:
                    self.board[i][j].draw(screen, self)
                    
    def unselectall(self):
        for i in range(8):
            for j in range(8):
                if self.board[i][j]: self.board[i][j].selected = False
                    
    def select(self, row, col):
        self.unselectall()
        if self.board[row][col] is not None and self.board[row][col].color == self.turn:
            self.board[row][col].selected = True
            return (row, col)
        return (None, None)
    
    def rotate_board(self):
        self.board = self.board[::-1]
        for i in range(8):
            self.board[i] = self.board[i][::-1]
            
        for i in range(8):
            for j in range(8):
                if self.board[i][j] is not None:
                    self.board[i][j].row = i
                    self.board[i][j].col = j
                    
    def chess_notation(self, row, col):
        if self.turn == 'w':
            alp = chr(col + ord('a')) 
            num = 8 - row
            return f'{alp}{num}'
        else:
            num = row + 1
            alp = chr(ord('h') - col)
            return f'{alp}{num}'
        
    def make_move(self, start, end, calc = False):
        self.move(start, end, calc)
        if not calc:
            self.unselectall()
            print(self.chess_notation(start[0], start[1]), end=' -> ')
            print(self.chess_notation(end[0], end[1]))
        self.rotate_board()
            
    def move(self, start, end, calc = False):
        removed = self.board[end[0]][end[1]]
        self.board[end[0]][end[1]] = self.board[start[0]][start[1]]
        self.board[start[0]][start[1]] = None
        self.board[end[0]][end[1]].row = end[0]
        self.board[end[0]][end[1]].col = end[1]
        
        if self.board[end[0]][end[1]].img == 'p' and not calc: 
            self.board[end[0]][end[1]].firstMove = False
        
        color = self.board[end[0]][end[1]].color
        opp_color = 'w' if color == 'b' else 'b'
        
        in_check = self.is_check(color)
        x, y = self.find_king(color)
        if not calc: 
            self.board[x][y].inCheck = in_check
        
        in_check = self.is_check(opp_color)
        x, y = self.find_king(opp_color)
        if not calc: 
            self.board[x][y].inCheck = in_check
            
        
        self.turn = 'b' if self.turn == 'w' else 'w'
        self.movelog.append([start, end, removed])
        
        return removed
    
    def undomove(self):
        if self.movelog:
            start, end, removed = self.movelog.pop()
            self.rotate_board()
            self.board[start[0]][start[1]] = self.board[end[0]][end[1]]
            self.board[end[0]][end[1]] = removed
            
            if removed is not None:
                self.board[end[0]][end[1]].row = end[0]
                self.board[end[0]][end[1]].col = end[1]
                
            self.board[start[0]][start[1]].row = start[0]
            self.board[start[0]][start[1]].col = start[1]
            self.turn = 'b' if self.turn == 'w' else 'w'
            
            in_check = self.is_check('w')
            x, y = self.find_king('w')
            self.board[x][y].inCheck = in_check
            
            in_check = self.is_check('b')
            x, y = self.find_king('b')
            self.board[x][y].inCheck = in_check
        
    def find_king(self, color):
        for i in range(8):
            for j in range(8):
                if self.board[i][j] is None: continue
                if self.board[i][j].color == color and self.board[i][j].img == 'K':
                    return (i, j)
                
    def is_checkmate(self, color):
        for i in range(8):
            for j in range(8):
                if self.board[i][j] is None: continue
                if self.board[i][j].color == color:
                    validmoves = self.board[i][j].valid_moves(self)
                    if validmoves: return False
                    
        if self.is_check(color):
            return True
        
        return False
            
    def is_check(self, color):
        opp_color = 'w' if color == 'b' else 'b'
        check = False
        
        for i in range(8):
            for j in range(8):
                if self.board[i][j] is None: continue
                if self.board[i][j].color == opp_color:
                    validmoves = self.board[i][j].all_moves(self)
                    for (y, x) in validmoves:
                        if self.board[x][y] is None: continue
                        if self.board[x][y].img == 'K' and self.board[x][y].color == color:
                            check = True
                            break
                if check: break
            if check: break
        
        return (check)
                
        
            