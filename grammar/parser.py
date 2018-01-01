from antlr4 import *
from BenLangLexer import BenLangLexer
from BenLangVisitor import BenLangVisitor
from BenLangParser import BenLangParser
import sys
import re
from grammar.ast import *

def prop_print(obj, sep):
    print(sep.join("%s: %s" % item for item in vars(obj).items()))


class BenLangPrintVisitor(BenLangVisitor):

    def enterEveryRule(self, ctx):
        pass
        # print("enter: {}".format(ctx.__class__.__name__))

    def exitEveryRule(self, ctx):
        pass
        # print("exit: {}".format(ctx.__class__.__name__) )

    def visitStatement(self, ctx):
        return self.visitChildren(ctx);

    def visitProg(self, ctx):
        print("IT BEGINS (visit prog)")
        return self.visitChildren(ctx)

    def visitTerminal(self, ctx):
        return ctx.symbol

    def visitExpr(self, ctx):
        x = expression_to_ast(ctx)
        draw_ast(x)


def is_terminal(x):
    return isinstance(x, tree.Tree.TerminalNodeImpl)


def expression_to_ast(root : BenLangParser.StatementContext):
    if is_terminal(root):
        # Values
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

    start_position = FilePosition(root.start.line, root.start.column, root.start.tokenIndex)
    stop_position = FilePosition(root.stop.line, root.stop.column, root.stop.tokenIndex)

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
        sym = root.children[0].symbol.type
        if sym == BenLangLexer.MINUS:
            return MinusOperation(expression_to_ast(root.children[1]), start_position, stop_position)

        if sym == BenLangLexer.PLUS:
            # Useless, we can discard it
            return expression_to_ast(root.children[1])

        if sym == BenLangLexer.OP_NOT:
            return NotOperation(expression_to_ast(root.children[1]), start_position, stop_position)

    if len(root.children) == 3:
        # Binary operators (two operands)
        if is_terminal(root.children[0]) and is_terminal(root.children[2]):
            return expression_to_ast(root.children[1])

        operator = root.children[1].symbol.type
        lhs = expression_to_ast(root.children[0])
        rhs = expression_to_ast(root.children[2])
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

        raise NotImplemented()


def graphviz(t, is_root_node, node_text, get_children, relations=[], labels={}, node_key=0):
    child_key = node_key

    labels[node_key] = sanitize_graphviz_label(node_text(t))

    if is_root_node(t):
        return node_key, relations, labels

    for child in get_children(t):
        child_key += 1
        relations.append((node_key, child_key))
        child_key += graphviz(child, is_root_node, node_text, get_children,  relations, labels, child_key)[0]

    return child_key, relations, labels


def graphviz_output(relations, labels):
    out = ""
    out += "digraph g {\n"
    for relation in relations:
        out += "\t{} -> {}\n".format(relation[0], relation[1])
    for k, v in labels.items():
        out += "\t{}[label=\"{}\"]\n".format(k, v)
    out += "}\n"

    return out


def ctx_text(ctx, symbolic_names):
    if isinstance(ctx, tree.Tree.TerminalNodeImpl):
        pattern = re.compile(r'\s+')
        text = re.sub(pattern, '', ctx.symbol.text)

        if len(text) > 0:
            return "{}({})".format(symbolic_names[ctx.symbol.type], text)
        else:
            return "{}".format(text)

    else:
        return ctx.__class__.__name__.replace("Context", "")


def sanitize_graphviz_label(text):
    return text.replace("\"", "\\\"")


def draw_syntax_tree(theTree, symbolic_names):
    out = graphviz(theTree, lambda t: isinstance(t, tree.Tree.TerminalNodeImpl), lambda x: ctx_text(x, symbolic_names), lambda x: x.getChildren())
    write_gv_output(out)


def draw_ast(ast : Node):
    out = graphviz(ast, lambda t: len(ast.get_children()) == 0, lambda x: x.__str__(), lambda x : x.get_children())
    write_gv_output(out)


def write_gv_output(output):
    gv = graphviz_output(output[1], output[2])
    f = open("graphviz", "w+")
    f.write(gv)
    f.close()

def main(argv):
    lexer = BenLangLexer(FileStream(argv[1]))
    stream = CommonTokenStream(lexer)
    parser = BenLangParser(stream)
    tree = parser.prog()
    #draw_syntax_tree(tree, BenLangLexer.symbolicNames)

    printer = BenLangPrintVisitor()
    printer.visit(tree)


# walker = ParseTreeWalker()
# walker.walk(printer, tree)

if __name__ == '__main__':
    main(sys.argv)
