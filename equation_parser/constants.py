import operator
from enum import Enum


class NodeType(str, Enum):
    """Convenience enumeration of node type"""
    Unary = 'unary'
    Binary = 'binary'
    Constant = 'constant'
    Variable = 'variable'


class Operators(str, Enum):
    """Convenience enumeration listing supported operation"""
    ADD = 'add'
    SUB = 'sub'
    MUL = 'mul'
    DIV = 'div'
    POW = 'pow'
    NEG = 'neg'
    ID = 'id'

    @staticmethod
    def get(value):
        """Return the function corresponding the enumeration value"""
        return OPERATORS_FUNC.get(value)

    # @classmethod
    # def as_dict(cls) -> dict:
    #     """Returns Operators class as dictionary"""
    #     return {value.value: value for value in cls}


OPERATORS_FUNC = {
    Operators.ADD: operator.add,
    Operators.SUB: operator.sub,
    Operators.MUL: operator.mul,
    Operators.DIV: operator.truediv,
    Operators.POW: operator.pow,
    Operators.NEG: operator.neg,
    Operators.ID: lambda x: x,
}
