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
        return x


def expression_to_ast(root : BenLangParser.StatementContext):
    if isinstance(root, tree.Tree.TerminalNodeImpl):
        # Reached value
        return IntNode(root.symbol.text)

    if len(root.children) == 1:
        return expression_to_ast(root.children[0])

    if len(root.children) == 3:
        operator = root.children[1].symbol.type
        if operator == BenLangLexer.PLUS:
            return AdditionNode(expression_to_ast(root.children[0]), expression_to_ast(root.children[2]))
        if operator == BenLangLexer.MULT:
            return MultiplicationNode(expression_to_ast(root.children[0]), expression_to_ast(root.children[2]))

        raise NotImplemented()


def graphviz(t, terminalNames, relations=[], labels={}, node_key=0):
    child_key = node_key
    pattern = re.compile(r'\s+')

    if isinstance(t, tree.Tree.TerminalNodeImpl):
        text = re.sub(pattern, '', t.symbol.text)
        text = text.replace("\"", "\\\"")
        if len(text) > 0:
            labels[node_key] = "{}({})".format(terminalNames[t.symbol.type], text)
        else:
            labels[node_key] = "{}".format(terminalNames[t.symbol.type])

        return node_key, relations, labels
    else:
        labels[node_key] = t.__class__.__name__.replace("Context", "")

    for child in t.getChildren():
        child_key += 1
        relations.append((node_key, child_key))
        child_key += graphviz(child, terminalNames, relations, labels, child_key)[0]

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


def main(argv):
    lexer = BenLangLexer(FileStream(argv[1]))
    stream = CommonTokenStream(lexer)
    parser = BenLangParser(stream)
    tree = parser.prog()
    out = graphviz(tree, parser.symbolicNames)
    gv = graphviz_output(out[1], out[2])
    f = open("graphviz", "w+")
    f.write(gv)
    f.close()

    printer = BenLangPrintVisitor()
    printer.visit(tree)


# walker = ParseTreeWalker()
# walker.walk(printer, tree)

if __name__ == '__main__':
    main(sys.argv)
