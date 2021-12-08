from random import randint, choice

pieceScore = {
    'K': 0,
    'Q': 9,
    'R': 5,
    'B': 3,
    'N': 3,
    'p': 1 
}
CHECKMATE = 1000
STALEMATE = 0
CHECK = 100

class MoveFinder:
    
    @staticmethod
    def randomMove(bo):
        cutoff = 80
        anyvalidmove = False
        while True:
            for i in range(8):
                for j in range(8):
                    if bo.board[i][j] is None: continue
                    if bo.board[i][j].color == bo.turn:
                        validmoves = bo.board[i][j].valid_moves(bo)
                        # print(validmoves)
                        if validmoves:
                            anyvalidmove = True
                            if randint(10, 100) >= cutoff:
                                randomMove = choice(validmoves)
                                # print((i, j), randomMove)
                                return [(i, j), (randomMove[1], randomMove[0])]
                        else:
                            cutoff -= 10
                            
            if not anyvalidmove:
                return None
    
    @staticmethod   
    def find_score(bo):
        score = 0
        board = bo.board
        for i in range(8):
            for j in range(8):
                if board[i][j] is None: continue
                if board[i][j].color == 'w':
                    score += pieceScore[board[i][j].img]
                else:
                    score -= pieceScore[board[i][j].img]
                    
        return score
    
    @staticmethod
    def greedyMove(bo):
        turnMultiplier = 1 if bo.turn == 'w' else -1
        
        maxScore = -CHECKMATE
        bestMove = None
        for i in range(8):
            for j in range(8):
                if bo.board[i][j] is None: continue
                if bo.board[i][j].color == bo.turn:
                    validmoves = bo.board[i][j].valid_moves(bo)
                    for move in validmoves:
                        opp_color = 'w' if bo.board[i][j].color == 'b' else 'b'
                        bo.make_move((i, j), (move[1], move[0]), calc=True)
                        if bo.is_checkmate(opp_color):
                            score = CHECKMATE
                        elif bo.is_stalemate(opp_color):
                            score = STALEMATE
                        elif bo.is_check(opp_color):
                            score = CHECK
                        else:
                            score = MoveFinder.find_score(bo)*turnMultiplier
                        
                        if score > maxScore:
                            maxScore = score
                            bestMove = [(i, j), (move[1], move[0])]
                        bo.undomove()
                        
        return bestMove