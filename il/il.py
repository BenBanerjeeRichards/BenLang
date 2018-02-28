class Il:

    def __init__(self, il_instructions, il_labels, num_memory_locations):
        self.num_memory_locations = num_memory_locations
        self.labels = il_labels
        self.instructions = il_instructions

    def __str__(self):
        for i, instruction in enumerate(self.instructions):
            label = self.labels[i] if i in self.labels else ""
            print('{0:15}  {1}'.format(label, instruction))
        if len(self.instructions) in self.labels:
            print('{0:15}  {1}'.format(self.labels[len(self.instructions)], ""))
            pass

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

    def __init__(self, memory_location: int, param_num: int):
        self.memory_location = memory_location
        self.param_num = param_num

    def __str__(self):
        return "push t{} [num #{}]".format(self.memory_location, self.param_num)


class FunctionCallIl:

    def __init__(self, function_name: str):
        self.function_name = function_name

    def __str__(self):
        return "call {}".format(self.function_name)


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


class StartFunctionCallIl:

    def __init__(self):
        pass

    def __str__(self):
        return "StartFunctionCall"


class EndFunctionCallIl:

    def __init__(self, num_params: int):
        self.num_params = num_params

    def __str__(self):
        return "EndFunctionCall"
