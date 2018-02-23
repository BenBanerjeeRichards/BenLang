# mov $t1, $t2
# add $t1, $t1, $t2
# addi $ti, $t2, 12
# j LABEL
# jr $ra

from il.il import *

# Notes:

# 1.  IL Gen wrong for while loop - should use conditional but jumps to start each time
# 2.  We run out of registers - possible leak or just too much stuff going on and need to expand to s registers
#      and the stack

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

        self.mips_registers = {
            0: "zero",
            1: "at",
            2: "v0",
            3: "v1",
            4: "a0",
            5: "a1",
            6: "a2",
            7: "a3",
            8: "t0",
            9: "t1",
            10: "t2",
            11: "t3",
            12: "t4",
            13: "t5",
            14: "t6",
            15: "t7",
            16: "s0",
            17: "s1",
            18: "s2",
            19: "s3",
            20: "s4",
            21: "s5",
            22: "s6",
            23: "s7",
            24: "t8",
            25: "t9",
            26: "k0",
            27: "k1",
            28: "gp",
            29: "sp",
            30: "fp",
            31: "ra"
        }

    def emit_instruction(self, instruction: str, params, inline_comment):
        params_formatted = ", ".join(params)
        without_comment = "\t{0:<10}{1:<20}".format(instruction, params_formatted)
        if inline_comment:
            self.code += "{0}#{1:<30}\n".format(without_comment, inline_comment)
        else:
            self.code += "{}\n".format(without_comment)

    def pretty_register(self, register_id: int):
        assert 31 >= register_id >= 0
        return "${}".format(self.mips_registers[register_id])

    def il_id_from_stack_location(self, stack_location: int):
        for k, v in self.stack_locations.items():
            if v == stack_location:
                return k
        return None

    def emit_label(self, label: str):
        self.code += "{}:\n".format(label)

    def emit_unary_op(self, instruction: str, dest_reg: int, op: int):
        self.emit_instruction(instruction, [self.pretty_register(dest_reg), self.pretty_register(op)], "")

    def emit_binary_op(self, instruction: str, dest_reg: int, op1_reg: int, op2_reg: int):
        self.emit_instruction(instruction, [self.pretty_register(dest_reg), self.pretty_register(op1_reg), self.pretty_register(op2_reg)], "")

    def emit_jump(self, label: str):
        self.emit_instruction("j", [label], "")

    def emit_return(self):
        self.emit_instruction("ja", ["$ra"], "")

    def emit_store(self, source_reg:int, offset: int, dest: int):
        pretty_source = self.pretty_register(source_reg)
        pretty_dest = self.pretty_register(dest)

        comment = "{} -> {}[{}]".format(pretty_source, pretty_dest, offset)
        with_offset = "{}({})".format(offset, pretty_dest)
        self.emit_instruction("sw", [pretty_source, with_offset], comment)

    def emit_load(self, source_reg:int, offset: int, dest: int):
        pretty_source = self.pretty_register(source_reg)
        pretty_dest = self.pretty_register(dest)
        with_offset = "{}({})".format(offset, pretty_dest)

        existing_id = self.il_id_from_stack_location(offset)
        additional_comment = ""
        if existing_id:
            additional_comment = " (t{})".format(existing_id)

        comment = "{} <- {}[{}] {}".format(pretty_source, pretty_dest, offset, additional_comment)

        self.emit_instruction("lw", [pretty_source, with_offset], comment)

    def emit_jal(self, label:str):
        self.emit_instruction("jal", [label], "")

    def emit_unary_intermediate(self, instruction: str, reg: int, intermediate: int):
        self.emit_instruction(instruction, [self.pretty_register(reg), str(intermediate)], "")

    def emit_binary_intermediate(self, instruction: str, source_reg: int, dest_reg: int, intermediate: int):
        self.emit_instruction(instruction, [self.pretty_register(source_reg),self.pretty_register(dest_reg), str(intermediate)], "")

    def emit_single_reg(self, instr: str, reg: int):
        self.emit_instruction(instr, [self.pretty_register(reg)], "")

    def emit_comment(self, comment):
        self.code += "\t# {}\n".format(comment)

    def emit_newline(self):
        self.code += "\n"

    def emit_branch(self, instr: str, lhs_reg: int, rhs_reg, label: str):
        self.emit_instruction(instr, [self.pretty_register(lhs_reg), self.pretty_register(rhs_reg), label], "")

    def save_reg_to_stack(self, reg: int, memory_loc_id: int):
        stack_offset = self.get_stack_location(memory_loc_id)
        self.emit_store(reg, stack_offset, self.fp_register)

    def generate(self):
        for i, instruction in enumerate(self.il_instructions):
            if i > 0:
                self.emit_newline()
            self.emit_comment(instruction)

            # Generate labels
            if i in self.il_labels:
                self.emit_label(self.il_labels[i])

            if isinstance(instruction, PushParamIl):
                self.generate_push(instruction)
            elif isinstance(instruction, FunctionCallIl):
                self.generate_function_call(instruction)
            elif isinstance(instruction, StartFunctionCallIl):
                self.generate_function_call_start()
            elif isinstance(instruction, IfGotoIl):
                self.generate_if_goto(instruction)
            elif isinstance(instruction, GotoIl):
                self.generate_goto(instruction)
            else:
                self.generate_assignment(instruction)

        # We can have a label at the very end of the program after instructions, check for this
        if len(self.il_instructions) in self.il_labels:
            self.emit_label(self.il_labels[len(self.il_instructions)])

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
                # print("Alloc {}, used: {}".format(register, self.used_registers))
                return register

        raise RegisterError("Ran out of t registers")

    def free_register(self, register: int):
        # print("Freed {}".format(register))
        if register in self.used_registers:
            self.used_registers.remove(register)
        else:
            raise RegisterError("Tried to free unallocated register {} ".format(register))

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

        if isinstance(operand, BoolOperand):
            reg = self.alloc_register()
            value = 1 if operand.value else 0
            self.emit_unary_intermediate("li", reg, value)
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

            op = il.rhs.operation
            dest = self.alloc_register()

            if op == "+":
                self.emit_binary_op("add", dest, lhs, rhs)
            elif op == "-":
                self.emit_binary_op("sub", dest, lhs, rhs)
            elif op == "*":
                self.emit_unary_op("mult", lhs, rhs)
                self.emit_single_reg("mflo", dest)
            elif op == "/":
                # Integer division
                self.emit_unary_op("div", lhs, rhs)
                self.emit_single_reg("mflo", dest)
            elif op == "<":
                self.emit_binary_op("slt", dest, lhs, rhs)
            elif op == "==":
                s1 = self.alloc_register()
                s2 = self.alloc_register()

                # We want to know if a == b
                # a xor b = zero if and only if a == b
                # So we test if a xor b is equal to zero
                # but MIPS doesn't have a "set if equal to zero"
                # We check if a xor b < 0 or a xor b > 0 instead
                # Finally negate result using stli for checking if not one

                self.emit_binary_op("xor", lhs, lhs, rhs)

                self.emit_binary_op("sltu", s1, lhs, 0)
                self.emit_binary_op("sltu", s2, 0, lhs)
                self.emit_binary_op("or", lhs, s1, s2)
                self.emit_binary_intermediate("slti", dest, lhs, 1)

                self.free_register(s1)
                self.free_register(s2)

            # Save to stack
            self.save_reg_to_stack(dest, il.target.id)

            self.free_register(dest)
            self.free_register(lhs)
            self.free_register(rhs)

        if isinstance(il.rhs, UnaryIl):

            if il.rhs.operation == "!":
                lhs = self.get_operand_register(il.rhs.operand)
                dest = self.alloc_register()

                # 1 xor 1 = 0
                # 0 xor 1 = 1
                # Hence xor is a not gate
                one_reg = self.alloc_register()

                self.emit_unary_intermediate("li", one_reg, 1)
                self.emit_binary_op("xor", dest, lhs, one_reg)

                self.free_register(one_reg)
                self.free_register(lhs)
                self.free_register(dest)

                self.save_reg_to_stack(dest, il.target.id)

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
            self.free_register(reg)

    def generate_function_call(self, il: FunctionCallIl):
        # Set $fp to $sp
        self.emit_unary_op("move", self.fp_register, self.sp_register)
        # Do da call
        self.emit_jal(il.function_name)

    def generate_function_call_start(self):
        self.emit_binary_intermediate("addi", self.sp_register, self.sp_register, -4)
        self.stack_pointer -= 4
        self.emit_store(self.fp_register, self.stack_pointer, self.fp_register)

    def generate_if_goto(self, il: IfGotoIl):
        assert isinstance(il.condition, MemoryOperand)

        lhs = self.get_operand_register(il.condition)
        self.emit_branch("bne", lhs, 0, il.label)
        self.free_register(lhs)

    def generate_goto(self, il: GotoIl):
        self.emit_jump(il.label)


class RegisterError(Exception):
    pass
