
#Game logic/storing the current state of the game


class GameState():
    def __init__(self):
        #the board is a 8x8 2D list
        #each element of the list is 2 characters. 
        #The first letter of the list represnts the colour, the second letter is the type of piece.
        #The -- is the empty space in the middle.
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp","bp","bp","bp","bp","bp","bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp","wp","wp","wp","wp","wp","wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]
        self.whiteToMove = True
        self.moveLog = []

#Takes a move as as parameter and executes it (this will not work for en passant, castling, and pawn promotion)
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--" #replace piece move with empty space
        self.board[move.endRow][move.endCol] = move.pieceMoved #moving the piece
        self.moveLog.append(move) #keeps track of move
        self.whiteToMove = not self.whiteToMove #switch turn

    def undoMove(self):
        if len(self.moveLog) != 0: #makes sure it's not the first move
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove #swap players

#All moves considering checks
    def getValidMoves(self):
        return self.getAllPossibleMoves()


#all moves without considering checks
    def getAllPossibleMoves(self):
        moves = [Move ( (6,4), (4,4), self.board)]
        for r in range(len(self.board)): #number of rows
            for c in range (len(self.board[r])): #number of columns in given row
                turn = self.board[r][c][0] #it will be 'w', 'b' or '-'
                if (turn == 'w' and self.whiteToMove) and (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1] #it will be be a possible piece or a '-'s
                    if piece == 'p':
                        self.getPawnMove(r, c, moves)
                    elif piece == 'R':
                        self.getRookMove (r, c, moves)
        return moves

    def getPawnMove(self, r, c, moves): #checks all the possible moves the pawn can make in the r,c and add these tp the list
        pass

    def getRookMove(self, r, c, moves): #checks all the possible moves the rook can make in the r,c and add these tp the list
        pass


class Move():
    #map keys to values
    #key : value
    ranksToRows = {"1":7, "2":6, "3":5, "4":4, "5":3, "6":2, "7":1, "8":0}
    rowsToRanks = {v : k for k, v in ranksToRows.items()}
    filesToCols = {"a" : 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol
        print(self.moveID)

#Overiding the equals method
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False


    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]
 