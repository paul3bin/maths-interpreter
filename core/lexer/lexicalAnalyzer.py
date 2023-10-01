"""
AUTHOR: Ebin Paul, Aswin Sasi
DESCRIPTION: The following Lexer class goes through the input string and generates a list of tokens.
            
REFERENCES: https://ruslanspivak.com/lsbasi-part7/
            https://ruslanspivak.com/lsbasi-part8/
            https://dev.to/j0nimost/implementing-a-math-interpreter-using-c-part2-lexer-4i81
"""

from string import ascii_lowercase, ascii_uppercase, digits

from core.lexer.token import Token, TokenType

WHITESPACE = " \n\t"
ALLOWED_IDENTIFIERS = "".join(tuple(ascii_lowercase)) + "".join(tuple(ascii_uppercase))

ALLOWED_OPERATORS = {
    "+": TokenType.PLUS,
    "-": TokenType.MINUS,
    "*": TokenType.MULTIPLY,
    "/": TokenType.DIVIDE,
    "=": TokenType.ASSIGN,
    "==": TokenType.EQ,
    "!": TokenType.NOT,
    "!=": TokenType.NEQ,
    "(": TokenType.LEFT_PARENTHESIS,
    ")": TokenType.RIGHT_PARENTHESIS,
    "%": TokenType.MODULO,
    "^": TokenType.CARET,
    "<": TokenType.LT,
    ">": TokenType.GT,
}

OTHER_TOKENS = {
    "ID": TokenType.IDENTIFIER,
    "INT": TokenType.INTEGER,
    "FLOAT": TokenType.FLOAT,
    "END": TokenType.END,
    "FUNC": TokenType.FUNC,
}

ALLOWED_CHARACTERS = (
    digits + "".join(ALLOWED_OPERATORS.keys()) + ALLOWED_IDENTIFIERS + "."
)

ALLOWED_FUNCTION = ("sin", "cos", "tan", "fact", "root")


class Lexer:
    def __init__(self, input_string: str):
        """
        Reserved constructor method
        """
        # creating a list of characters from the string
        # eg: 12+24  -> ['1', '2', '+', '2', '4']
        self.__character_list = list(input_string)

        self.__tokens = []

    def add_token_to_list(self, token_char: str, value=None) -> None:
        if value != None:
            self.__tokens.append(Token(OTHER_TOKENS[token_char], value))
        else:
            if token_char == "END":
                self.__tokens.append(Token(OTHER_TOKENS[token_char]))
                return
            self.__tokens.append(Token(ALLOWED_OPERATORS[token_char], token_char))

    def tokenize_number(self, number_string):
        # checking if numbers are present in the number string.
        # If yes, append the integer token to the token list and assign empty string to the number_string variable.
        # If no, move on to identifying the characters and append to tokens list.
        if "." in number_string:
            if len(number_string) > 1:
                self.add_token_to_list("FLOAT", float(number_string))
                return ""
            else:
                raise Exception("Invalid expression.")

        else:
            self.add_token_to_list("INT", int(number_string))

        return ""

    def generate_tokens(self) -> None:
        """
        Identifies each token from the input string and appends it to the tokens list
        """
        # intializing the number string and identifier string as an empty string
        number_string = ""
        identifier_string = ""

        if self.__character_list:
            # iterating through all the chacters present in the input string list
            for character in self.__character_list:
                # skipping the whitespace characters
                if character in WHITESPACE:
                    continue

                # Checking if characters present in the input string are allowed or not
                if character not in ALLOWED_CHARACTERS:
                    raise Exception("Invalid character(s).")

                # identifying if current character is a digit
                if character.isdigit():
                    if identifier_string:
                        identifier_string += character
                    else:
                        number_string += character

                elif character == ".":
                    number_string += character

                elif character in ALLOWED_IDENTIFIERS:
                    if (
                        character == "e"
                        and len(identifier_string) == 0
                        and number_string
                    ):
                        number_string = self.tokenize_number(number_string)
                        self.add_token_to_list("*")
                        self.tokenize_number("10")
                        self.add_token_to_list("^")
                        continue
                    identifier_string += character

                # checking if current character is one of the allowed operand characters:
                elif character in ALLOWED_OPERATORS.keys():
                    # checking if alphabets are present in the number string.
                    # If yes, append the identifier token to the token list and assign empty string to the identifier_string variable.
                    if identifier_string:
                        if number_string:
                            raise Exception("Invalid expression.")

                        if character == "(":
                            if identifier_string in ALLOWED_FUNCTION:
                                self.add_token_to_list("FUNC", identifier_string)
                                self.add_token_to_list(character)
                                identifier_string = ""
                                continue
                            else:
                                raise Exception("Function not defined.")

                        self.add_token_to_list("ID", identifier_string)

                        identifier_string = ""

                    # tokenizing number
                    elif number_string:
                        number_string = self.tokenize_number(number_string)

                    # Checking if the current character is = operator,
                    # and appending a token with token-type ASSIGN to the tokens list
                    elif character == "=":
                        # if the previous token is of TokenType ASSIGN,
                        # then replace it with EQ token
                        if self.__tokens[-1].type == TokenType.ASSIGN:
                            self.__tokens.pop()
                            self.add_token_to_list("==")
                            continue

                        # if the previous token is of TokenType ASSIGN,
                        # then replace it with NEQ token
                        elif self.__tokens[-1].type == TokenType.NOT:
                            self.__tokens.pop()
                            self.add_token_to_list("!=")
                            continue

                        # if the previous token is of TokenType EQ or NEQ,
                        # then raise exception
                        elif self.__tokens[-1].type in (TokenType.EQ, TokenType.NEQ):
                            raise Exception(
                                "Invalid expression. No more than two (=) characters allowed"
                            )

                    # adding the appropriate token based on the current character.
                    self.add_token_to_list(character)

            # if number string is not empty once loop ends,then add the integer token to the list
            if number_string:
                number_string = self.tokenize_number(number_string)

            # if identifier string is not empty once loop ends,then add the identifier token to the list
            if identifier_string:
                self.add_token_to_list("ID", identifier_string)
        else:
            self.add_token_to_list("END")

    def get_tokens(self) -> list:
        """
        calls the generate tokens method and returns the list of tokens
        """
        self.generate_tokens()
        return self.__tokens
