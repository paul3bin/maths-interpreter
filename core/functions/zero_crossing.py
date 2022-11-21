# from ..interpreter import Interpreter
# from core.interpreter import Interpreter
# from .. import Interpreter
from interpreter import *


def derivative(expression: str, xval: str):
    d1 = Interpreter(f"d1=x+{0.000001}").execute()
    d2 = Interpreter(f"d2=x-{0.000001}").execute()

    newExpression1 = expression.replace("x", "d1")
    expr1 = Interpreter(newExpression1)
    dans1 = expr1.execute()

    newExpression2 = expression.replace("x", "d2")
    expr2 = Interpreter(newExpression2)
    dans2 = expr2.execute()

    dans3 = (dans1 - dans2) / 2 * 0.000001
    return dans3


def zeroCrossing(expression: str, x_value: str):
    # Assign the value of x in the interpreter
    val = Interpreter(f"x={x_value}")
    xval = val.execute()
    # Pass the expression
    expr = Interpreter(expression)
    ans = expr.execute()

    for _ in range(100):
        ans1 = abs(ans)
        # Assign the value of v1
        val1 = Interpreter(f"v1={ans1}").execute()
        # compare the value through interpreter
        if Interpreter("v1<0.00001").execute():
            break

        # call the derivative function
        d_value = derivative(expression, xval)
        ans2 = abs(d_value)
        # Assign the value of v2
        val2 = Interpreter(f"v2={ans2}").execute()
        # compare the value through interpreter
        if Interpreter("v2<0.00001").execute():
            break

        # update the value of xval and x (x of interpreter)***********
        ans3 = Interpreter(f"x=x-{ans/d_value}")
        xval = ans3.execute()

        expr = Interpreter(expression)
        ans = expr.execute()

    ans4 = Interpreter(f"x={xval}").execute()
    return ans4


if __name__ == "__main__":
    final1 = zeroCrossing("x^2-25", "8")
    print("\n Zero Crossing at x = {}".format(final1))
