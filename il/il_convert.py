from il.il import *
from parse.ast import *


class VariableEnvironment:

    def __init__(self):
        self.variables = [{}]

    def add_variable(self, name, memory_location : int):
        self.variables[-1][name] = memory_location

    def get_variable(self, name):
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
        self.env = VariableEnvironment()

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
            return BoolOperand(True)
        if isinstance(root, FalseNode):
            return BoolOperand(False)
        if isinstance(root, IdentifierNode):
            memory_location = self.env.get_variable(root.identifier)
            assert memory_location is not None
            return MemoryOperand(memory_location)

        if isinstance(root, AdditionNode):
            return self._arith_il(root, "+")
        if isinstance(root, MultiplicationNode):
            return self._arith_il(root, "*")
        if isinstance(root, SubtractionNode):
            return self._arith_il(root, "-")
        if isinstance(root, DivisionNode):
            return self._arith_il(root, "/")
        if isinstance(root, AndNode):
            return self._arith_il(root, "&&")
        if isinstance(root, OrNode):
            return self._arith_il(root, "||")
        if isinstance(root, OpEqualsNode):
            return self._arith_il(root, "==")
        if isinstance(root, OpLessThanNode):
            return self._arith_il(root, "<")

        if isinstance(root, DeclarationNode):
            rhs = self.expression_to_il(root.rhs)

            self._next_memory()
            self.instructions.append(AssignmentIl(self._current_memory(), rhs))

            # Store memory location in variable
            self.env.add_variable(root.identifier.identifier, self.memory_idx)
            return

    def _arith_il(self, root: Node, operator: str):
        lhs = self.expression_to_il(root.left)
        rhs = self.expression_to_il(root.right)
        addition = BinaryIl(lhs, operator, rhs)
        self._next_memory()
        assignment = AssignmentIl(self._current_memory(), addition)
        self._add_instruction(assignment)
        return self._current_memory()

    def _add_instruction(self, instruction):
        self.instructions.append(instruction)

    def _next_memory(self):
        self.memory_idx += 1
        return self.memory_idx

    def _current_memory(self) -> MemoryOperand:
        return MemoryOperand(self.memory_idx)

