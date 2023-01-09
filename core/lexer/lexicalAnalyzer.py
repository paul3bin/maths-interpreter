"""
AUTHOR: Ebin Paul
DESCRIPTION: The following Lexer class goes through the input string and generates a list of tokens.
            
REFERENCES: https://ruslanspivak.com/lsbasi-part7/
            https://ruslanspivak.com/lsbasi-part8/
            https://dev.to/j0nimost/implementing-a-math-interpreter-using-c-part2-lexer-4i81
"""

from string import ascii_lowercase, ascii_uppercase, digits
from core.functions.functions import function
from .token import Token, TokenType

WHITESPACE = " \t"
ALLOWED_IDENTIFIERS = "".join(tuple(ascii_lowercase)) + "".join(tuple(ascii_uppercase))
ALLOWED_CHARACTERS = digits + "+-/*%()^=.<> \n\t" + ALLOWED_IDENTIFIERS
ALLOWED_OP_CHARACTERS = ("+", "-", "/", "*", "%", "(", ")", "^", "%", "=", "<", ">")

ALLOWED_FUNC = ("sin", "cos", "tan", "sqt", "lgn", "lgx", "l10")  # new - testing something out

OP_TOKEN_TYPE = (
    TokenType.MULTIPLY,
    TokenType.PLUS,
    TokenType.DIVIDE,
    TokenType.MINUS,
    TokenType.LEFT_PARENTHESIS,
    TokenType.CARET,
    TokenType.MODULO,
    TokenType.ASSIGN,
    TokenType.LT,
    TokenType.GT,
)
OPERAND_TOKEN_TYPE = (TokenType.INTEGER, TokenType.FLOAT)


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
        identifier_string = ""

        if self.__character_list:

            # iterating through all the chacters present in the input string list
            count = 0
            for character in self.__character_list:

                # This is causing issues relating to variables
                if character == '(':  # new - testing ideas

                    # 0 isn't correct cause what if func is used mid-expression
                    if len(self.__character_list) > 3:

                        left_par_instances = list(filter(lambda i: self.__character_list[i] == '(', range(len(self.__character_list))))
                        name = ''.join(self.__character_list[self.__character_list.index(character) - 3:self.__character_list.index(character)])

                        if name in ALLOWED_FUNC:
                            print('Hello. This line is running.')
                            count += 1

                            if count > 1:
                                name = self.__character_list[left_par_instances[count-1]-3] + self.__character_list[left_par_instances[count-1]-2] + self.__character_list[left_par_instances[count-1]-1]

                            self.__tokens.append(Token(TokenType.FUNCTION, name))
                            self.__tokens.append(Token(TokenType.LEFT_PARENTHESIS, "'('"))
                        else:
                            print('This line is running.')
                            self.__tokens.append(Token(TokenType.LEFT_PARENTHESIS, "'('"))
                            self.__tokens.append(Token(TokenType.IDENTIFIER, name))
                    else:
                        print('Nope. This line is running.')
                        self.__tokens.append(Token(TokenType.LEFT_PARENTHESIS, "'('"))

                # Checking if characters present in the input string are allowed or not
                if character not in ALLOWED_CHARACTERS:
                    raise Exception("Invalid character(s).")

                # skipping the whitespace characters
                if character in WHITESPACE:
                    continue

                # identifying if current character is a digit
                if character.isdigit():
                    if identifier_string:
                        identifier_string += character
                        continue
                    number_string += character

                elif character == ".":
                    number_string += character

                elif character in ALLOWED_IDENTIFIERS:
                    identifier_string += character

                # checking if current character is one of the following characters:
                # +, -, *, /, (, )
                elif character in ALLOWED_OP_CHARACTERS:

                    # checking if alphabets are present in the number string.
                    # If yes, append the identifier token to the token list and assign empty string to the identifier_string variable.
                    if identifier_string:
                        if number_string:
                            raise Exception("Invalid expression.")

                        # Max testing rn

                        # -2 before function is before left_parenthesis
                        if len(self.__tokens)-2 >= 0:
                            if self.__tokens[len(self.__tokens)-2].type != TokenType.FUNCTION: # testing - Max rn
                                self.__tokens.append(Token(TokenType.IDENTIFIER, identifier_string))
                        else:
                            self.__tokens.append(Token(TokenType.IDENTIFIER, identifier_string))
                        identifier_string = ""

                    # checking if numbers are present in the number string.
                    # If yes, append the integer token to the token list and assign empty string to the number_string variable.
                    # If no, move on to identifying the characters and append to tokens list.
                    elif number_string:
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

                    #elif character == "(":
                        #self.__tokens.append(Token(TokenType.LEFT_PARENTHESIS, "'('"))

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

                    elif character == "=":
                        # if token list is empty and,
                        # the first character encountered is plus
                        # then raise an exception
                        if not self.__tokens:
                            raise Exception("Invalid expression")

                        # if the last token in token list
                        # is one of the TokenType is other than IDENTIFIER
                        # then raise an exception
                        elif (
                            self.__tokens[-1].type in OP_TOKEN_TYPE
                            or self.__tokens[-1].type in OPERAND_TOKEN_TYPE
                        ):
                            raise Exception("Invalid expression")
                        else:
                            self.__tokens.append(Token(TokenType.ASSIGN, "'='"))

                    elif character == "<":
                        # if token list is empty and,
                        # the first character encountered is plus
                        # then raise an exception
                        if not self.__tokens:
                            raise Exception("Invalid expression")

                        # if the last token in token list
                        # is one of the TokenTypes other than INTEGER , FLOAT and IDENTIFIER
                        # then raise an exception
                        elif self.__tokens[-1].type in OP_TOKEN_TYPE:
                            raise Exception("Invalid expression")

                        else:
                            self.__tokens.append(Token(TokenType.LT, "'<'"))

                    elif character == ">":
                        # if token list is empty and,
                        # the first character encountered is plus
                        # then raise an exception
                        if not self.__tokens:
                            raise Exception("Invalid expression")

                        # if the last token in token list
                        # is one of the TokenTypes other than INTEGER , FLOAT and IDENTIFIER
                        # then raise an exception
                        elif self.__tokens[-1].type in OP_TOKEN_TYPE:
                            raise Exception("Invalid expression")

                        else:
                            self.__tokens.append(Token(TokenType.GT, "'>'"))

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

            # if identifier string is not empty once loop ends,then add the identifier token to the list
            if identifier_string:
                self.__tokens.append(Token(TokenType.IDENTIFIER, identifier_string))
        else:
            self.__tokens.append(Token(TokenType.END))

    def get_tokens(self) -> list:
        """
        calls the generate tokens method and returns the list of tokens
        """
        self.generate_tokens()

        type_list = []  # list of TokenType class for the inputted command

        for x in self.__tokens:
            type_list.append(x.type)

        # while there's still a function
        for x in self.__tokens:

            # think it's to do with the order of the while loop and if statement
            if x.type == TokenType.FUNCTION:
                while (TokenType.FUNCTION in type_list):
                    if type_list.count(TokenType.LEFT_PARENTHESIS) != 0:
                        if type_list.count(TokenType.LEFT_PARENTHESIS) == type_list.count(TokenType.RIGHT_PARENTHESIS):

                            # think this might need to be switched around
                            start = list(filter(lambda i: type_list[i] == TokenType.LEFT_PARENTHESIS, range(len(type_list)))).pop()  # also removes last element
                            end = list(filter(lambda i: type_list[i] == TokenType.RIGHT_PARENTHESIS, range(len(type_list))))[0]  # DOESNT remove last element yet

                            if self.__tokens[start-1].type == TokenType.FUNCTION:  # if theres a function before the inner brackets list - find out what the function is

                                if self.__tokens[start-1].value == 'sin':
                                    self.__tokens[start-1] = function(self.__tokens[start+1:end]).sin()  # just for testing and fun
                                    type_list[start - 1] = function(self.__tokens[start + 1:end]).sin().type
                                elif self.__tokens[start-1].value == 'cos':
                                    self.__tokens[start-1] = function(self.__tokens[start+1:end]).cos()  # just for testing and fun
                                    type_list[start - 1] = function(self.__tokens[start + 1:end]).cos().type
                                elif self.__tokens[start - 1].value == 'tan':
                                    self.__tokens[start-1] = function(self.__tokens[start+1:end]).tan()  # just for testing and fun
                                    type_list[start - 1] = function(self.__tokens[start + 1:end]).tan().type
                                elif self.__tokens[start-1].value == 'lgx':
                                    self.__tokens[start-1] = function(self.__tokens[start+1:end]).lgx()  # just for testing and fun
                                    type_list[start - 1] = function(self.__tokens[start + 1:end]).lgx().type
                                elif self.__tokens[start-1].value == 'l10':
                                    self.__tokens[start-1] = function(self.__tokens[start+1:end]).l10()  # just for testing and fun
                                    type_list[start - 1] = function(self.__tokens[start + 1:end]).l10().type
                                elif self.__tokens[start - 1].value == 'lgn':
                                    self.__tokens[start-1] = function(self.__tokens[start+1:end]).lgn()  # just for testing and fun
                                    type_list[start - 1] = function(self.__tokens[start + 1:end]).lgn().type
                                elif self.__tokens[start-1].value == 'sqt':
                                    print(self.__tokens)
                                    self.__tokens[start - 1] = function(self.__tokens[start + 1:end]).sqt()  # just for testing and fun
                                    type_list[start-1] = function(self.__tokens[start+1:end]).sqt().type

                                del self.__tokens[start:end+1]  # deletes the parenthesis
                                del type_list[start:end+1]

                        else:
                            raise Exception('Missing parenthesis(es)')

        return self.__tokens
