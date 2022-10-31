import ast
from structlog import getLogger
from .base import Node, BinaryNode, ConstantNode, VariableNode, UnaryNode
from .constants import Operators

from typing import Union

logger = getLogger()


def eval_node(ast_node: Union[ast.Constant, ast.Name, ast.BinOp, ast.UnaryOp]) -> Node:
    """Evaluate and dispatch to one of eval method depending on the type of ast_node"""
    log = logger.bind(func='eval node')
    log.debug(ast_node)
    func = AST_EVALUATORS[type(ast_node)]
    return func(ast_node)


def eval_binop(ast_node: ast.BinOp) -> BinaryNode:
    """Defines a binary node"""
    log = logger.bind(func='eval binop')
    log.debug(ast.dump(ast_node))
    op_type = OPERATORS_MAP[type(ast_node.op)]
    op = Operators.get(op_type)
    return BinaryNode(left=eval_node(ast_node.left), right=eval_node(ast_node.right), func=op)


def eval_constant(ast_node: ast.Constant) -> ConstantNode:
    """Defines a constant node"""
    log = logger.bind(func='eval constant')
    log.debug(ast.dump(ast_node))
    return ConstantNode(value=ast_node.value)


def eval_name(ast_node: ast.Name) -> VariableNode:
    """Defines a variable node"""
    log = logger.bind(func='eval name')
    log.debug(ast.dump(ast_node))
    return VariableNode(value=ast_node.id)


def eval_unaryop(ast_node: ast.UnaryOp) -> UnaryNode:
    """Degines a unary operation node"""
    log = logger.bind(func='eval unary')
    log.debug(ast.dump(ast_node))
    op_type = OPERATORS_MAP[type(ast_node.op)]
    op = Operators.get(op_type)
    return UnaryNode(func=op, value=eval_node(ast_node.operand))


def from_string(equation_string: str) -> Node:
    """Build a tree starting from an equation string"""
    log = logger.bind(func='build tree')
    log.debug('Start building')
    ast_node = ast.parse(equation_string, '<string>', mode='eval')
    if isinstance(ast_node, ast.Expression):
        node_value = ast_node.body
    else:
        node_value = ast_node
    return eval_node(node_value)


AST_EVALUATORS = {
    ast.Constant: eval_constant,
    ast.Name: eval_name,
    ast.BinOp: eval_binop,
    ast.UnaryOp: eval_unaryop,
}

OPERATORS_MAP = {
    ast.Add: Operators.ADD,
    ast.Sub: Operators.SUB,
    ast.Mult: Operators.MUL,
    ast.Div: Operators.DIV,
    ast.Pow: Operators.POW,
    ast.USub: Operators.NEG,
    ast.UAdd: Operators.ID
}