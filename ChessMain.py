#Moving the pieces and drawing the board I think

import pygame as p
import ChessEngine

p.init()
WIDTH = HEIGHT = 512 
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}

#Intitalise a global dictonary of images. This will be called exactly once in the main

def loadImages():
    pieces = ["wp", "wQ", "wK", "wB", "wN", "wR", "bp", "bQ", "bK", "bB", "bN", "bR"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("assets/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))


def main():
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False #flag varible for when a move is made

    loadImages()
    running = True
    sqSelected = () #nosquare is selected at first. Keeps track of the last click of the user 
    playerClicks = [] #keeps track of player's clicks
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
                #mouse handler
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                if sqSelected == (row, col): #if the user clicks the smae square twice
                    sqSelected = ()
                    playerClicks =[]
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected)
                if len(playerClicks) == 2 :
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                    print(playerClicks)
                    print(move.getChessNotation())
                    if move in validMoves:
                        gs.makeMove(move)
                        moveMade = True

                    sqSelected = () #reset clicks
                    playerClicks = []
                #key handler
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z: #undo when 'z' is pressed
                    gs.undoMove()
                    moveMade = True

        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False

                

        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()

def drawGameState(screen, gs):
    drawBoard(screen) #drawing the squares on the board
    drawPieces(screen, gs.board) #drawing the pieces onto the squares

#draw squares. The topleft square is always light
def drawBoard(screen):
    colors = [p.Color("white"), p.Color("blue")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c) % 2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))



#draw the pieces on the board using the current GameState.board
def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--": #not empty square
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

if __name__ == "__main__":
    main()