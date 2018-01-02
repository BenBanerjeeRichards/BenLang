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
        self.identifier = identifier

    def __str__(self):
        return self.identifier


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
        self.left = left
        self.right = right

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
        self.function_name = function_name
        self.params = params

    def __str__(self):
        return "{}()".format(self.function_name)


class StatementNode(Node):

    def __init__(self, node, start_position: FilePosition, stop_position: FilePosition):
        super().__init__([node], start_position, stop_position)

    def __str__(self):
        return "stmt"


class StatementBlockNode(Node):

    def __init__(self, statements, start_position: FilePosition, stop_position: FilePosition):
        super().__init__(statements, start_position, stop_position)

    def __str__(self):
        return "stmts"


class WhileNode(Node):

    def __init__(self, condition, statements: StatementBlockNode, start_position: FilePosition, stop_position: FilePosition):
        super().__init__([condition, statements], start_position, stop_position)
        self.condition = condition
        self.statements = statements

    def __str__(self):
        return "while"


class IfOnlyNode(Node):

    def __init__(self, condition, statements, start_position: FilePosition, stop_position: FilePosition):
        super().__init__([condition, statements], start_position, stop_position)
        self.condition = condition
        self.statements = statements

    def __str__(self):
        return "if"


class IfElseNode(Node):

    def __init__(self, condition, statements_if, statements_else, start_position: FilePosition, stop_position: FilePosition):
        super().__init__([condition, statements_if, statements_else], start_position, stop_position)
        self.condition = condition
        self.statement_if = statements_if
        self.statements_else = statements_else

    def __str__(self):
        return "ifelse"


class ProgramNode(Node):

    def __init__(self, block, start_position: FilePosition, stop_position: FilePosition):
        super().__init__([block], start_position, stop_position)

    def __str__(self):
        return "program"


class DeclarationNode(Node):

    def __init__(self, type, identifier, rhs, start_position: FilePosition, stop_position: FilePosition):
        super().__init__([type, identifier, rhs], start_position, stop_position)
        self.type = type
        self.identifier = identifier
        self.rhs = rhs

    def __str__(self):
        return "decl"


class AssignmentNode(Node):

    def __init__(self, identifier, rhs, start_position: FilePosition, stop_position: FilePosition):
        super().__init__([identifier, rhs], start_position, stop_position)
        self.identifier = identifier
        self.rhs = rhs

    def __str__(self):
        return "assign"


class AbstractTypeNode(Node):

    def __init__(self, start_position: FilePosition):
        super().__init__([], start_position, start_position)


class IntegerTypeNode(AbstractTypeNode):
    def __str__(self):
        return "int"


class StringTypeNode(AbstractTypeNode):
    def __str__(self):
        return "string"


class BoolTypeNode(AbstractTypeNode):
    def __str__(self):
        return "bool"
