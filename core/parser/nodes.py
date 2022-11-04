from core.lexer.token import Token, TokenType


class OperandNode:
    """
    Blueprint of a leaf node
    """

    def __init__(self, token):
        self.token: Token = token
        self.__value = self.token.value

    def get_node_value(self):
        return self.__value

    def __str__(self):
        return f"{self.__value}"

    def __repr__(self):
        return self.__str__()


class OperatorNode:
    """
    Class definition for Operator (+, -, *, /) node

    The left node can either be an operator node or an operand node.
    """

    def __init__(
        self,
        left_node: OperandNode,
        token: Token,
        right_node: OperandNode,
    ):
        self.left_node = left_node
        self.token = token
        self.right_node = right_node

    def get_node_value(self):
        """
        returns result of arithmetic operation.
        """
        if self.token.type == TokenType.PLUS:
            if self.left_node != None:
                return (
                    self.left_node.get_node_value() + self.right_node.get_node_value()
                )
            return self.right_node.get_node_value()

        elif self.token.type == TokenType.MINUS:
            if self.left_node != None:
                return (
                    self.left_node.get_node_value() - self.right_node.get_node_value()
                )

            return -self.right_node.get_node_value()

        elif self.token.type == TokenType.MULTIPLY:
            return self.left_node.get_node_value() * self.right_node.get_node_value()

        elif self.token.type == TokenType.DIVIDE:
            return self.left_node.get_node_value() / self.right_node.get_node_value()

    def __str__(self):
        return f"{self.left_node} {self.token.type.name} {self.right_node}"

    def __repr__(self):
        return self.__str__()
