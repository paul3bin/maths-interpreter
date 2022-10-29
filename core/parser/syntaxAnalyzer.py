from core.lexer.token import Token, TokenType

from .nodes import OperatorNode, OperandNode

"""
BNF :-

    expression -> term [(PLUS | MINUS) term]*
    term -> factor [(MULTIPLY | DIVIDE) factor]*
    factor -> NUMBER | LEFT_PARENTHESIS expression RIGHT_PARENTHESIS

"""


class Parser:
    def __init__(self, tokens: list):
        self.__tokens = tokens
        self.current_token: Token = None
        self.position = 0
        self.get_next_token()
        self.parenthesis_count = 0

    def get_next_token(self):
        """
        assigns token at position value to the current token
        """
        try:
            if self.position < len(self.__tokens):

                self.current_token = self.__tokens[self.position]
                self.position += 1

                if self.current_token.type in (
                    TokenType.LEFT_PARENTHESIS,
                    TokenType.RIGHT_PARENTHESIS,
                ):
                    self.parenthesis_count += 1

        except:
            raise Exception("Invalid expression.")

    def factor(self):
        """
        factor -> NUMBER | LEFT_PARENTHESIS expression RIGHT_PARENTHESIS
        """
        token = self.current_token

        if token.type in (TokenType.INTEGER, TokenType.FLOAT):
            self.get_next_token()
            return OperandNode(token)

        elif token.type == TokenType.LEFT_PARENTHESIS:
            self.get_next_token()
            result = self.expression()

            self.get_next_token()
            return result

    def term(self):
        """
        method for parsing a term
        term -> factor [(MULTIPLY | DIVIDE) factor]*
        """
        result = self.factor()

        if self.current_token and self.current_token.type in (
            TokenType.MULTIPLY,
            TokenType.DIVIDE,
        ):
            operator = self.current_token
            self.get_next_token()
            result = OperatorNode(result, operator.type.name, self.factor())

        return result

    def expression(self):
        """
        method for parsing expression
        expression -> term [(PLUS | MINUS) term]*
        """
        result = self.term()

        if self.current_token and self.current_token.type in (
            TokenType.PLUS,
            TokenType.MINUS,
        ):
            operator = self.current_token
            self.get_next_token()
            result = OperatorNode(result, operator.type.name, self.term())

        return result

    def parse(self):
        result = self.expression()

        if self.parenthesis_count % 2 != 0:
            raise Exception("Missing parenthesis")

        return result
