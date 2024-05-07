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
    def __init__(self, board : Board) -> None:
        self.value : int = board.value
        self.board : Board = board
        self.children : list = []
        self.parent : Node = None

        self.currentPlayer : int = 1         

    def generateIndirectMoves(self):
        def checkMoves(x : int, y : int, lastPosition : tuple, currentBoard : Board):
            currentBoardState = currentBoard.boardState
            #Top
            if y > 1:
                #Left
                if x > 1 and currentBoardState[y-1][x-1] != 0 and lastPosition != (x-2,y-2):
                    fixedBoardState = createFixedBoardState(x, y, x-2, y-2, currentBoard)
                    fixedBoard = createKid(self, fixedBoardState)
                    checkMoves(x-2, y-2, (x,y), fixedBoard)
                #Mid
                if currentBoardState[y-1][x] != 0 and lastPosition != (x, y-2):
                    fixedBoardState = createFixedBoardState(x, y, x, y-2, currentBoard)
                    fixedBoard = createKid(self, fixedBoardState)
                    checkMoves(x, y-2, (x,y), fixedBoard)
                #Right
                if x < 14 and currentBoardState[y-1][x+1] != 0 and lastPosition != (x+2, y-2):
                    fixedBoardState = createFixedBoardState(x, y, x+2, y-2, currentBoard)
                    fixedBoard = createKid(self, fixedBoardState)
                    checkMoves(x+2, y-2, (x,y), fixedBoard)
            #Mid Left
            if x > 1 and currentBoardState[y][x-1] != 0 and lastPosition != (x-2, y):
                fixedBoardState = createFixedBoardState(x, y, x-2, y, currentBoard)
                fixedBoard = createKid(self, fixedBoardState)
                checkMoves(x-2, y, (x,y), fixedBoard)
            #Mid Right
            if x < 14 and currentBoardState[y][x+1] != 0 and lastPosition != (x+2, y):
                fixedBoardState = createFixedBoardState(x, y, x+2, y, currentBoard)
                fixedBoard = createKid(self, fixedBoardState)
                checkMoves(x+2, y, (x,y), fixedBoard)
            #Bot 
            if y < 14:
                #Left
                if x > 1 and currentBoardState[y+1][x-1] != 0 and lastPosition != (x-2, y+2):
                    fixedBoardState = createFixedBoardState(x, y, x-2, y+2, currentBoard)
                    fixedBoard = createKid(self, fixedBoardState)
                    checkMoves(x-2,y+2, (x,y), fixedBoard)
                #Mid
                if currentBoardState[y+1][x] != 0 and lastPosition != (x, y+2):
                    fixedBoardState = createFixedBoardState(x, y, x, y+2, currentBoard)
                    fixedBoard = createKid(self, fixedBoardState)
                    checkMoves(x, y+2, (x,y), fixedBoard)
                #Right
                if x < 14 and currentBoardState[y+1][x+1] != 0 and lastPosition != (x+2, y+2):
                    fixedBoardState = createFixedBoardState(x, y, x+2, y+2, currentBoard)
                    fixedBoard = createKid(self, fixedBoardState)
                    checkMoves(x+2, y+2, (x,y), fixedBoard)

        def createKid(parentNode : Node, fixedBoardState) -> Board:
            newBoard = Board.Board(fixedBoardState)
            newNode = Node(newBoard)
            newNode.parent = parentNode
            parentNode.children.append(newNode)
            return newBoard

        def createFixedBoardState(oldX : int, oldY : int, newX : int, newY : int, givenBoard : Board) -> list[list[int]]:
            fixedBoardState = givenBoard.copyBoardState()
            fixedBoardState[newY][newX] = fixedBoardState[oldY][oldX]
            fixedBoardState[oldY][oldX] = 0
            return fixedBoardState

        board = self.board
        if self.currentPlayer == 1: allPieces = self.board.currentOnes
        elif self.currentPlayer == 2: allPieces = self.board.currentTwos
        else: raise Exception("Unknown player. Only possible players are: 1 and 2.")
        for piece in allPieces:
            x = piece[1]
            y = piece[0]
            checkMoves(x, y, (x,y), board)

    def generateDirectMoves(self):
        def createKid(self, fixedBoardState) -> None:
            newBoard = Board.Board(fixedBoardState)
            newNode = Node(newBoard)
            newNode.parent = self
            self.children.append(newNode)

        def createFixedBoardState(oldX, oldY, newX, newY):
            fixedBoardState = board.copyBoardState()
            fixedBoardState[newY][newX] = fixedBoardState[oldY][oldX]
            fixedBoardState[oldY][oldX] = 0
            return fixedBoardState

        board = self.board
        boardState = self.board.boardState
        counter = 0
        if self.currentPlayer == 1: allPieces = self.board.currentOnes
        elif self.currentPlayer == 2: allPieces = self.board.currentTwos
        else: raise Exception("Unknown player. Only possible players are: 1 and 2.")
        for piece in allPieces:
            x = piece[1]
            y = piece[0]
            #Direct Moves
            #Top
            if y > 0:
                #Left
                if x > 0 and boardState[y-1][x-1] == 0:
                    fixedBoardState = createFixedBoardState(x, y, x-1, y-1)
                    createKid(self, fixedBoardState)
                    counter +=1
                #Mid
                if boardState[y-1][x] == 0:
                    fixedBoardState = createFixedBoardState(x, y, x, y-1)
                    createKid(self, fixedBoardState)
                    counter +=1
                #Right
                if x < 15 and boardState[y-1][x+1] == 0:
                    fixedBoardState = createFixedBoardState(x, y, x+1, y-1)
                    createKid(self, fixedBoardState)
                    counter +=1
            #Mid Left
            if x > 0 and boardState[y][x-1] == 0:
                fixedBoardState = createFixedBoardState(x, y, x-1, y)
                createKid(self, fixedBoardState)
                counter +=1
            #Mid Right
            if x < 15 and boardState[y][x+1] == 0:
                fixedBoardState = createFixedBoardState(x, y, x+1, y)
                createKid(self, fixedBoardState)
                counter +=1
            #Bot 
            if y < 15:
                #Left
                if x > 0 and boardState[y+1][x-1] == 0:
                    fixedBoardState = createFixedBoardState(x, y, x-1, y+1)
                    createKid(self, fixedBoardState)
                    counter +=1
                #Mid
                if boardState[y+1][x] == 0:
                    fixedBoardState = createFixedBoardState(x, y, x, y+1)
                    createKid(self, fixedBoardState)
                    counter +=1
                #Right
                if x < 15 and boardState[y+1][x+1] == 0:
                    fixedBoardState = createFixedBoardState(x, y, x+1, y+1)
                    createKid(self, fixedBoardState)
                    counter +=1
    
    def sortChildren(self):
        self.children.sort()

node = Node(Board.Board(INDIRECT_BOARD2))
# node.board.printBoard()
node.generateDirectMoves()
node.generateIndirectMoves()
for child in node.children:
    child.board.printBoard()
print(len(node.children))

# node1 = Node(Board.Board(INDIRECT_BOARD2))
# board11 = node1.board.copyBoardState()
# node11 = Node(Board.Board(board11))

# node1.board.printBoard()
# node11.board.printBoard()