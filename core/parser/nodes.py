"""
AUTHOR: Ebin Paul, Aswin Sasi
DESCRIPTION: The following classes are nodes of Abstract Syntax Tree (AST). Each class has a get_node_value method which returns,
            the value of that particular node
            
REFERENCES: https://ruslanspivak.com/lsbasi-part7/
            https://ruslanspivak.com/lsbasi-part8/
            https://dev.to/j0nimost/making-a-math-interpreter-ast-4848
            https://dev.to/j0nimost/making-a-math-interpreter-parser-52j8
"""

from core.lexer.token import Token, TokenType

# from core.functions import factorial

SYMBOL_TABLE = {}


class OperandNode:
    """
    Blueprint of a leaf node
    """

    def __init__(self, token: Token):
        self.token: Token = token
        self.__value = self.token.value

    def get_node_value(self):
        return self.__value

    def __str__(self):
        return f"{self.__value}"

    def __repr__(self):
        return self.__str__()


class IdentifierNode:
    def __init__(self, token: Token):
        self.token: Token = token
        self.__value = self.token.value

    def get_node_value(self):
        try:
            return SYMBOL_TABLE[self.__value]
        except:
            raise Exception(f"{self.__value} not defined.")

    def __str__(self):
        return self.__value

    def __repr__(self):
        return self.__str__()


# function delclarations


def factorial(f1: int):
    fact_answer = 1
    if f1 >= 0:
        while f1 >= 1:
            fact_answer *= f1
            f1 -= 1
        return fact_answer
    else:
        return "No factorial for negative numbers"


def sin_function(s1=int):
    sin_ans1 = (s1 % 360) * 3.1415 / 180
    sin_ans2 = sin_ans1
    for i in range(1, 20):
        y = (2 * i) + 1
        if i % 2 == 1:
            sin_ans2 -= (sin_ans1**y) / factorial(y)
        else:
            sin_ans2 += (sin_ans1**y) / factorial(y)
    return round(sin_ans2, 4)


def cos_function(s1=int):
    cos_ans1 = (s1 % 360) * 3.1415 / 180
    cos_ans2 = 1
    for i in range(1, 20):
        y = 2 * i
        if i % 2 == 1:
            cos_ans2 -= (cos_ans1**y) / factorial(y)
        else:
            cos_ans2 += (cos_ans1**y) / factorial(y)
    return round(cos_ans2, 3)


class FunctionNode:
    def __init__(self, token: Token, value):
        self.token: Token = token
        self.leaf_node: OperandNode or IdentifierNode = value

    def get_node_value(self):
        # return f"{self.token.value}({self.leaf_node})"
        if self.token.value == "fact":
            # return factorial(self.leaf_node.get_node_value())
            # return self.leaf_node.get_node_value()
            f_ans = factorial(self.leaf_node.get_node_value())
            return f_ans

        elif self.token.value == "sin":
            s_ans = sin_function(self.leaf_node.get_node_value())
            return s_ans

        elif self.token.value == "cos":
            c_ans = cos_function(self.leaf_node.get_node_value())
            return c_ans

    def __str__(self):
        return self.__value

    def __repr__(self):
        return self.__str__()


class OperatorNode:
    """
    Class definition for Operator (+, -, *, /, ^, %, <, >, =, ==, !, !=) node

    The left node can either be an operator node or an operand node.
    """

    def __init__(
        self,
        left_node: OperandNode or IdentifierNode or OperatorNode,
        operator: Token,
        right_node: OperandNode or IdentifierNode or OperatorNode,
    ):
        self.left_node = left_node
        self.operator = operator
        self.right_node = right_node

    def get_node_value(self):
        """
        returns result of arithmetic operation.
        """
        if self.operator.type == TokenType.PLUS:
            # checking for unary PLUS operator
            # if left node is none then the node is an unary operator
            # else return the result of arithmetic PLUS operation
            if self.left_node:
                return (
                    self.left_node.get_node_value() + self.right_node.get_node_value()
                )

            return +self.right_node.get_node_value()

        elif self.operator.type == TokenType.MINUS:
            # checking for unary MINUS operator
            # if left node is none then the node is an unary operator
            # else return the result of arithmetic MINUS operation
            if self.left_node:
                return (
                    self.left_node.get_node_value() - self.right_node.get_node_value()
                )

            return -self.right_node.get_node_value()

        elif self.operator.type == TokenType.MULTIPLY:
            return self.left_node.get_node_value() * self.right_node.get_node_value()

        elif self.operator.type == TokenType.DIVIDE:
            return self.left_node.get_node_value() / self.right_node.get_node_value()

        elif self.operator.type == TokenType.CARET:
            return self.left_node.get_node_value() ** self.right_node.get_node_value()

        elif self.operator.type == TokenType.MODULO:
            return self.left_node.get_node_value() % self.right_node.get_node_value()

        elif self.operator.type == TokenType.LT:
            return self.left_node.get_node_value() < self.right_node.get_node_value()

        elif self.operator.type == TokenType.GT:
            return self.left_node.get_node_value() > self.right_node.get_node_value()

        elif self.operator.type == TokenType.ASSIGN:
            if self.left_node.token.type == TokenType.IDENTIFIER:
                SYMBOL_TABLE[str(self.left_node)] = self.right_node.get_node_value()
                return SYMBOL_TABLE[str(self.left_node)]

            raise Exception("Invalid expression")

        elif self.operator.type == TokenType.EQ:
            return self.left_node.get_node_value() == self.right_node.get_node_value()

        elif self.operator.type == TokenType.NEQ:
            return self.left_node.get_node_value() != self.right_node.get_node_value()

    def __str__(self):
        return f"{self.left_node} {self.operator.type.name} {self.right_node}"

    def __repr__(self):
        return self.__str__()
