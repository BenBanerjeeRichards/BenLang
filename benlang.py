import os
import sys

from codegen.codegen import CodeGen
from il.il_convert import IlGenerator
from parse.parser import get_syntax_tree, to_ast
from typecheck.typecheck import check
import subprocess

mars = "Mars4_5.jar"
FNULL = open(os.devnull, 'w')

def main(argv):
    if len(argv) != 3:
        print("Expected params: benlang.py <input.ben> <output.s>")
        return

    compile_benlang(argv[1], argv[2])
    test()


def compile_benlang(input_file: str, output_file: str):
    # Parse
    syntax_tree = get_syntax_tree(input_file)
    # Syntax -> AST
    ast = to_ast(syntax_tree)
    # draw_ast(ast)

    # Type check
    check(ast)

    # Generate IL
    il = IlGenerator().to_il(ast)

    # Codegen
    cd = CodeGen(il)
    cd.generate()

    with open("mips_template.s", "r") as template_file, open(output_file, "w+") as output_file:
        template = template_file.read()
        code = template.format(cd.code)
        output_file.write(code)
        output_file.close()


def run_mips(file:str):
    out = subprocess.check_output(["java", "-jar", mars, file], stderr=FNULL)
    return str(out).split("Copyright 2003-2014 Pete Sanderson and Kenneth Vollmar\\n\\r\\")[1][1:-5]


def test():
    test_files = os.listdir("test/integrationData/ben")
    for ben_file in test_files:
        test_name = os.path.splitext(ben_file)[0]
        expected_output = open("test/integrationData/out/{}.out".format(test_name), "r").read()
        mips_output = "test/integrationData/mips/{}.s".format(test_name)

        # Compile
        print("[TEST {}]".format(test_name), end="")

        try:
            compile_benlang("test/integrationData/ben/" + ben_file, mips_output)
        except Exception as e:
            print("[TEST {}]: COMPILATION FAILED WITH ERROR".format(test_name), end="")
            print(e)
            continue
        print(" compile ok, ", end="")

        actual_output = run_mips(mips_output)
        if actual_output == expected_output:
            print("output correct. PASSED")
        else:
            print("output incorrect: FAILED")
            print("expected output:")
            print(expected_output)
            print("actual output:")
            print(actual_output)
            print()

if __name__ == "__main__":
    main(sys.argv)
