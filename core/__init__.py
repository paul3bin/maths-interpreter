import os
import sys

from .interpreter import Interpreter

sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def main_execute(input_string: str):
    interpreter = Interpreter(input_string)

    result = interpreter.execute()

    return result
