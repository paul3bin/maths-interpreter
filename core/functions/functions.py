from core.lexer.token import Token, TokenType
import re

class function:
    tokens = []

    def __init__(self, tokens):
        self.tokens = tokens

        # TO DO:
        # find out if there's a variable within the tokens
        # turn the variable into its value
        # In general, variables need to be looked into
        # Somehow import the symbols_table from the parser?

    def sin(self):
        return Token(TokenType.INTEGER, 1)

    def cos(self):
        return Token(TokenType.INTEGER, 2)

    def tan(self):
        return Token(TokenType.INTEGER, 3)

    def sqt(self):

        print('hi')

        toks = self.tokens

        if len(self.tokens) > 1:  # check if tokens is longer than 1
            # calculate expression
            build = ""
            for i in self.tokens:
                build += re.sub('\'', '', str(self.tokens[self.tokens.index(i)].value))

            toks = [Token(TokenType.FLOAT, eval(build))]

        if toks[0].type in (TokenType.INTEGER, TokenType.FLOAT):  # check that the first integer is either a float or integer
            number = toks[0].value
        else:
            raise Exception('Invalid parameters')

        answer = number**(1/2)  # how to do the square root in python

        return Token(TokenType.FLOAT, answer)

    def lgn(self):
        return Token(TokenType.INTEGER, 4)

    def lgx(self):
        return Token(TokenType.INTEGER, 5)

    def l10(self):
        return Token(TokenType.INTEGER, 6)
