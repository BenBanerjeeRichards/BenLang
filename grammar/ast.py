class Node:

    def __init__(self, children):
        self._children = children

    def get_children(self):
        return self._children

    def __str__(self):
        return ""


class IntNode(Node):

    def __init__(self, value):
        super().__init__([])
        self.value = value
        
    def __str__(self):
        return self.value


class AdditionNode(Node):

    def __init__(self, left: Node, right: Node):
        super().__init__([left, right])

    def __str__(self):
        return "+"


class MultiplicationNode(AdditionNode):
    def __str__(self):
        return "*"

