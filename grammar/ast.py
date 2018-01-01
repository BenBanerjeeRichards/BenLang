class FilePosition:

    def __init__(self, line, column, token_index):
        self.column = column
        self.line = line
        self.token_index = token_index


class Node:

    def __init__(self, children, start_position: FilePosition, stop_position: FilePosition):
        self.stop_position = stop_position
        self.start_position = start_position
        self._children = children

    def get_children(self):
        return self._children

    def __str__(self):
        return ""


class IntNode(Node):

    def __init__(self, value, position: FilePosition):
        super().__init__([], position, position)
        self.value = value

    def __str__(self):
        return self.value


class TrueNode(Node):

    def __init__(self, position: FilePosition):
        super().__init__([], position, position)

    def __str__(self):
        return "true"


class FalseNode(Node):
    def __init__(self, position: FilePosition):
        super().__init__([], position, position)

    def __str__(self):
        return "false"


class IdentifierNode(Node):
    def __init__(self, identifier, position : FilePosition):
        super().__init__([], position, position)
        self._ident = identifier

    def __str__(self):
        return self._ident


class StringNode(Node):
    def __init__(self, string : str, position : FilePosition):
        super().__init__([], position, position)
        self.string = string

    def __str__(self):
        return "\"{}\"".format(self.string)


class ParamsNode(Node):
    def __init__(self, params: [Node], start_position: FilePosition, stop_position: FilePosition):
        super().__init__(params, start_position, stop_position)

    def __str__(self):
        return "Params"


class AbstractBinaryOpNode(Node):
    def __init__(self, left: Node, right: Node, start: FilePosition, stop: FilePosition):
        super().__init__([left, right], start, stop)

    def __str__(self):
        return ""


class AbstractUnaryOpNode(Node):
    def __init__(self, operand: Node, start: FilePosition, stop: FilePosition):
        super().__init__([operand], start, stop)

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


class OpEqualsNode(AbstractBinaryOpNode):
    def __str__(self):
        return "=="


class OpLessThanNode(AbstractBinaryOpNode):
    def __str__(self):
        return "<"


class ApplicationNode(Node):

    def __init__(self, function_name: Node, params: [Node], start_position: FilePosition,
                 stop_position: FilePosition):
        super().__init__(params, start_position, stop_position)
        self._function_name = function_name

    def __str__(self):
        return "{}()".format(self._function_name)