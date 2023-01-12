from core import main_execute


def derivative(expression: str, xval: str):
    d1 = main_execute(f"d1=x+{0.000001}")
    d2 = main_execute(f"d2=x-{0.000001}")

    newExpression1 = expression.replace("x", "d1")
    expr1 = main_execute(newExpression1)
    dans1 = expr1

    newExpression2 = expression.replace("x", "d2")
    expr2 = main_execute(newExpression2)
    dans2 = expr2

    dans3 = (dans1 - dans2) / 2 * 0.000001
    return dans3


def zeroCrossing(expression: str, x_value: str):
    # Assign the value of x in the interpreter
    val = main_execute(f"x={x_value}")
    xval = val
    # Pass the expression
    expr = main_execute(expression)
    ans = expr

    for _ in range(100):
        ans1 = abs(ans)
        # Assign the value of v1
        val1 = main_execute(f"v1={ans1}")
        # compare the value through interpreter
        if main_execute("v1<0.00001"):
            break

        # call the derivative function
        d_value = derivative(expression, xval)
        ans2 = abs(d_value)
        # Assign the value of v2
        val2 = main_execute(f"v2={ans2}")
        # compare the value through main_execute
        if main_execute("v2<0.00001"):
            break

        # update the value of xval and x (x of interpreter)***********
        ans3 = main_execute(f"x=x-{ans}/{d_value}")
        xval = ans3

        expr = main_execute(expression)
        ans = expr

    ans4 = main_execute(f"x={xval}")
    return ans4


def bisection_method(function_exp, initial_value, final_value):

    main_execute(f"x={initial_value}")
    f_of_initial_value = main_execute(f"{function_exp}")
    main_execute(f"x={final_value}")
    f_of_final_value = main_execute(f"{function_exp}")

    if f_of_initial_value * f_of_final_value >= 0:
        return "No roots"

    while True:

        middle_value = (final_value + initial_value) / 2

        main_execute(f"x={middle_value}")
        f_of_middle_value = main_execute(f"{function_exp}")

        if f_of_middle_value == 0 or ((final_value - initial_value) / 2) < 0.0005:
            return middle_value

        if (f_of_middle_value * f_of_initial_value) < 0:
            final_value = middle_value

        elif (f_of_middle_value * f_of_final_value) < 0:
            initial_value = middle_value

        main_execute(f"x={initial_value}")
        f_of_initial_value = main_execute(f"{function_exp}")
        main_execute(f"x={final_value}")
        f_of_final_value = main_execute(f"{function_exp}")


if __name__ == "__main__":
    exp1 = "x^2-2*x-6"
    a = -5
    b = 2
    print(bisection_method(exp1, a, b))
