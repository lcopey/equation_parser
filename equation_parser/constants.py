import operator
from enum import Enum, auto


class Operators(Enum):
    """Convenience enumeration listing supported operation"""
    ADD = auto()
    SUB = auto()
    MUL = auto()
    DIV = auto()
    POW = auto()
    NEG = auto()
    ID = auto()

    @staticmethod
    def get(value):
        """Return the function corresponding the enumeration value"""
        return OPERATORS_FUNC.get(value)


OPERATORS_FUNC = {
    Operators.ADD: operator.add,
    Operators.SUB: operator.sub,
    Operators.MUL: operator.mul,
    Operators.DIV: operator.truediv,
    Operators.POW: operator.pow,
    Operators.NEG: operator.neg,
    Operators.ID: lambda x: x,
}
