class Node:

    def __init__(self, children):
        self._children = children

    def get_children(self):
        return self._children


class IntNode(Node):

    def __init__(self, value):
        super().__init__([])
        self.value = value


class AdditionNode(Node):

    def __init__(self, left: Node, right: Node):
        super().__init__([left, right])


class MultiplicationNode(AdditionNode):
    pass

