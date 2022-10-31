from collections import OrderedDict
import pandas as pd
from .constants import Operators, NodeType
from typing import Union


def from_dict(datas: dict):
    node_type = datas.pop('type')
    node_class = NODES_DEFINITION[node_type]
    return node_class(**datas)


class Node:
    """Basic structure for all nodes"""

    def __repr__(self):
        return f'<{self.__class__.__name__}>'

    def eval(self, *args):
        """General evaluation method"""
        raise NotImplementedError

    def serialize(self) -> OrderedDict:
        """Serialize to dict"""
        raise NotImplementedError


class UnaryNode(Node):
    """Node implementing unary operation"""

    def __init__(self, value: Union[Node, dict], func_type):
        if isinstance(value, dict):
            value = from_dict(value)
        self.value = value
        self.func_type = func_type
        self.func = Operators.get(func_type)

    def eval(self, datas: pd.DataFrame):
        """Apply func to value"""
        return self.func(self.value.eval(datas))

    def serialize(self) -> OrderedDict:
        """Serialize to Ordered dict"""
        return OrderedDict([('type', NodeType.Unary),
                            ('value', self.value.serialize()),
                            ('func_type', self.func_type)])


class BinaryNode(Node):
    """Node implementing binary operation"""

    def __init__(self, left: Union[Node, dict], right: Union[Node, dict], func_type):
        if isinstance(left, dict):
            left = from_dict(left)
        if isinstance(right, dict):
            right = from_dict(right)
        self.left = left
        self.right = right
        self.func_type = func_type
        self.func = Operators.get(func_type)

    def eval(self, datas: pd.DataFrame):
        """Apply func to left and right value"""
        return self.func(self.left.eval(datas), self.right.eval(datas))

    def __repr__(self):
        return (f"""{super().__repr__()} {self.func}"""
                f"""\n\tleft={self.left.__repr__()}\n\tright={self.right.__repr__()}""")

    def serialize(self) -> OrderedDict:
        return OrderedDict([('type', NodeType.Binary),
                            ('left', self.left.serialize()),
                            ('right', self.right.serialize()),
                            ('func_type', self.func_type)])


class ConstantNode(Node):
    """Node implementing constant value"""

    def __init__(self, value):
        self.value = value

    def eval(self, datas: pd.DataFrame):
        """Return value"""
        return self.value

    def serialize(self) -> OrderedDict:
        """Serialize as OrderedDict"""
        return OrderedDict([('type', NodeType.Constant),
                            ('value', self.value)])


class VariableNode(Node):
    """Node implementing variable name"""

    def __init__(self, value):
        self.value = value

    def eval(self, datas: pd.DataFrame):
        """Return the columns in datas named value"""
        return datas[self.value]

    def serialize(self) -> OrderedDict:
        """Serialize as OrderedDict"""
        return OrderedDict([('type', NodeType.Variable),
                            ('value', self.value)])


NODES_DEFINITION = {NodeType.Unary: UnaryNode,
                    NodeType.Binary: BinaryNode,
                    NodeType.Constant: ConstantNode,
                    NodeType.Variable: VariableNode}
