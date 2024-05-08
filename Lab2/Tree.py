from Node import Node
class Tree:
    def __init__(self, root : Node, depth : int) -> None:
        self.root = root
        self.depth = depth

    def minmax(self, givenNode : Node, currentDepth : int) -> Node:
        if currentDepth == 0 or givenNode.board.isOver != 0:
            return givenNode
        
        if givenNode.currentPlayer == 1:
            value = float('-inf')
            for child in givenNode.children:
                if value < self.minmax(child, currentDepth - 1, 2).value:
                    value = self.minmax(child, currentDepth - 1, 2).value
                value = max(value, self.minmax(child, currentDepth - 1), 2)
        else:
            value = float('inf')
            for child in givenNode.children:
                value = min(value, self.minmax(child, currentDepth - 1, 1), 1)
        return value
        
    def generateChildren(self, node : Node, currentDepth : int = 0):
        node.generateMoves()
        if currentDepth < self.depth:
            for child in node.children:
                self.generateChildren(child, currentDepth+1)
                
    def printTreeDownNode(self, givenNode : Node):
        givenNode.printNode()
        for child in givenNode.children:
            self.printTreeDownNode(child)