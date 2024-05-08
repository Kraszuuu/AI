import Board

START_BOARD = [
        [1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0],
        [1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0],
        [1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0],
        [1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,2],
        [0,0,0,0,0,0,0,0,0,0,0,0,2,2,2,2],
        [0,0,0,0,0,0,0,0,0,0,0,2,2,2,2,2],
        [0,0,0,0,0,0,0,0,0,0,0,2,2,2,2,2]
    ]

#16 moves possible
INDIRECT_BOARD1 = [
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
]

#26 moves possible
INDIRECT_BOARD2 = [
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
]


class Node:
    def __init__(self, board : Board, parent : 'Node' = None) -> None:
        self.board : Board = board
        self.value : int = board.value
        self.children : list[Node] = []
        self.parent : Node = parent
        self.currentPlayer : int = parent.currentPlayer % 2 + 1 if parent != None else 1

    # Creates all kinds of movement
    def generateMoves(self):
        # Creates direct moves (movements in 8 possible directions)
        def generateDirectMoves(givenBoard : Board, allPieces : list):
            def checkMoves(x : int, y : int, currentBoard : Board):
                currentBoardState = currentBoard.boardState
                #Top
                if y > 0:
                    #Left
                    if x > 0 and currentBoardState[y-1][x-1] == 0:
                        fixedBoardState = createFixedBoardState(x, y, x-1, y-1, givenBoard)
                        createKid(self, fixedBoardState)
                    #Mid
                    if currentBoardState[y-1][x] == 0:
                        fixedBoardState = createFixedBoardState(x, y, x, y-1, givenBoard)
                        createKid(self, fixedBoardState)
                    #Right
                    if x < 15 and currentBoardState[y-1][x+1] == 0:
                        fixedBoardState = createFixedBoardState(x, y, x+1, y-1, givenBoard)
                        createKid(self, fixedBoardState)
                #Mid Left
                if x > 0 and currentBoardState[y][x-1] == 0:
                    fixedBoardState = createFixedBoardState(x, y, x-1, y, givenBoard)
                    createKid(self, fixedBoardState)
                #Mid Right
                if x < 15 and currentBoardState[y][x+1] == 0:
                    fixedBoardState = createFixedBoardState(x, y, x+1, y, givenBoard)
                    createKid(self, fixedBoardState)
                #Bot 
                if y < 15:
                    #Left
                    if x > 0 and currentBoardState[y+1][x-1] == 0:
                        fixedBoardState = createFixedBoardState(x, y, x-1, y+1, givenBoard)
                        createKid(self, fixedBoardState)
                    #Mid
                    if currentBoardState[y+1][x] == 0:
                        fixedBoardState = createFixedBoardState(x, y, x, y+1, givenBoard)
                        createKid(self, fixedBoardState)
                    #Right
                    if x < 15 and currentBoardState[y+1][x+1] == 0:
                        fixedBoardState = createFixedBoardState(x, y, x+1, y+1, givenBoard)
                        createKid(self, fixedBoardState)

            for piece in allPieces:
                x = piece[1]
                y = piece[0]
                checkMoves(x, y, givenBoard)

        # Creates indirect moves (moves that include jumping over other pieces)
        def generateIndirectMoves(givenBoard : Board, allPieces : list):
            def checkMoves(x : int, y : int, lastPosition : tuple, currentBoard : Board):
                currentBoardState = currentBoard.boardState
                #Top
                if y > 1:
                    #Left
                    if x > 1 and currentBoardState[y-1][x-1] != 0 and currentBoardState[y-2][x-2] == 0 and lastPosition != (x-2,y-2):
                        fixedBoardState = createFixedBoardState(x, y, x-2, y-2, currentBoard)
                        fixedBoard = createKid(self, fixedBoardState)
                        checkMoves(x-2, y-2, (x,y), fixedBoard)
                    #Mid
                    if currentBoardState[y-1][x] != 0 and currentBoardState[y-2][x] == 0 and lastPosition != (x, y-2):
                        fixedBoardState = createFixedBoardState(x, y, x, y-2, currentBoard)
                        fixedBoard = createKid(self, fixedBoardState)
                        checkMoves(x, y-2, (x,y), fixedBoard)
                    #Right
                    if x < 14 and currentBoardState[y-1][x+1] != 0 and currentBoardState[y-2][x+2] == 0 and lastPosition != (x+2, y-2):
                        fixedBoardState = createFixedBoardState(x, y, x+2, y-2, currentBoard)
                        fixedBoard = createKid(self, fixedBoardState)
                        checkMoves(x+2, y-2, (x,y), fixedBoard)
                #Mid Left
                if x > 1 and currentBoardState[y][x-1] != 0 and currentBoardState[y][x-2] == 0 and lastPosition != (x-2, y):
                    fixedBoardState = createFixedBoardState(x, y, x-2, y, currentBoard)
                    fixedBoard = createKid(self, fixedBoardState)
                    checkMoves(x-2, y, (x,y), fixedBoard)
                #Mid Right
                if x < 14 and currentBoardState[y][x+1] != 0 and currentBoardState[y][x+2] == 0 and lastPosition != (x+2, y):
                    fixedBoardState = createFixedBoardState(x, y, x+2, y, currentBoard)
                    fixedBoard = createKid(self, fixedBoardState)
                    checkMoves(x+2, y, (x,y), fixedBoard)
                #Bot 
                if y < 14:
                    #Left
                    if x > 1 and currentBoardState[y+1][x-1] != 0 and currentBoardState[y+2][x-2] == 0 and lastPosition != (x-2, y+2):
                        fixedBoardState = createFixedBoardState(x, y, x-2, y+2, currentBoard)
                        fixedBoard = createKid(self, fixedBoardState)
                        checkMoves(x-2,y+2, (x,y), fixedBoard)
                    #Mid
                    if currentBoardState[y+1][x] != 0 and currentBoardState[y+2][x] == 0 and lastPosition != (x, y+2):
                        fixedBoardState = createFixedBoardState(x, y, x, y+2, currentBoard)
                        fixedBoard = createKid(self, fixedBoardState)
                        checkMoves(x, y+2, (x,y), fixedBoard)
                    #Right
                    if x < 14 and currentBoardState[y+1][x+1] != 0 and currentBoardState[y+2][x+2] == 0 and lastPosition != (x+2, y+2):
                        fixedBoardState = createFixedBoardState(x, y, x+2, y+2, currentBoard)
                        fixedBoard = createKid(self, fixedBoardState)
                        checkMoves(x+2, y+2, (x,y), fixedBoard)

            for piece in allPieces:
                x = piece[1]
                y = piece[0]
                checkMoves(x, y, (x,y), givenBoard)

            # Returns copy of board 
    
        def createFixedBoardState(oldX : int, oldY : int, newX : int, newY : int, givenBoard : Board) -> list[list[int]]:
            fixedBoardState = givenBoard.copyBoardState()
            fixedBoardState[newY][newX] = fixedBoardState[oldY][oldX]
            fixedBoardState[oldY][oldX] = 0
            return fixedBoardState
        
        # Creates kid node. Assigns its parent, also returns node itself (optional)
        def createKid(parentNode : 'Node', fixedBoardState) -> Board:
            newBoard = Board.Board(fixedBoardState)
            newNode = Node(newBoard, parentNode)
            # newNode.parent = parentNode
            parentNode.children.append(newNode)
            return newBoard

        givenBoard = self.board
        if self.currentPlayer == 1: allPieces = self.board.currentOnes
        elif self.currentPlayer == 2: allPieces = self.board.currentTwos
        else: raise Exception("Unknown player. Only possible players are: 1 and 2.")

        generateDirectMoves(givenBoard, allPieces)
        generateIndirectMoves(givenBoard, allPieces)
    
    def printNode(self):
        self.board.printBoard()

# node = Node(Board.Board(INDIRECT_BOARD2))
# node.generateMoves()
# for child in node.children:
#     child.board.printBoard()
# print(len(node.children))

# node1 = Node(Board.Board(INDIRECT_BOARD2))
# board11 = node1.board.copyBoardState()
# node11 = Node(Board.Board(board11))

# node1.board.printBoard()
# node11.board.printBoard()