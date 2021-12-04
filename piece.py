import pygame as p

WIDTH = HEIGHT = 600
BOARD_WIDTH = 552
DIMENSION = 8
SQ_SIZE = BOARD_WIDTH // DIMENSION
IMAGES = {}


def loadImages():
    global IMAGES
    pieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ',
              'bp', 'bR', 'bN', 'bB', 'bK', 'bQ' ]

    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load('images/' + piece + '.png'), (SQ_SIZE, SQ_SIZE))

loadImages()
    

class Piece:
    img = ''
    startX = startY = (WIDTH - BOARD_WIDTH) // 2
    
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.selected = False
        
    def all_moves(self, bo):
        pass
    
    def valid_moves(self, bo):
        pass
    
    def draw(self, screen, bo):
        board = bo.board
        image = IMAGES[self.color + self.img]
        
        x = self.startX + (self.col * SQ_SIZE)
        y = self.startY + (self.row * SQ_SIZE)
        
        if self.selected:
            p.draw.rect(screen, (0, 155, 155), p.Rect(x, y, SQ_SIZE, SQ_SIZE))
            vm = self.valid_moves(bo)
            for (xx, yy) in vm:
                xx = self.startX + (xx*SQ_SIZE)
                yy = self.startX + (yy*SQ_SIZE)
                
                sur = p.Surface((SQ_SIZE, SQ_SIZE))
                sur.set_alpha(128)
                sur.fill((0, 100, 200))
                screen.blit(sur, (xx, yy))
                
        if self.img == 'K':
            if self.inCheck:
                sur = p.Surface((SQ_SIZE, SQ_SIZE))
                sur.set_alpha(128)
                sur.fill((255, 0, 0))
                screen.blit(sur, (x, y))
                    
        screen.blit(image, (x, y))
           

        
class Pawn(Piece): 
    img = 'p'
    def __init__(self, row, col, color):
        super().__init__(row, col, color)
        self.firstMove = True
        self.promoted = False
        
    def valid_moves(self, bo):
        moves = self.all_moves(bo)
        
        l = len(moves)
        for i in range(l-1, -1, -1):
            move = moves[i]
            bo.make_move((self.row, self.col), (move[1], move[0]), calc = True)
            
            if bo.is_check(self.color):
                del moves[i]
            bo.undomove()
        
        return moves
    
    def all_moves(self, bo):
        board = bo.board
        i = self.row
        j = self.col
        
        moves = []
        # if self.color == 'g':
        #     if self.firstMove:    
        #         p = board[i+2][j]
        #         if p is None and board[i+1][j] is None:
        #             moves.append((j, i+2))
        #     if i < 7:
        #         p = board[i+1][j]
        #         if p is None:
        #             moves.append((j, i+1))
        #         if j < DIMENSION - 1 and board[i+1][j+1] is not None and board[i+1][j+1].color != self.color:
        #             moves.append((j+1, i+1))
        #         if j > 0 and board[i+1][j-1] is not None and board[i+1][j-1].color != self.color:
        #             moves.append((j-1, i+1))
        # else:
        if self.firstMove:    
            p = board[i-2][j]
            if p is None and board[i-1][j] is None:
                moves.append((j, i-2))
        if i > 0:
            p = board[i-1][j]
            if p is None:
                moves.append((j, i-1))
            if j < DIMENSION - 1 and board[i-1][j+1] is not None and board[i-1][j+1].color != self.color:
                moves.append((j+1, i-1))
            if j > 0 and board[i-1][j-1] is not None and board[i-1][j-1].color != self.color:
                moves.append((j-1, i-1))   
                
        return moves
                
    
        
class Rook(Piece): 
    img = 'R'
    
    def valid_moves(self, bo):
        moves = self.all_moves(bo)
        
        l = len(moves)
        for i in range(l-1, -1, -1):
            move = moves[i]
            bo.make_move((self.row, self.col), (move[1], move[0]), calc = True)
            
            if bo.is_check(self.color):
                del moves[i]
            bo.undomove()
        
        return moves
    
    def all_moves(self, bo):
        board = bo.board
        i = self.row
        j = self.col
        
        moves = []
        for off in range(1, DIMENSION):
            x = i + off
            y = j
            
            if 0 <= x < DIMENSION:
                if board[x][y] is None: moves.append((y, x))
                elif board[x][y].color != self.color: 
                    moves.append((y, x))
                    break
                else: break
        
        for off in range(1, DIMENSION):
            x = i - off
            y = j
            
            if 0 <= x < DIMENSION:
                if board[x][y] is None: moves.append((y, x))
                elif board[x][y].color != self.color: 
                    moves.append((y, x))
                    break
                else: break
                
        for off in range(1, DIMENSION):
            x = i 
            y = j + off
            
            if 0 <= y < DIMENSION:
                if board[x][y] is None: moves.append((y, x))
                elif board[x][y].color != self.color: 
                    moves.append((y, x))
                    break
                else: break
                
        for off in range(1, DIMENSION):
            x = i 
            y = j - off
            
            if 0 <= y < DIMENSION:
                if board[x][y] is None: moves.append((y, x))
                elif board[x][y].color != self.color: 
                    moves.append((y, x))
                    break
                else: break
    
        return moves
    
class Knight(Piece): 
    img = 'N'
    
    def valid_moves(self, bo):
        moves = self.all_moves(bo)
        
        l = len(moves)
        for i in range(l-1, -1, -1):
            move = moves[i]
            bo.make_move((self.row, self.col), (move[1], move[0]), calc = True)
            
            if bo.is_check(self.color):
                del moves[i]
            bo.undomove()
        
        return moves
    
    def all_moves(self, bo):
        board = bo.board
        i = self.row
        j = self.col
        
        moves = []
        vec = [(1, 2), (1, -2), (-1, 2), (-1, -2),
               (2, 1), (2, -1), (-2, 1), (-2, -1)]
        
        for x, y in vec:
            x = i + x
            y = j + y
            
            if 0 <= x < DIMENSION and 0 <= y < DIMENSION:
                if board[x][y] is None or board[x][y].color != self.color:
                    moves.append((y, x))
                
        return moves
    
    
class Bishop(Piece): 
    img = 'B'
    
    def valid_moves(self, bo):
        moves = self.all_moves(bo)
        
        l = len(moves)
        for i in range(l-1, -1, -1):
            move = moves[i]
            bo.make_move((self.row, self.col), (move[1], move[0]), calc = True)
            
            if bo.is_check(self.color):
                del moves[i]
            bo.undomove()
            
        return moves
    
    def all_moves(self, bo):
        board = bo.board
        i = self.row
        j = self.col
        
        moves = []
        for off in range(1, DIMENSION):
            x = i + off
            y = j + off
            if 0 <= x < DIMENSION and 0 <= y < DIMENSION:
                if board[x][y] is None or board[x][y].color != self.color:
                    moves.append((y, x))
                    if board[x][y] and board[x][y].color != self.color: break
                else: break
            else: break
            
        for off in range(1, DIMENSION):
            x = i - off
            y = j - off
            if 0 <= x < DIMENSION and 0 <= y < DIMENSION:
                if board[x][y] is None or board[x][y].color != self.color:
                    moves.append((y, x))
                    if board[x][y] and board[x][y].color != self.color: break
                else: break
            else: break
            
            
        for off in range(1, DIMENSION):
            x = i + off
            y = j - off
            if 0 <= x < DIMENSION and 0 <= y < DIMENSION:
                if board[x][y] is None or board[x][y].color != self.color:
                    moves.append((y, x))
                    if board[x][y] and board[x][y].color != self.color: break
                else: break
            else: break
            
        for off in range(1, DIMENSION):
            x = i - off
            y = j + off
            if 0 <= x < DIMENSION and 0 <= y < DIMENSION:
                if board[x][y] is None or board[x][y].color != self.color:
                    moves.append((y, x))
                    if board[x][y] and board[x][y].color != self.color: break
                else: break
            else: break
                
    
        return moves
    
    
class Queen(Piece): 
    img = 'Q'

    def valid_moves(self, bo):
        moves = self.all_moves(bo)
        
        l = len(moves)
        for i in range(l-1, -1, -1):
            move = moves[i]
            bo.make_move((self.row, self.col), (move[1], move[0]), calc = True)
            
            if bo.is_check(self.color):
                del moves[i]
            bo.undomove()
        
        return moves
    
    def all_moves(self, bo):
        board = bo.board
        i = self.row
        j = self.col
        
        moves = []
        for off in range(1, DIMENSION):
            x = i + off
            y = j + off
            if 0 <= x < DIMENSION and 0 <= y < DIMENSION:
                if board[x][y] is None or board[x][y].color != self.color:
                    moves.append((y, x))
                    if board[x][y] and board[x][y].color != self.color: break
                else: break
            else: break
            
        for off in range(1, DIMENSION):
            x = i - off
            y = j - off
            if 0 <= x < DIMENSION and 0 <= y < DIMENSION:
                if board[x][y] is None or board[x][y].color != self.color:
                    moves.append((y, x))
                    if board[x][y] and board[x][y].color != self.color: break
                else: break
            else: break
            
            
        for off in range(1, DIMENSION):
            x = i + off
            y = j - off
            if 0 <= x < DIMENSION and 0 <= y < DIMENSION:
                if board[x][y] is None or board[x][y].color != self.color:
                    moves.append((y, x))
                    if board[x][y] and board[x][y].color != self.color: break
                else: break
            else: break
            
        for off in range(1, DIMENSION):
            x = i - off
            y = j + off
            if 0 <= x < DIMENSION and 0 <= y < DIMENSION:
                if board[x][y] is None or board[x][y].color != self.color:
                    moves.append((y, x))
                    if board[x][y] and board[x][y].color != self.color: break
                else: break
            else: break
        
        for off in range(1, DIMENSION):
            x = i + off
            y = j
            
            if 0 <= x < DIMENSION:
                if board[x][y] is None: moves.append((y, x))
                elif board[x][y].color != self.color: 
                    moves.append((y, x))
                    break
                else: break
        
        for off in range(1, DIMENSION):
            x = i - off
            y = j
            
            if 0 <= x < DIMENSION:
                if board[x][y] is None: moves.append((y, x))
                elif board[x][y].color != self.color: 
                    moves.append((y, x))
                    break
                else: break
                
        for off in range(1, DIMENSION):
            x = i 
            y = j + off
            
            if 0 <= y < DIMENSION:
                if board[x][y] is None: moves.append((y, x))
                elif board[x][y].color != self.color: 
                    moves.append((y, x))
                    break
                else: break
                
        for off in range(1, DIMENSION):
            x = i 
            y = j - off
            
            if 0 <= y < DIMENSION:
                if board[x][y] is None: moves.append((y, x))
                elif board[x][y].color != self.color: 
                    moves.append((y, x))
                    break
                else: break
           
        return moves
    
    
class King(Piece): 
    img = 'K'
    
    def __init__(self, row, col, color):
        super().__init__(row, col, color)
        self.inCheck = False
    
    def valid_moves(self, bo):
        moves = self.all_moves(bo)
        
        l = len(moves)
        for i in range(l-1, -1, -1):
            move = moves[i]
            bo.make_move((self.row, self.col), (move[1], move[0]), calc = True)
            
            if bo.is_check(self.color):
                del moves[i]
            bo.undomove()
        
        return moves
    
    def all_moves(self, bo):
        board = bo.board
        i = self.row
        j = self.col
        
        moves = []
        vec = [(1, 0), (0, 1), (-1, 0), (0, -1),
               (1, 1), (1, -1), (-1, 1), (-1, -1)]
        
        for x, y in vec:
            x = i + x
            y = j + y
            if 0 <= x < DIMENSION and 0 <= y < DIMENSION:
                if board[x][y] is None or board[x][y].color != self.color: moves.append((y, x))
    
        return moves