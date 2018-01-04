class Operand:

    def __init__(self):
        pass


class MemoryOperand(Operand):

    def __init__(self, id: int):
        super().__init__()
        self.id = id

    def __str__(self):
        return "t{}".format(self.id)


class StringOperand(Operand):
    def __init__(self, value: str):
        super().__init__()
        self.value = value

    def __str__(self):
        return self.value


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


class PushParamIl:

    def __init__(self, memory_location: int):
        self.memory_location = memory_location

    def __str__(self):
        return "push t{}".format(self.memory_location)


class FunctionCallIl:

    def __init__(self, function_name: str):
        self.function_name = function_name

    def __str__(self):
        return "call {}".format(self.function_name)


class PopParamIl:

    def __init__(self):
        pass

    def __str__(self):
        return "pop"


class IfGotoIl:

    def __init__(self, condition, goto_label: str):
        self.label = goto_label
        self.condition = condition

    def __str__(self):
        return "if {} goto {}".format(self.condition, self.label)


class GotoIl:

    def __init__(self, label: str):
        self.label = label

    def __str__(self):
        return "goto {}".format(self.label)