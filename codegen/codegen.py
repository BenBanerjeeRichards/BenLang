# mov $t1, $t2
# add $t1, $t1, $t2
# addi $ti, $t2, 12
# j LABEL
# jr $ra

from il.il import *


class CodeGen:

    def __init__(self, il_instructions, il_labels):
        # We emit a string which is then processed by SPIM
        self.il_labels = il_labels
        self.il_instructions = il_instructions
        self.code = ""
        self.stack_locations = {}   # Dict between memory location id and stack offset from $fp
        self.stack_pointer = 0

        self.used_registers = []

        self.t_registers = list(range(8, 15))
        self.s_registers = list(range(16, 23))

        self.fp_register = 30
        self.sp_register = 29
        self.zero_register = 0

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

    def emit_unary_intermediate(self, instruction: str, reg: int, intermediate: int):
        self.code += "\t{}\t${}, {}\n".format(instruction, reg, intermediate)

    def emit_binary_intermediate(self, instruction: str, source_reg: int, dest_reg: int, intermediate: int):
        self.code += "\t{}\t${}, ${}, {}\n".format(instruction, source_reg, dest_reg, intermediate)

    def emit_comment(self, comment):
        self.code += "\t# {}\n".format(comment)

    def emit_newline(self):
        self.code += "\n"

    def save_reg_to_stack(self, reg: int, memory_loc_id: int):
        stack_offset = self.get_stack_location(memory_loc_id)
        self.emit_store(reg, stack_offset, self.fp_register)

    def generate(self):
        for i, instruction in enumerate(self.il_instructions):
            if i > 0:
                self.emit_newline()
            self.emit_comment(instruction)

            if isinstance(instruction, PushParamIl):
                self.generate_push(instruction)
            elif isinstance(instruction, FunctionCallIl):
                self.generate_function_call(instruction)
            elif isinstance(instruction, PopParamIl):
                pass
            else:
                self.generate_assignment(instruction)

    def get_stack_location(self, il_id: int):
        if il_id in self.stack_locations:
            return self.stack_locations[il_id]

        # New stack location
        self.emit_binary_intermediate("addi", self.sp_register, self.sp_register,  -4)
        self.stack_pointer -= 4
        self.stack_locations[il_id] = self.stack_pointer
        return self.stack_pointer

    def alloc_register(self) -> int:
        for register in self.t_registers:
            if register not in self.used_registers:
                self.used_registers.append(register)
                return register

        raise NotImplementedError("Ran out of t registers")

    def free_register(self, register: int):
        if register in self.used_registers:
            self.used_registers.remove(register)

    def get_operand_register(self, operand: Operand):
        if isinstance(operand, IntegerOperand):
            reg = self.alloc_register()
            self.emit_unary_intermediate("li", reg, operand.value)
            return reg

        if isinstance(operand, MemoryOperand):
            stack_loc = self.get_stack_location(operand.id)
            reg = self.alloc_register()
            self.emit_load(reg, stack_loc, self.fp_register)
            return reg

    def generate_assignment(self, il: AssignmentIl):
        if isinstance(il.rhs, Operand):
            # li    $t0, 34
            reg = self.get_operand_register(il.rhs)
            self.save_reg_to_stack(reg, il.target.id)
            self.free_register(reg)

        if isinstance(il.rhs, BinaryIl):
            # In the form of t1 = t2 + 23
            lhs = self.get_operand_register(il.rhs.lhs)
            rhs = self.get_operand_register(il.rhs.rhs)

            instr = ""
            op = il.rhs.operation
            dest = self.alloc_register()

            if op == "+":
                instr = "add"

            self.emit_binary_op(instr, dest, lhs, rhs)

            # Save to stack
            self.save_reg_to_stack(dest, il.target.id)

            self.free_register(dest)
            self.free_register(lhs)
            self.free_register(rhs)

    def generate_push(self, il: PushParamIl):
        if isinstance(il, PushParamIl):
            stack_pos = self.get_stack_location(il.memory_location)
            reg = self.alloc_register()
            # Load into reg
            self.emit_load(reg, stack_pos, self.fp_register)
            # Push onto stack
            self.emit_binary_intermediate("addi", self.sp_register, self.sp_register, -4)
            self.stack_pointer -= 4
            self.emit_store(reg, self.stack_pointer, self.fp_register)

    def generate_function_call(self, il: FunctionCallIl):
        if isinstance(il, FunctionCallIl):
            # Set $fp to $sp
            self.emit_unary_op("move", self.fp_register, self.sp_register)
            # Do da call
            self.emit_jal(il.function_name)
