from ..interpreter import main


def derivative(expression: str, xval: str):
    d1 = main(f"d1=x+{0.000001}")
    d2 = main(f"d2=x-{0.000001}")

    newExpression1 = expression.replace("x", "d1")
    expr1 = main(newExpression1)
    dans1 = expr1

    newExpression2 = expression.replace("x", "d2")
    expr2 = main(newExpression2)
    dans2 = expr2

    dans3 = (dans1 - dans2) / 2 * 0.000001
    return dans3


def zeroCrossing(expression: str, x_value: str):
    # Assign the value of x in the interpreter
    val = main(f"x={x_value}")
    xval = val
    # Pass the expression
    expr = main(expression)
    ans = expr

    for _ in range(100):
        ans1 = abs(ans)
        # Assign the value of v1
        val1 = main(f"v1={ans1}")
        # compare the value through interpreter
        if main("v1<0.00001"):
            break

        # call the derivative function
        d_value = derivative(expression, xval)
        ans2 = abs(d_value)
        # Assign the value of v2
        val2 = main(f"v2={ans2}")
        # compare the value through main
        if main("v2<0.00001"):
            break

        # update the value of xval and x (x of interpreter)***********
        ans3 = main(f"x=x-{ans}/{d_value}")
        xval = ans3

        expr = main(expression)
        ans = expr

    ans4 = main(f"x={xval}")
    return ans4
