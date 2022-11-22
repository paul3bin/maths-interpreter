"""
Authors: Max James, Christopher Gavey, Ebin Paul, Aswin, Soniya
Program: Mathematical visualisation software interpreter
Version: 2
Version Date: 08/11/2022
"""
from core.functions.zero_crossing import zeroCrossing
from core.interpreter import main

if __name__ == "__main__":
    # while True:
    #     input_string = input("Enter expression >> ")
    #     if input_string:
    #         print(main(input_string))

    #     continue
    final1 = zeroCrossing("x^2-25", "8")
    print(f"\n Zero Crossing at x = {final1}")
