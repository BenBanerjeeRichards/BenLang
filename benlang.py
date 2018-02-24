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
    il = IlGenerator().to_il(ast)
    for i, instruction in enumerate(il.instructions):
        label = il.labels[i] if i in il.labels else ""
        print('{0:15}  {1}'.format(label, instruction))
    if len(il.instructions) in il.labels:
        print('{0:15}  {1}'.format(il.labels[len(il.instructions)], ""))
        pass

    cd = CodeGen(il)
    cd.generate()

    with open("mips_template.s", "r") as template_file, open("out.s", "w+") as output_file:
        template = template_file.read()
        code = template.format(cd.code)
        output_file.write(code)
        output_file.close()

if __name__ == "__main__":
    main(sys.argv)
