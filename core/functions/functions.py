"""
Function file that holds additional functions for Maths Software like 
factorial, sine, cosine, etc.
"""


def factorial(f1: int):
    fact_answer = 1
    if f1 >= 0:
        while f1 >= 1:
            fact_answer *= f1
            f1 -= 1
        return fact_answer
    else:
        return "No factorial for negative numbers"


def sin_function(s1: int):
    sin_ans1 = (s1 % 360) * 3.1415 / 180
    sin_ans2 = sin_ans1
    for i in range(1, 20):
        y = (2 * i) + 1
        if i % 2 == 1:
            sin_ans2 -= (sin_ans1**y) / factorial(y)
        else:
            sin_ans2 += (sin_ans1**y) / factorial(y)
    return round(sin_ans2, 4)


def cos_function(s1: int):
    cos_ans1 = (s1 % 360) * 3.1415 / 180
    cos_ans2 = 1
    for i in range(1, 20):
        y = 2 * i
        if i % 2 == 1:
            cos_ans2 -= (cos_ans1**y) / factorial(y)
        else:
            cos_ans2 += (cos_ans1**y) / factorial(y)
    return round(cos_ans2, 3)
