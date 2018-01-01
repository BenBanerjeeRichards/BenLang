from antlr4 import *
from BenLangLexer import BenLangLexer
from BenLangParser import BenLangParser
import sys
from parse.ast import *
from util.graph import draw_ast, draw_syntax_tree


def is_terminal(x):
    return isinstance(x, tree.Tree.TerminalNodeImpl)


def get_start_stop_pos(root):
    start_position = FilePosition(root.start.line, root.start.column, root.start.tokenIndex)
    stop_position = FilePosition(root.stop.line, root.stop.column, root.stop.tokenIndex)
    return start_position, stop_position


def to_ast(root):
    if is_terminal(root):
        position = FilePosition(root.symbol.line, root.symbol.column, root.symbol.tokenIndex)
        if root.symbol.type == BenLangLexer.BOOL_TYPE:
            return BoolTypeNode(position)
        if root.symbol.type == BenLangLexer.STRING_TYPE:
            return StringTypeNode(position)
        if root.symbol.type == BenLangLexer.INT_TYPE:
            return IntegerTypeNode(position)

    start_position, stop_position = get_start_stop_pos(root)

    if isinstance(root, BenLangParser.ATypeContext):
        return to_ast(root.children[0])

    if isinstance(root, BenLangParser.ProgContext):
        return ProgramNode(to_ast(root.children[0]), start_position, stop_position)

    if isinstance(root, BenLangParser.StatementBlockContext):
        statements = []
        for s in root.children:
            statements.append(to_ast(s))
        return StatementBlockNode(statements, start_position, stop_position)

    if isinstance(root, BenLangParser.StatementContext):
        return to_ast(root.children[0])  # Ignore semicolon if exists

    if isinstance(root, BenLangParser.WhileLoopContext):
        assert len(root.children) == 7
        condition = to_ast(root.children[2])
        statements = to_ast(root.children[5])
        return WhileNode(condition, statements, start_position, stop_position)

    if isinstance(root, BenLangParser.ExprContext):
        return expression_to_ast(root)

    if isinstance(root, BenLangParser.IfOnlyContext):
        assert len(root.children) == 7
        condition = to_ast(root.children[2])
        statements = to_ast(root.children[5])
        return IfOnlyNode(condition, statements, start_position, stop_position)

    if isinstance(root, BenLangParser.IfElseContext):
        assert len(root.children) == 11
        condition = to_ast(root.children[2])
        statements_if = to_ast(root.children[5])
        statements_else = to_ast(root.children[9])
        return IfElseNode(condition, statements_if, statements_else, start_position, stop_position)

    if isinstance(root, BenLangParser.DeclarationContext):
        assert len(root.children) == 4;
        type = to_ast(root.children[0])
        identifier = expression_to_ast(root.children[1])
        rhs = to_ast(root.children[3])
        return DeclarationNode(type, identifier, rhs, start_position, stop_position)

    if isinstance(root, BenLangParser.AssignmentContext):
        identifier = expression_to_ast(root.children[0])
        rhs = to_ast(root.children[2])
        return AssignmentNode(identifier, rhs, start_position, stop_position)


def expression_to_ast(root: BenLangParser.StatementContext):
    if is_terminal(root):
        # Values
        return get_expression_value(root)

    start_position, stop_position = get_start_stop_pos(root)

    if isinstance(root, BenLangParser.ApplicationContext):
        func_name = expression_to_ast(root.children[0])
        # If expression exists in Params, if it doesn't then no parameters passed (note optional expression)
        # params: LBRACKET expression? paramsRest;
        params = []
        if len(root.children[1].children) > 2:
            params = expression_to_ast(root.children[1]).get_children()
        return ApplicationNode(func_name, params, start_position, stop_position)

    if isinstance(root, BenLangParser.ParamsRestContext):
        assert len(root.children) == 3
        param = expression_to_ast(root.children[1])

        if len(root.children[2].children) == 1:
            # No more parameters
            return ParamsNode([param], start_position, stop_position)

        params = expression_to_ast(root.children[2])
        return ParamsNode([param] + params.get_children(), start_position, stop_position)

    if isinstance(root, BenLangParser.ParamsContext):
        assert len(root.children) == 3
        ps = []
        ps.append(expression_to_ast(root.children[1]))

        if len(root.children[2].children) == 3:
            ps = ps + expression_to_ast(root.children[2]).get_children()

        return ParamsNode(ps, start_position, stop_position)

    if len(root.children) == 1:
        # Terminals
        return expression_to_ast(root.children[0])

    if len(root.children) == 2:
        # unary operators
        operand = expression_to_ast(root.children[1])
        return get_expression_unary_ast(root, operand, start_position, stop_position)

    if len(root.children) == 3:
        # Binary operators (two operands)
        if is_terminal(root.children[0]) and is_terminal(root.children[2]):
            return expression_to_ast(root.children[1])

        operator = root.children[1].symbol.type
        lhs = expression_to_ast(root.children[0])
        rhs = expression_to_ast(root.children[2])
        return get_expression_binary_ast(operator, lhs, rhs, start_position, stop_position)
    raise NotImplemented()


def get_expression_unary_ast(root, operand, start_position, stop_position):
    sym = root.children[0].symbol.type
    if sym == BenLangLexer.MINUS:
        return MinusOperation(operand, start_position, stop_position)

    if sym == BenLangLexer.PLUS:
        # Useless, we can discard it
        return operand

    if sym == BenLangLexer.OP_NOT:
        return NotOperation(operand, start_position, stop_position)


def get_expression_value(root):
    position = FilePosition(root.symbol.line, root.symbol.column, root.symbol.tokenIndex)
    if root.symbol.type == BenLangLexer.INTEGER:
        return IntNode(root.symbol.text, position)
    if root.symbol.type == BenLangLexer.FALSE:
        return FalseNode(position)
    if root.symbol.type == BenLangLexer.TRUE:
        return TrueNode(position)
    if root.symbol.type == BenLangParser.IDENTIFIER:
        return IdentifierNode(root.symbol.text, position)
    if root.symbol.type == BenLangParser.STRING:
        return StringNode(root.symbol.text, position)


def get_expression_binary_ast(operator, lhs, rhs, start_position, stop_position):
    if operator == BenLangLexer.PLUS:
        return AdditionNode(lhs, rhs, start_position, stop_position)
    if operator == BenLangLexer.MULT:
        return MultiplicationNode(lhs, rhs, start_position, stop_position)
    if operator == BenLangLexer.DIV:
        return DivisionNode(lhs, rhs, start_position, stop_position)
    if operator == BenLangLexer.MINUS:
        return SubtractionNode(lhs, rhs, start_position, stop_position)
    if operator == BenLangLexer.OP_AND:
        return AndNode(lhs, rhs, start_position, stop_position)
    if operator == BenLangLexer.OP_OR:
        return OrNode(lhs, rhs, start_position, stop_position)
    if operator == BenLangLexer.OP_EQ:
        return OpEqualsNode(lhs, rhs, start_position, stop_position)
    if operator == BenLangLexer.OP_LT:
        return OpLessThanNode(lhs, rhs, start_position, stop_position)


def main(argv):
    lexer = BenLangLexer(FileStream(argv[1]))
    stream = CommonTokenStream(lexer)
    parser = BenLangParser(stream)
    tree = parser.prog()
    x = to_ast(tree)
    draw_ast(x)


if __name__ == '__main__':
    main(sys.argv)
