import unittest
from random import shuffle

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

VALUES_FOR_TWOS = [
    [30,29,28,27,26,24,22,20,18,16,14,12,10,8,6,4],
    [29,29,28,27,25,24,22,20,18,16,14,12,10,8,6,4],
    [28,28,28,27,24,24,22,20,18,16,14,12,10,8,6,4],
    [27,27,27,24,24,22,22,20,18,16,14,12,10,8,6,4],
    [26,25,24,24,24,22,20,20,18,16,14,12,10,8,6,4],
    [24,24,24,22,22,22,20,18,18,16,14,12,10,8,6,4],
    [22,22,22,22,20,20,21,19,17,17,14,12,10,8,6,4],
    [20,20,20,20,20,18,19,19,17,15,14,12,10,8,6,4],
    [18,18,18,18,18,18,17,17,17,15,12,12,10,8,6,4],
    [16,16,16,16,16,16,17,15,15,15,12,10,10,8,6,4],
    [14,14,14,14,14,14,14,14,12,12,12,10,10,8,6,4],
    [12,12,12,12,12,12,12,12,12,10,10,10,8,6,3,2],
    [10,10,10,10,10,10,10,10,10,10,8,8,8,3,2,0],
    [8,8,8,8,8,8,8,8,8,8,8,6,3,2,1,0],
    [6,6,6,6,6,6,6,6,6,6,6,3,2,1,-3,-3],
    [4,4,4,4,4,4,4,4,4,4,4,3,0,-3,-3,-7]
]

VALUES_FOR_ONES = [
    [-7, -3, -3, 0, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
    [-3, -3, 1, 2, 3, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6],
    [0, 1, 2, 3, 6, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
    [0, 2, 3, 8, 8, 8, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10],
    [2,3,6,8,10,10,10,12,12,12,12,12,12,12,12,12],
    [4,6,8,8,10,12,12,12,14,14,14,14,14,14,14,14],
    [4,6,8,10,10,12,15,15,15,17,16,16,16,16,16,16],
    [4,6,8,10,12,12,15,17,17,17,18,18,18,18,18,18],
    [4,6,8,10,12,14,15,17,19,19,18,20,20,20,20,20],
    [4,6,8,10,12,14,17,17,19,21,20,20,22,22,22,22],
    [4,6,8,10,12,14,16,18,18,20,22,22,22,24,24,24],
    [4,6,8,10,12,14,16,18,20,20,22,24,24,24,25,26],
    [4,6,8,10,12,14,16,18,20,22,22,24,24,27,27,27],
    [4,6,8,10,12,14,16,18,20,22,24,24,27,28,28,28],
    [4,6,8,10,12,14,16,18,20,22,24,25,27,28,29,29],
    [4,6,8,10,12,14,16,18,20,22,24,26,27,28,29,30]
]

CAMP_ONE = [
    (11,14),(11,15),
    (12,13),(12,14),(12,15),
    (13,12),(13,13),(13,14),(13,15),
    (14,11),(14,12),(14,13),(14,14),(14,15),
    (15,11),(15,12),(15,13),(15,14),(15,15)
]

CAMP_TWO = [
    (0,0),(0,1),(0,2),(0,3),(0,4),
    (1,0),(1,1),(1,2),(1,3),(1,4),
    (2,0),(2,1),(2,2),(2,3),
    (3,0),(3,1),(3,2),
    (4,0),(4,1)
]

# Class representing current board state, including:
#   - positions
#   - camps
#   - basic heuristics
#   - win conditions
class Board:
    def __init__(self, boardState) -> None:
        self.boardState : list[list[int]] = boardState
        # self.__campOne : list = self.__defineCampOne()
        # self.__campTwo : list = self.__defineCampTwo()
        self.currentOnes : list = self.__addElements(1) #[(i, j) for i, row in enumerate(self.boardState) for j, column in enumerate(row) if column == 1]
        self.currentTwos : list = self.__addElements(2) #[(i, j) for i, row in enumerate(self.boardState) for j, column in enumerate(row) if column == 2]
        # self.allPieces = self.currentOnes + self.currentTwos
        self.value : int = self.__calculateValue()
        self.isOver : int = self.__checkWinConditions()

    # calculating board value
    def __calculateValue(self) -> int:
        
        # field values for ones
        # def setValuesForOnes() -> list[list[int]]:
        #     result = setValuesForTwos()
        #     emptyMatrix = [[0 for _ in range(16)] for _ in range(16)]
        #     for i in range(len(result)):
        #         for j in range(len(result[i])):
        #             emptyMatrix[i][j] = result[len(result) - i - 1][len(result) - j - 1]
        #     return emptyMatrix

        result = 0
        # valuesForOnes = setValuesForOnes()
        # valuesForTwos = setValuesForTwos()
        for one in self.currentOnes:
            result += VALUES_FOR_ONES[one[1]][one[0]]
        for two in self.currentTwos:
            result -= VALUES_FOR_TWOS[two[1]][two[0]]
        return result
    
    # returns list of positions (tuples(x,y)) of given pieces
    def __addElements(self, elementIndex : int) -> list:
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
        shuffle(result)
        return result

    # UNUSED
    def __calculateDistances(self) -> int:
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

    # 1 - one won, 2 - two won, 0 - still undecided
    def __checkWinConditions(self) -> int:
        # def defineCampOne() -> list:
        #     result = [
        #         (0,0),(0,1),(0,2),(0,3),(0,4),
        #         (1,0),(1,1),(1,2),(1,3),(1,4),
        #         (2,0),(2,1),(2,2),(2,3),
        #         (3,0),(3,1),(3,2),
        #         (4,0),(4,1)
        #     ]
        #     return result
    
        # def defineCampTwo() -> list:
        #     result = [
        #         (11,14),(11,15),
        #         (12,13),(12,14),(12,15),
        #         (13,12),(13,13),(13,14),(13,15),
        #         (14,11),(14,12),(14,13),(14,14),(14,15),
        #         (15,11),(15,12),(15,13),(15,14),(15,15)
        #     ]
        #     return result
        result = 1
        # campOne = defineCampOne()
        # campTwo = defineCampTwo()
        for element in self.currentOnes:
            if element not in CAMP_ONE:
                result = 2
                break
        for element in self.currentTwos:
            if element not in CAMP_TWO:
                result = 0
                break
        return result

    # print pieces on the board and board value
    def printBoard(self) -> None:
        for row in self.boardState:
            print(row)
        print("Value: " + str(self.value))
        print("========================")

    # copy current positions of pieces
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
    board = Board(START_BOARD)
    board.printBoard()