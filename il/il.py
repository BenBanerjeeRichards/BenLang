class Operand:

    def __init__(self):
        pass


class MemoryOperand(Operand):

    def __init__(self, id: int):
        super().__init__()
        self.id = id

    def __str__(self):
        return "t{}".format(self.id)


class IntegerOperand(Operand):

    def __init__(self, value: int):
        super().__init__()
        self.value = value

    def __str__(self):
        return str(self.value)


class BoolOperand(Operand):

    def __init__(self, value: bool):
        super().__init__()
        self.value = value

    def __str__(self):
        if self.value:
            return "#t"
        else:
            return "#f"


class BinaryIl:

    def __init__(self, lhs: Operand, operation: str, rhs: Operand):
        self.lhs = lhs
        self.rhs = rhs
        self.operation = operation

    def __str__(self):
        return "{} {} {}".format(self.lhs, self.operation, self.rhs)


class UnaryIl:

    def __init__(self, operation: str, operand: Operand):
        self.operand = operand
        self.operation = operation

    def __str__(self):
        return "{} {}".format(self.operation, self.operand)


class AssignmentIl:

    def __init__(self, target: MemoryOperand, rhs):
        self.target = target
        self.rhs = rhs

    def __str__(self):
        return "{} := {}".format(self.target, self.rhs)
