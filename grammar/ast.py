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


class TrueNode(Node):

    def __init__(self):
        super().__init__([])

    def __str__(self):
        return "true"


class FalseNode(Node):
    def __init__(self):
        super().__init__([])

    def __str__(self):
        return "false"


class AbstractBinaryOpNode(Node):
    def __init__(self, left: Node, right: Node):
        super().__init__([left, right])

    def __str__(self):
        return ""


class AbstractUnaryOpNode(Node):
    def __init__(self, operand : Node):
        super().__init__([operand])

    def __str__(self):
        return ""


class AdditionNode(AbstractBinaryOpNode):
    def __str__(self):
        return "+"


class MultiplicationNode(AbstractBinaryOpNode):
    def __str__(self):
        return "*"


class DivisionNode(AbstractBinaryOpNode):
    def __str__(self):
        return "/"


class SubtractionNode(AbstractBinaryOpNode):
    def __str__(self):
        return "-"


class MinusOperation(AbstractUnaryOpNode):
    def __str__(self):
        return "-"


class NotOperation(AbstractUnaryOpNode):
    def __str__(self):
        return "!"


class AndNode(AbstractBinaryOpNode):
    def __str__(self):
        return "&&"


class OrNode(AbstractBinaryOpNode):
    def __str__(self):
        return "||"


