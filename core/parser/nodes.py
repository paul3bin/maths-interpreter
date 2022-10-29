from core.lexer.token import Token, TokenType


# Defining the Node
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
    def __init__(
        self, left_node: OperandNode, operator: TokenType, right_node: OperandNode
    ):
        self.left_node = left_node
        self.operator = operator
        self.right_node = right_node

    def __str__(self):
        return f"{self.left_node} {self.operator} {self.right_node}"

    def __repr__(self):
        return self.__str__()
