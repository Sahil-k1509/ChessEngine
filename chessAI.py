from random import randint, choice, shuffle

pieceScore = {
    'K': 0,
    'Q': 90,
    'R': 50,
    'B': 30,
    'N': 30,
    'p': 10 
}
CHECKMATE = 1000
STALEMATE = 0
CHECK = 20

class MoveFinder:
    
    @staticmethod
    def randomMove(bo):
        '''
        Out of all valid moves, return a move at random.
        If no valid moves, return None.
        '''
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
        '''
        Find the score of board based on pieces.
        '''
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
        '''
        Choose the current best move greedily. If all moves are equivalent choose a random move.
        '''
        turnMultiplier = 1 if bo.turn == 'w' else -1
        
        maxScore = MoveFinder.find_score(bo)*turnMultiplier
        bestMove = None
        effective = False
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
                            effective = True
                        
                        bo.undomove()
        
        if bestMove is None:
            return MoveFinder.randomMove(bo)
        if not effective:
            return MoveFinder.randomMove(bo)
        
        return bestMove
    
    
    @staticmethod
    def miniMaxSmall(bo):
        '''
        Iterative minimax Algorithm that looks one move ahead.
        '''
        turnMultiplier = 1 if bo.turn == 'w' else -1
        
        # opponentMinMaxScore = MoveFinder.find_score(bo)*turnMultiplier
        opponentMinMaxScore = CHECKMATE
        bestMove = None
        opponent_color = 'w' if bo.turn == 'b' else 'b'
        
        playerMoves = bo.generate_valid_moves(bo.turn)
        shuffle(playerMoves)
        for playerMove in playerMoves:
            bo.make_move(playerMove[0], playerMove[1], calc = True)
            opponent_moves = bo.generate_valid_moves(opponent_color)
            shuffle(opponent_moves)
            
            # opponentMaxScore = MoveFinder.find_score(bo)*turnMultiplier
            opponentMaxScore = -CHECKMATE
            for oppMove in opponent_moves:
                bo.make_move(oppMove[0], oppMove[1], calc = True)
                if bo.is_checkmate(bo.turn):
                    score = -CHECKMATE*turnMultiplier
                elif bo.is_stalemate(bo.turn):
                    score = STALEMATE
                elif bo.is_check(bo.turn):
                    score = -CHECK*turnMultiplier
                else:
                    score = -MoveFinder.find_score(bo)*turnMultiplier
                    
                if score > opponentMaxScore:
                    opponentMaxScore = score        
                bo.undomove()
            
            if  opponentMaxScore < opponentMinMaxScore:
                opponentMinMaxScore = opponentMaxScore
                bestMove = playerMove     
            
            bo.undomove()
                    
        
        if bestMove is None:
            return MoveFinder.randomMove(bo)
        
        return bestMove