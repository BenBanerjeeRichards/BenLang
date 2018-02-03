from parse.parser import get_syntax_tree, to_ast
from util.graph import draw_ast, draw_syntax_tree
from typecheck.typecheck import check
from il.il_convert import IlGenerator
from codegen.codegen import CodeGen
from parse.BenLangParser import BenLangParser
import sys


def main(argv):
    syntax_tree = get_syntax_tree(argv[1])
    ast = to_ast(syntax_tree)
    draw_ast(ast)

    check(ast)
    ilgen = IlGenerator()
    ilgen.expression_to_il(ast)
    for i, instruction in enumerate(ilgen.instructions):
        label = ilgen.labels[i] if i in ilgen.labels else ""
        # print('{0:15}  {1}'.format(label, instruction))
    if len(ilgen.instructions) in ilgen.labels:
        # print('{0:15}  {1}'.format(ilgen.labels[len(ilgen.instructions)], ""))
        pass

    cd = CodeGen(ilgen.instructions, ilgen.labels)
    cd.generate()
    print(cd.code)

if __name__ == "__main__":
    main(sys.argv)
