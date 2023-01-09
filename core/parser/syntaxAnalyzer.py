"""
AUTHORS: Ebin Paul, Aswin
DESCRIPTION: The following class is used to create an Abstract Syntax Tree (AST). The operators with higher precedence
            are the located lower in the tree mean while, operators with lower precedence are located higher in the tree.
            
REFERENCES: https://pages.cs.wisc.edu/~fischer/cs536.s06/course.hold/html/NOTES/4.SYNTAX-DIRECTED-TRANSLATION.html#astVsParse
            https://en.cppreference.com/w/cpp/language/operator_precedence
            https://cs.wmich.edu/~gupta/teaching/cs4850/sumII06/The%20syntax%20of%20C%20in%20Backus-Naur%20form.htm
            https://ruslanspivak.com/lsbasi-part3/
            https://ruslanspivak.com/lsbasi-part4/
            https://ruslanspivak.com/lsbasi-part5/
            https://ruslanspivak.com/lsbasi-part7/
            https://ruslanspivak.com/lsbasi-part8/
            https://dev.to/j0nimost/making-a-math-interpreter-ast-4848
            https://dev.to/j0nimost/making-a-math-interpreter-parser-52j8
"""


from core.lexer.lexicalAnalyzer import Lexer
from core.lexer.token import Token, TokenType

from .nodes import IdentifierNode, OperandNode, OperatorNode

"""
BNF :-
    <assignment> -> <variable> = <expression>
    <equality-expression> -> <relational> [(== | !=) <equality-expression>]*
    <relational> -> <expression> [(< | >)] <expression>
    <expression> -> <term> [(+ | -) <term>]*
    <term> -> <term> [(* | / | %) <power>]*
    <power> -> <factor> ^ <power> | <factor>
    <factor> -> <number> |  (expression) 
    <number> -> <int> <float> | <digit>
"""


class Parser:
    def __init__(self, input_string: str):
        self.__tokens = Lexer(input_string).get_tokens()
        self.current_token: Token = None
        self.position = 0
        self.parenthesis_stack = []
        self.next_token()

    def next_token(self):
        """
        assigns token at position value to the current token
        """
        try:
            if self.position < len(self.__tokens):

                self.current_token = self.__tokens[self.position]
                self.position += 1

                if self.current_token.type == TokenType.LEFT_PARENTHESIS:
                    self.parenthesis_stack.append(")")

                elif self.current_token.type == TokenType.RIGHT_PARENTHESIS:
                    try:
                        self.parenthesis_stack.pop()
                    except:
                        raise Exception("Missing parenthesis")

        except:
            raise Exception("Invalid expression.")

    def factor(self):
        """
        <factor> -> <number> |  (expression)
        """
        token = self.current_token

        if self.current_token.type == TokenType.END:
            return

        # if the expression starts with one of the following tokens,
        # then raise an exception
        if self.current_token.type in (
            TokenType.MULTIPLY,
            TokenType.MODULO,
            TokenType.DIVIDE,
            TokenType.CARET,
            TokenType.ASSIGN,
            TokenType.GT,
            TokenType.LT,
            TokenType.NEQ,
            TokenType.EQ,
        ):
            raise Exception("Invalid expression.")

        # set the left node as NULL/NONE is the current node encountered is a unary operator.
        elif self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
            self.next_token()
            return OperatorNode(None, token, self.term())

        # return an operand node if current node is integer or float
        elif token.type in (TokenType.INTEGER, TokenType.FLOAT):
            self.next_token()
            return OperandNode(token)

        elif token.type == TokenType.IDENTIFIER:
            self.next_token()
            return IdentifierNode(token)

        elif token.type == TokenType.LEFT_PARENTHESIS:
            self.next_token()
            result = self.expression()

            self.next_token()
            return result

    def power(self):
        """
        <power> -> <factor> ^ <power> | <factor>
        """
        result = self.factor()

        if self.current_token.type == TokenType.NOT:
            raise Exception("Invalid expression")

        while (
            self.current_token.type != TokenType.END
            and self.current_token
            and self.current_token.type == TokenType.CARET
        ):

            operator = self.current_token
            self.next_token()

            result = OperatorNode(result, operator, self.factor())

        return result

    def term(self):
        """
        method for parsing a term
        <term> -> <term> [(* | / | %) <power>]*
        """
        result = self.power()

        while (
            self.current_token.type != TokenType.END
            and self.current_token
            and self.current_token.type
            in (TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.MODULO)
        ):
            operator = self.current_token
            self.next_token()

            result = OperatorNode(result, operator, self.power())

        return result

    def expression(self):
        """
        method for parsing expression
        <expression> -> <term> [(+ | -) <term>]*
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
            self.next_token()
            result = OperatorNode(result, operator, self.term())

        return result

    def relational(self):
        """
        BNF for relational operators
        <relational> -> <expression> [(< | >)] <expression>
        """
        result = self.expression()
        while (
            self.current_token.type != TokenType.END
            and self.current_token
            and self.current_token.type in (TokenType.LT, TokenType.GT)
        ):
            operator = self.current_token
            self.next_token()
            result = OperatorNode(result, operator, self.expression())

        return result

    def equality(self):
        """
        BNF for relational operators
        <equality-expression> -> <relational> [(== | !=) <equality-expression>]*
        """
        result = self.relational()
        while (
            self.current_token.type != TokenType.END
            and self.current_token
            and self.current_token.type in (TokenType.EQ, TokenType.NEQ)
        ):
            operator = self.current_token
            self.next_token()
            result = OperatorNode(result, operator, self.relational())

        return result

    def assignment(self):
        """
        BNF for assignment
        <assignment> -> <variable> = <expression>
        """
        result = self.equality()
        while (
            self.current_token.type != TokenType.END
            and self.current_token
            and self.current_token.type == TokenType.ASSIGN
        ):
            operator = self.current_token
            self.next_token()
            result = OperatorNode(result, operator, self.equality())

        return result

    def parse(self):
        """
        Parses the tokens list and returns an AST (Abstract Syntax Tree)
        """
        result = self.assignment()

        if self.parenthesis_stack:
            raise Exception("Missing parenthesis")

        return result
