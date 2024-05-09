from Node import Node
class Tree:
    def __init__(self, root : Node, depth : int) -> None:
        self.root = root
        self.depth = depth

    def minmax(self, givenNode : Node, currentDepth : int) -> int:
        if currentDepth == self.depth - 1 or givenNode.board.isOver != 0:
            return givenNode.value
        
        if givenNode.currentPlayer == 1:
            value = float('-inf')
            for child in givenNode.children:
                if value < self.minmax(child, currentDepth + 1):
                    value = self.minmax(child, currentDepth + 1)
                    givenNode.value = value
                    givenNode.nextNode = child

        else:
            value = float('inf')
            for child in givenNode.children:
                if value > self.minmax(child, currentDepth + 1):
                    value = self.minmax(child, currentDepth + 1)
                    givenNode.value = value
                    givenNode.nextNode = child

        return value


    def alphaBeta(self, givenNode : Node, currentDepth : int, alpha = -9999, beta = 9999) -> int:
        if currentDepth == self.depth - 1 or givenNode.board.isOver != 0:
            return givenNode.value
        
        if givenNode.currentPlayer == 1:
            value = float('-inf')
            for child in givenNode.children:
                helper = self.alphaBeta(child, currentDepth + 1, alpha, beta)
                if value < helper:
                    value = helper
                    alpha = max(alpha, value)
                    givenNode.value = value
                    givenNode.nextNode = child
                if beta <= alpha:
                    break

        else:
            value = float('inf')
            for child in givenNode.children:
                helper = self.alphaBeta(child, currentDepth + 1, alpha, beta)
                if value > helper:
                    beta = min(beta, value)
                    givenNode.value = value
                    givenNode.nextNode = child
                if beta <= alpha:
                    break

        return value
        
    def generateChildren(self, node : Node, currentDepth : int = 1):
        node.generateMoves()
        if currentDepth < self.depth - 1:
            for child in node.children:
                self.generateChildren(child, currentDepth+1)

    def playUsingMinmax(self) -> bool:
        if self.root.children == []: 
            self.generateChildren(self.root)
        self.root.printNode()
        self.minmax(self.root, 0)
        self.root = self.root.nextNode
        if self.root.board.isOver == 0:
            return True
        return False
    
    def playUsingAlphaBeta(self) -> bool:
        if self.root.children == []:
            self.generateChildren(self.root)
        self.root.printNode()
        self.alphaBeta(self.root, 0)
        self.root = self.root.nextNode
        if self.root.board.isOver == 0:
            return True
        return False

   
    def printTreeDownNode(self, givenNode : Node):
        givenNode.printNode()
        for child in givenNode.children:
            self.printTreeDownNode(child)