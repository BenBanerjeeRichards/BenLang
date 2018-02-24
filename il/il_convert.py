from il.il import *
from parse.ast import *


class VariableEnvironment:

    def __init__(self):
        self.variables = [{}]

    def add_variable(self, name, memory_location : int):
        self.variables[-1][name] = memory_location

    def get_variable(self, name) -> int:
        for scope in self.variables:
            if name in scope:
                return scope[name]
        return None

    def add_scope(self):
        self.variables.append({})

    def pop_scope(self):
        self.variables.pop()


class IlGenerator:

    def __init__(self):
        self.memory_idx = 0
        self.instructions = []
        self.labels = {}        # Association between label id and instruction index (zero based)
        self.env = VariableEnvironment()
        self.if_label_idx = 0
        self.while_label_idx = 0

    def to_il(self, ast: Node):
        self.expression_to_il(ast)
        return Il(self.instructions, self.labels, self.memory_idx)

    def _if_label_if(self, id: int):
        return "if_{}_if".format(id)

    def _if_label_end(self, id: int):
        return "if_{}_end".format(id)

    def _start_while(self, id: int):
       return "while_{}_start".format(id)

    def _end_while(self, id: int):
       return "while_{}_end".format(id)

    def expression_to_il(self, root: Node):
        if isinstance(root, ProgramNode):
            self.expression_to_il(root.get_children()[0])
        if isinstance(root, StatementBlockNode):
            for child in root.get_children():
                self.expression_to_il(child)
        if isinstance(root, StatementNode):
            self.expression_to_il(root.get_children()[0])
        if isinstance(root, IntNode):
            return IntegerOperand(root.value)
        if isinstance(root, TrueNode):
            self._next_memory()
            self._add_instruction(AssignmentIl(self._current_memory(), BoolOperand(True)))
            return self._current_memory()
        if isinstance(root, FalseNode):
            self._next_memory()
            self._add_instruction(AssignmentIl(self._current_memory(), BoolOperand(False)))
            return self._current_memory()
        if isinstance(root, StringNode):
            return StringOperand(root.string)
        if isinstance(root, IdentifierNode):
            memory_location = self.env.get_variable(root.identifier)
            assert memory_location is not None
            return MemoryOperand(memory_location)

        if isinstance(root, AdditionNode):
            return self._binary_il(root, "+")
        if isinstance(root, MultiplicationNode):
            return self._binary_il(root, "*")
        if isinstance(root, SubtractionNode):
            return self._binary_il(root, "-")
        if isinstance(root, DivisionNode):
            return self._binary_il(root, "/")
        if isinstance(root, AndNode):
            return self._binary_il(root, "&&")
        if isinstance(root, OrNode):
            return self._binary_il(root, "||")
        if isinstance(root, OpEqualsNode):
            return self._binary_il(root, "==")
        if isinstance(root, OpLessThanNode):
            return self._binary_il(root, "<")

        if isinstance(root, MinusOperation):
            return self._unary_il(root, "-")
        if isinstance(root, NotOperation):
            return self._unary_il(root, "!")

        if isinstance(root, ApplicationNode):
            return self._function_call(root)

        if isinstance(root, IfElseNode):
            self._if_else_il(root)

        if isinstance(root, IfOnlyNode):
            self._if_only_il(root)
        if isinstance(root, DeclarationNode) or isinstance(root, AssignmentNode):
            rhs = self.expression_to_il(root.rhs)

            memory_loc_id = self.env.get_variable(root.identifier.identifier)

            if not memory_loc_id:
                self._next_memory()
                memory_loc_id = self._current_memory().id

            self.instructions.append(AssignmentIl(MemoryOperand(memory_loc_id), rhs))

            # Store memory location in variable
            self.env.add_variable(root.identifier.identifier, memory_loc_id)
            return

        if isinstance(root, WhileNode):
            self.while_label_idx += 1
            start_label = self._start_while(self.while_label_idx)
            end_label = self._end_while(self.while_label_idx)

            # Negated condition
            if len(self.instructions) in self.labels:
                start_label = self.labels[len(self.instructions)]
            else:
                self.labels[len(self.instructions)] = start_label

            negated_condition = NotOperation(root.condition, root.start_position, root.stop_position)
            condition_loc = self.expression_to_il(negated_condition)
            self._add_instruction(IfGotoIl(condition_loc, end_label))

            self.expression_to_il(root.statements)
            self._add_instruction(GotoIl(start_label))
            self.labels[len(self.instructions)] = end_label

    def _if_only_il(self, root: IfOnlyNode):
        self.if_label_idx += 1
        idx = self.if_label_idx
        end_label = self._if_label_end(idx)

        # condition (then negated with not)
        negated_condition = NotOperation(root.condition, root.start_position, root.stop_position)
        condition_loc = self.expression_to_il(negated_condition)
        self._add_instruction(IfGotoIl(condition_loc, end_label))

        # If body
        self.expression_to_il(root.statements)

        # Add label
        self.labels[len(self.instructions)] = end_label

    def _if_else_il(self, root: IfElseNode):
        self.if_label_idx += 1
        idx = self.if_label_idx
        if_label = self._if_label_if(idx)
        end_label = self._if_label_end(idx)

        # condition
        result_location = self.expression_to_il(root.condition)
        self._add_instruction(IfGotoIl(result_location, if_label))

        # else body
        self.expression_to_il(root.statements_else)
        self._add_instruction(GotoIl(end_label))
        self.labels[len(self.instructions)] = if_label

        # if body
        self.expression_to_il(root.statement_if)

        # finally add end to next instruction
        self.labels[len(self.instructions)] = end_label

    def _unary_il(self, root: AbstractUnaryOpNode, operator: str):
        rhs = self.expression_to_il(root.operand)
        unary = UnaryIl(operator, rhs)
        self._next_memory()

        assignment = AssignmentIl(self._current_memory(), unary)
        self._add_instruction(assignment)
        return self._current_memory()

    def _binary_il(self, root: Node, operator: str):
        lhs = self.expression_to_il(root.left)
        rhs = self.expression_to_il(root.right)
        addition = BinaryIl(lhs, operator, rhs)
        self._next_memory()
        assignment = AssignmentIl(self._current_memory(), addition)
        self._add_instruction(assignment)
        return self._current_memory()

    def _function_call(self, root: ApplicationNode):
        param_memory_locs = []
        for param in root.params:
            param_il = self.expression_to_il(param)
            mem_loc = None
            if not isinstance(param_il, MemoryOperand):
                # Assign values to memory location (so they can be pushed onto the stack)
                self._next_memory()
                assignment = AssignmentIl(self._current_memory(), param_il)
                self._add_instruction(assignment)
                mem_loc = self._current_memory()
            else:
                mem_loc = param_il

            param_memory_locs.append(mem_loc.id)
        self._add_instruction(StartFunctionCallIl())

        for location in param_memory_locs:
            self._add_instruction(PushParamIl(location))

        # Push function call
        call = FunctionCallIl(root.function_name.identifier)

        # If function is a non-void, assign value to memory location
        ret = None
        if not root.is_void:
            self._next_memory()
            self._add_instruction(AssignmentIl(self._current_memory(), call))
            ret = self._current_memory()
        else:
            self._add_instruction(call)

        return ret

    def _add_instruction(self, instruction):
        self.instructions.append(instruction)

    def _next_memory(self):
        self.memory_idx += 1
        return self.memory_idx

    def _current_memory(self) -> MemoryOperand:
        return MemoryOperand(self.memory_idx)

