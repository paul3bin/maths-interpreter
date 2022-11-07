from core.parser.nodes import Token, TokenType


class Interpreter:
    def __init__(self, root_node):
        self.__root_node = root_node

    def execute(self):
        return self.__root_node.get_node_value()
