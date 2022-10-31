from pydantic import BaseModel
from pydantic.validators import Callable, Any
import pandas as pd


class Node(BaseModel):
    """Basic structure for all nodes"""

    def __repr__(self):
        return f'<{self.__class__.__name__}>'

    def eval(self, *args):
        """General evaluation method"""
        raise NotImplementedError


class UnaryNode(Node):
    """Node implementing unary operation"""
    value: Node
    func: Callable

    def eval(self, datas: pd.DataFrame):
        """Apply func to value"""
        return self.func(self.value.eval(datas))


class BinaryNode(Node):
    """Node implementing binary operation"""
    left: Node
    right: Node
    func: Callable

    def eval(self, datas: pd.DataFrame):
        """Apply func to left and right value"""
        return self.func(self.left.eval(datas), self.right.eval(datas))

    def __repr__(self):
        return (f"""{super().__repr__()} {self.func}"""
                f"""\n\tleft={self.left.__repr__()}\n\tright={self.right.__repr__()}""")


class ConstantNode(Node):
    """Node implementing constant value"""
    value: Any

    def eval(self, datas: pd.DataFrame):
        """Return value"""
        return self.value


class VariableNode(Node):
    """Node implementing variable name"""
    value: str

    def eval(self, datas: pd.DataFrame):
        """Return the columns in datas named value"""
        return datas[self.value]
