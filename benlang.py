from parse.parser import get_syntax_tree, to_ast
from util.graph import draw_ast, draw_syntax_tree
from typecheck.typecheck import check
from parse.BenLangParser import  BenLangParser
import sys


def main(argv):
    syntax_tree = get_syntax_tree(argv[1])
    ast = to_ast(syntax_tree)
    draw_ast(ast)

    check(ast)

if __name__ == "__main__":
    main(sys.argv)
