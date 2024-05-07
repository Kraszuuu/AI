from Node import Node
class Tree:
    def __init__(self, root : Node, depth : int) -> None:
        self.root = root
        self.depth = depth
        
    def createDepth(self, node : Node, currentDepth : int = 0):
        node.generateMoves()
        if currentDepth < self.depth:
            for child in node.children:
                self.createDepth(child, currentDepth+1)
                
    def printTreeDownNode(self, givenNode : Node):
        givenNode.printNode()
        for child in givenNode.children:
            self.printTreeDownNode(child)