from sys import exit
from parse.ast import *


class Type:
    BOOL = 1
    INT = 2
    STRING = 3
    VOID = 4

    def __init__(self):
        pass

    def from_ast_node(self, node: AbstractTypeNode):
        if isinstance(node, StringTypeNode):
            return self.STRING
        if isinstance(node, IntegerTypeNode):
            return self.INT
        if isinstance(node, BoolTypeNode):
            return self.BOOL


class FunctionType:

    def __init__(self, param_types: [int], return_type: int):
        self.return_type = return_type
        self.param_types = param_types


class Environment:

    def __init__(self):
        self.variables = [{}]
        self.functions = [
            {
                "outputStr": FunctionType([Type.STRING], Type.VOID),
                "outputInt": FunctionType([Type.INT], Type.VOID),
                "outputBool": FunctionType([Type.BOOL], Type.VOID),
                "input": FunctionType([], Type.STRING),
                "intToString": FunctionType([Type.INT], Type.STRING),
                "stringToInt": FunctionType([Type.STRING], Type.INT),
            }
        ]

    def add_scope(self):
        self.variables.append({})

    def pop_scope(self):
        self.variables.pop()

    def get_variable(self, identifier: str):
        return self._get_from_env(identifier, self.variables)

    def add_variable(self, identifier: str, type: int):
        # add to current scope
        self.variables[-1][identifier] = type

    def get_function(self, identifier: str):
        return self.functions[0][identifier]

    @staticmethod
    def _get_from_env(name, env: [dict]):
        for scope in env:
            if name in scope:
                return scope[name]
        return None

    def get_type(self, root: Node):
        if isinstance(root, IntNode):
            return Type.INT
        if isinstance(root, TrueNode) or isinstance(root, FalseNode):
            return Type.BOOL
        if isinstance(root, StringNode):
            return Type.STRING
        if instance_of_one(root, [AdditionNode, SubtractionNode, MultiplicationNode, DivisionNode, OpLessThanNode]):
            left = self.get_type(root.left)
            right = self.get_type(root.right)
            if not (left == Type.INT and right == Type.INT):
                error(root, "Type error: expected integer operands")
            return left
        if instance_of_one(root, [AndNode, OrNode]):
            left = self.get_type(root.left)
            right = self.get_type(root.right)
            if not (left == Type.BOOL and right == Type.BOOL):
                error(root, "Type error: expected boolean operands")
            return left
        if isinstance(root, OpEqualsNode):
            left = self.get_type(root.left)
            right = self.get_type(root.right)
            if not left == right:
                error(root, "Type error: expected operands to equals to be of same type")
            return left
        if isinstance(root, IdentifierNode):
            lookup_var = self.get_variable(get_identifier(root))
            if lookup_var is not None:
                return lookup_var
            error(root, "Variable {} used but not declared".format(get_identifier(root)))


def instance_of_one(obj, types):
    for type in types:
        if isinstance(obj, type):
            return True
    return False


def get_identifier(ident_node: IdentifierNode) -> str:
    return ident_node.identifier


def check(tree):
    # Used as a stack of dictionaries
    # When new scope is entered, dictionary pushed onto stack
    # Initially we have global only
    env = Environment()
    _do_check(tree, env)


def _do_check(root, env: Environment):
    if isinstance(root, ProgramNode):
        _do_check(root.get_children()[0], env)

    elif isinstance(root, StatementBlockNode):
        for statement in root.get_children():
            _do_check(statement, env)

    elif isinstance(root, StatementNode):
        return _do_check(root.get_children()[0], env)

    elif isinstance(root, DeclarationNode):
        variable_identifier = get_identifier(root.identifier)
        if env.get_variable(variable_identifier) is not None:
            error(root, "Variable {} already declared".format(variable_identifier))
        else:
            # Check types
            var_type = Type().from_ast_node(root.type)
            rhs_type = env.get_type(root.rhs)
            if not rhs_type == var_type:
                error(root, "Declaration has incorrect left and right types")
            env.add_variable(variable_identifier, var_type)

    elif isinstance(root, AssignmentNode):
        variable_identifier = get_identifier(root.identifier)
        variable_type = env.get_variable(variable_identifier)
        if variable_type is None:
            error(root, "Variable {} not declared".format(variable_identifier))
        else:
            if not env.get_type(root.rhs) == variable_type:
                error(root, "Variable has different type to rhs")

    else:
        return env.get_type(root)


def error(node: Node, message: str):
    print("Error at {}:{} to {}:{} - {}".format(node.start_position.line, node.start_position.column,
                                                node.stop_position.line, node.stop_position.column, message))

    exit(0)
