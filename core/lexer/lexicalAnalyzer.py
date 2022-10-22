# TO ADD:
# 1) ADD FLOATS
# 2) ADD NEGATIVE NUMBERS
# 3) POWER TO FUNTIONALITY

# 4)VARIABLE DECLARATION + ADD VARIABLES TOGETHER

# ------- DEADLINE FOR FUNCTIONALITY


from .token import Token, TokenType

WHITESPACE = " \n\t"


class Lexer:
    def __init__(self, input_string: str):
        """
        Rserved constructor method
        """
        # creating a list of characters from the string
        self.__string_character_list = list(input_string)  # 1+2 -> ['1', '+', '2']
        self.__tokens = []

    def generate_tokens(self):
        """
        Generates tokens and appends it to to tokens list
        """
        # intializing the number string as an empty string
        number_string = ""

        # iterating through all the chacters present in the input string list
        for character in self.__string_character_list:

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
            elif character in ["+", "-", "/", "*", "(", ")"]:

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
                    self.__tokens.append(Token(TokenType.MULTIPLY, "'*'"))
                elif character == "/":
                    self.__tokens.append(Token(TokenType.DIVIDE, "'/'"))
                elif character == "(":
                    self.__tokens.append(Token(TokenType.LEFT_PARENTHESIS, "'('"))
                elif character == ")":
                    self.__tokens.append(Token(TokenType.RIGHT_PARENTHESIS, "')'"))

        # if number string is not empty once loop ends,then add the integer token to the list
        if number_string:
            if "." in number_string:
                if len(number_string) > 1:
                    self.__tokens.append(Token(TokenType.FLOAT, float(number_string)))
                    number_string = ""
                else:
                    raise Exception("Invalid expression.")

            else:
                self.__tokens.append(Token(TokenType.INTEGER, int(number_string)))

    def get_tokens(self) -> list:
        """
        calls the generate tokens method and returns the list of tokens
        """
        self.generate_tokens()
        return self.__tokens
