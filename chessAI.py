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
            for i in range(bo.rows):
                for j in range(bo.cols):
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
        Positive score is good for white.
        '''
        score = 0
        board = bo.board
        for i in range(bo.rows):
            for j in range(bo.cols):
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
        for i in range(bo.rows):
            for j in range(bo.cols):
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
                score = 0
                if bo.is_checkmate(bo.turn):
                    score = -CHECKMATE*turnMultiplier
                elif bo.is_stalemate(bo.turn):
                    score = STALEMATE
                elif bo.is_check(bo.turn):
                    score = -CHECK*turnMultiplier
                
                score += -MoveFinder.find_score(bo)*turnMultiplier
                    
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
    
    
    @staticmethod   
    def scoreBoard(bo):
        '''
        Improved method to find score.
        '''
        if bo.is_checkmate('w'): return -CHECKMATE
        if bo.is_checkmate('b'): return CHECKMATE
        if bo.is_stalemate('w') or bo.is_stalemate('b'): return STALEMATE
        
        score = 0
        board = bo.board
        for i in range(bo.rows):
            for j in range(bo.cols):
                if board[i][j] is None: continue
                if board[i][j].color == 'w':
                    score += pieceScore[board[i][j].img]
                else:
                    score -= pieceScore[board[i][j].img]
                    
        return score
    
    @staticmethod
    def miniMax(bo):
        nextMove = None
        maxDepth = 2

        def miniMaxHelper(bo, depth, whiteToMove):
            nonlocal nextMove, maxDepth
            if depth == 0:
                return MoveFinder.scoreBoard(bo)
            
            if whiteToMove:
                maxScore = -CHECKMATE
                validmoves = bo.generate_valid_moves('w')
                shuffle(validmoves)
                for move in validmoves:
                    bo.make_move(move[0], move[1], calc = True)
                    score = miniMaxHelper(bo, depth - 1, False)
                    if score > maxScore:
                        maxScore = score
                        if depth == maxDepth:
                            nextMove = move
                    bo.undomove(calc = True)
                return maxScore
            else:
                minScore = CHECKMATE
                validmoves = bo.generate_valid_moves('b')
                shuffle(validmoves)
                for move in validmoves:
                    bo.make_move(move[0], move[1], calc = True)
                    score = miniMaxHelper(bo, depth - 1, True)
                    if score < minScore:
                        minScore = score
                        if depth == maxDepth:
                            nextMove = move
                    bo.undomove(calc = True)
                return minScore         
            
        whiteToMove = (bo.turn == 'w')
        miniMaxHelper(bo, maxDepth, whiteToMove)
        if nextMove is None:
            return MoveFinder.randomMove(bo)
        
        return nextMove