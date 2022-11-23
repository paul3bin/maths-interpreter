"""
Authors: Max, Christopher, Ebin Paul, Aswin, Soniya
Program: Mathematical visualisation software interpreter

"""
from core.interpreter import main

if __name__ == "__main__":
    while True:
        input_string = input("Enter expression >> ")
        if input_string:
            print(main(input_string))

        continue
