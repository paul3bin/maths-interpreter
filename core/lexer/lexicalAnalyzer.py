"""
TO ADD:

1) VARIABLE DECLARATION
2) Executing expressions with variables in it

"""


from .token import Token, TokenType

WHITESPACE = " \t"
ALLOWED_CHARACTERS = "0123456789+-/*%()^. \n\t"
ALLOWED_OP_CHARACTERS = ("+", "-", "/", "*", "%", "(", ")", "^", "%")
OP_TOKEN_TYPE = (
    TokenType.MULTIPLY,
    TokenType.PLUS,
    TokenType.DIVIDE,
    TokenType.MINUS,
    TokenType.LEFT_PARENTHESIS,
    TokenType.CARET,
    TokenType.MODULO,
)


class Lexer:
    def __init__(self, input_string: str):
        """
        Reserved constructor method
        """
        # creating a list of characters from the string
        # eg: 12+24  -> ['1', '2', '+', '2', '4']
        self.__character_list = list(input_string)

        self.__tokens = []

    def generate_tokens(self):
        """
        Generates tokens and appends it to to tokens list
        """
        # intializing the number string as an empty string
        number_string = ""

        if self.__character_list:

            # iterating through all the chacters present in the input string list
            for character in self.__character_list:

                # Checking if characters present in the input string are allowed or not
                if character not in ALLOWED_CHARACTERS:
                    raise Exception("Invalid character(s).")

                # skipping the whitespace characters
                if character in WHITESPACE:
                    continue

                # identifying if current character is a digit
                if character.isdigit():
                    number_string += character

                elif character == ".":
                    number_string += character

                # checking if current character is one of the following characters:
                # +, -, *, /, (, )
                elif character in ALLOWED_OP_CHARACTERS:

                    # checking if numbers are present in the number string.
                    # If yes, append the integer token to the token list and assign empty string to the number_string variable.
                    # If no, move on to identifying the characters and append to tokens list.
                    if number_string:
                        if "." in number_string:
                            if len(number_string) > 1:
                                self.__tokens.append(
                                    Token(TokenType.FLOAT, float(number_string))
                                )
                                number_string = ""
                            else:
                                raise Exception("Invalid expression.")

                        else:
                            self.__tokens.append(
                                Token(TokenType.INTEGER, int(number_string))
                            )
                            number_string = ""

                    if character == "+":
                        self.__tokens.append(Token(TokenType.PLUS, "'+'"))

                    elif character == "-":
                        self.__tokens.append(Token(TokenType.MINUS, "'-'"))

                    elif character == "*":
                        # if token list is empty and,
                        # the first character encountered is plus
                        # then raise an exception
                        if not self.__tokens:
                            raise Exception("Invalid expression")

                        # if the last token in token list
                        # is one of the TokenTypes other than INTEGER and FLOAT
                        # then raise an exception
                        elif self.__tokens[-1].type in OP_TOKEN_TYPE:
                            raise Exception("Invalid expression")

                        else:
                            self.__tokens.append(Token(TokenType.MULTIPLY, "'*'"))

                    elif character == "/":
                        # if token list is empty and,
                        # the first character encountered is plus
                        # then raise an exception
                        if not self.__tokens:
                            raise Exception("Invalid expression")

                        # if the last token in token list
                        # is one of the TokenTypes other than INTEGER and FLOAT
                        # then raise an exception
                        elif self.__tokens[-1].type in OP_TOKEN_TYPE:
                            raise Exception("Invalid expression")
                        else:
                            self.__tokens.append(Token(TokenType.DIVIDE, "'/'"))

                    elif character == "(":
                        self.__tokens.append(Token(TokenType.LEFT_PARENTHESIS, "'('"))

                    elif character == ")":
                        self.__tokens.append(Token(TokenType.RIGHT_PARENTHESIS, "')'"))

                    elif character == "^":
                        # if token list is empty and,
                        # the first character encountered is plus
                        # then raise an exception
                        if not self.__tokens:
                            raise Exception("Invalid expression")

                        # if the last token in token list
                        # is one of the TokenTypes other than INTEGER and FLOAT
                        # then raise an exception
                        elif self.__tokens[-1].type in OP_TOKEN_TYPE:
                            raise Exception("Invalid expression")
                        else:
                            self.__tokens.append(Token(TokenType.CARET, "'^'"))

                    elif character == "%":
                        # if token list is empty and,
                        # the first character encountered is plus
                        # then raise an exception
                        if not self.__tokens:
                            raise Exception("Invalid expression")

                        # if the last token in token list
                        # is one of the TokenTypes other than INTEGER and FLOAT
                        # then raise an exception
                        elif self.__tokens[-1].type in OP_TOKEN_TYPE:
                            raise Exception("Invalid expression")
                        else:
                            self.__tokens.append(Token(TokenType.MODULO, "'%'"))

            # if number string is not empty once loop ends,then add the integer token to the list
            if number_string:
                if "." in number_string:
                    if len(number_string) > 1:
                        self.__tokens.append(
                            Token(TokenType.FLOAT, float(number_string))
                        )
                        number_string = ""
                    else:
                        raise Exception("Invalid expression.")

                else:
                    self.__tokens.append(Token(TokenType.INTEGER, int(number_string)))
        else:
            self.__tokens.append(Token(TokenType.END))

    def get_tokens(self) -> list:
        """
        calls the generate tokens method and returns the list of tokens
        """
        self.generate_tokens()
        return self.__tokens
