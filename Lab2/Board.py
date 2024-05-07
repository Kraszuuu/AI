import unittest

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

WIN_ONE_BOARD = [
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
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1],
    [0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1],
    [0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1],
    [0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1]
]

# Class representing current board state, including:
#   - positions
#   - camps
#   - basic heuristics
#   - win conditions
class Board:
    def __init__(self, boardState) -> None:
        self.boardState : int[[]] = boardState
        self.campOne : list = self.defineCampOne()
        self.campTwo : list = self.defineCampTwo()
        self.currentOnes : list = self.addElements(1)
        self.currentTwos : list = self.addElements(2)
        self.allPieces = self.currentOnes + self.currentTwos
        self.value : int = self.calculateDistances()
        self.isOver : int = self.checkWinConditions()

    # Populating board, checking conditions, calculating distances
    def defineCampOne(self) -> list:
        result = [
            (0,0),(0,1),(0,2),(0,3),(0,4),
            (1,0),(1,1),(1,2),(1,3),(1,4),
            (2,0),(2,1),(2,2),(2,3),
            (3,0),(3,1),(3,2),
            (4,0),(4,1)
        ]
        return result
    
    def defineCampTwo(self) -> list:
        result = [
            (11,14),(11,15),
            (12,13),(12,14),(12,15),
            (13,12),(13,13),(13,14),(13,15),
            (14,11),(14,12),(14,13),(14,14),(14,15),
            (15,11),(15,12),(15,13),(15,14),(15,15)
        ]
        return result
    
    def addElements(self, elementIndex : int) -> list:
        if elementIndex != 1 and elementIndex != 2:
            raise Exception("Wrong elementIndex. Accepted elementIndex numbers are: 1 and 2")
        result = []
        i = 0
        j = 0
        for row in self.boardState:
            for column in row:
                if column == elementIndex:
                    result.append((i,j))
                j += 1
            j = 0
            i += 1
        return result

    def calculateDistances(self) -> int:
        def calculateDistance(self, elementIndex : int) -> int:
            def findClosestSpotDistance(element : tuple, potentialSpots : list) -> int:
                minimalDistance = 999
                for spot in potentialSpots:
                    distanceX = abs(element[0] - spot[0])
                    distanceY = abs(element[1] - spot[1])
                    distance = max(distanceX, distanceY)

                    if distance < minimalDistance: minimalDistance = distance
                return minimalDistance

            if elementIndex == 1:
                targetCamp = self.campTwo
                currentElements = self.currentOnes
            elif elementIndex == 2:
                targetCamp = self.campOne
                currentElements = self.currentTwos
            else:
                raise Exception("Wrong elementIndex. Accepted elementIndex numbers are: 1 and 2")
            
            result = 0
            for element in currentElements:
                result += findClosestSpotDistance(element, targetCamp)
            return result
        return calculateDistance(self, 1) - calculateDistance(self, 2)

    def checkWinConditions(self) -> int:
        result = 1
        for element in self.currentOnes:
            if element not in self.campTwo:
                result = 2
                break
        for element in self.currentTwos:
            if element not in self.campOne:
                result = 0
                break
        return result

    def printBoard(self) -> None:
        for row in self.boardState:
            print(row)
        print("Value: " + str(self.value))
        print("========================")

    def copyBoardState(self):
        fixedBoardState = [[0 for _ in range(len(self.boardState[0]))] for _ in range(len(self.boardState))]

        for i in range(len(self.boardState)):
            for j in range(len(self.boardState[0])):
                fixedBoardState[i][j] = self.boardState[i][j]
        return fixedBoardState


class BoardTest(unittest.TestCase):
    def testCalculateDistances(self):
        startBoard : Board = Board(START_BOARD)
        self.assertEqual(startBoard.value, 0)
        self.assertEqual(startBoard.isOver, False)

        winOneBoard : Board = Board(WIN_ONE_BOARD)
        self.assertEqual(winOneBoard.value, 0)
        self.assertEqual(winOneBoard.isOver, True)

if __name__ == '__main__':
    unittest.main()