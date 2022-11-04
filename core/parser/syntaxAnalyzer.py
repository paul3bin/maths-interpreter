from core.lexer.token import Token, TokenType

from .nodes import OperandNode, OperatorNode

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

        if self.current_token.type == TokenType.END:
            return

        # set the left node as NULL/NONE is the current node encountered is a unary operator.
        elif self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
            self.get_next_token()
            return OperatorNode(None, token, self.term())

        # return an operand node if current node is integer or float
        elif token.type in (TokenType.INTEGER, TokenType.FLOAT):
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

        while (
            self.current_token.type != TokenType.END
            and self.current_token
            and self.current_token.type
            in (
                TokenType.MULTIPLY,
                TokenType.DIVIDE,
            )
        ):
            operator = self.current_token
            self.get_next_token()
            result = OperatorNode(result, operator, self.factor())

        return result

    def expression(self):
        """
        method for parsing expression
        expression -> term [(PLUS | MINUS) term]*
        """
        result = self.term()

        while (
            self.current_token.type != TokenType.END
            and self.current_token
            and self.current_token.type
            in (
                TokenType.PLUS,
                TokenType.MINUS,
            )
        ):
            operator = self.current_token
            self.get_next_token()
            result = OperatorNode(result, operator, self.term())

        return result

    def parse(self):
        """
        Parses the tokens list and returns an AST (Abstract Syntax Tree)
        """
        result = self.expression()

        # checking if opened Parentheses are closed
        if self.parenthesis_count % 2 != 0:
            raise Exception("Missing parenthesis")

        return result
