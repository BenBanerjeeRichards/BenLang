# mov $t1, $t2
# add $t1, $t1, $t2
# addi $ti, $t2, 12
# j LABEL
# jr $ra

class CodeGen:

    def __init__(self, il):
        self.il = il
        # We emit a string which is then processed by SPIM
        self.code = ""

    def emit_label(self, label: str):
        self.code += "{}:\n".format(label)

    def emit_unary_op(self, instruction: str, dest_reg: int, op: int):
        self.code += "\t{}\t${}, ${}\n".format(instruction, dest_reg, op)

    def emit_binary_op(self, instruction: str, dest_reg: int, op1_reg: int, op2_reg: int):
        self.code += "\t{}\t${}, ${}, ${}\n".format(instruction, dest_reg, op1_reg, op2_reg)

    def emit_jump(self, label: str):
        self.code += "\tj\t{}\n".format(label)

    def emit_return(self):
        self.code += "\tja\t$ra\n"

    def emit_store(self, source_reg:int, offset: int, dest: int):
        self.code += "\tsw\t${}, {}(${})\n".format(source_reg, offset, dest)

    def emit_load(self, source_reg:int, offset: int, dest: int):
        self.code += "\tlw\t${}, {}(${})\n".format(source_reg, offset, dest)

    def emit_jal(self, label:str):
        self.code += "\tjal\t{}\n".format(label)
