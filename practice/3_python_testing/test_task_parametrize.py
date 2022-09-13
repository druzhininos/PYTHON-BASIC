"""
Write a parametrized test for two functions.
The functions are used to find a number by ordinal in the Fibonacci sequence.
One of them has a bug.

Fibonacci sequence: https://en.wikipedia.org/wiki/Fibonacci_number

Task:
 1. Write a test with @pytest.mark.parametrize decorator.
 2. Find the buggy function and fix it.
"""

import pytest

def fibonacci_1(n):
    a, b = 0, 1
    if n > 0:
        for _ in range(n-1):
            a, b = b, a + b
        return b
    return 0


def fibonacci_2(n):
    fibo = [0, 1]
    for i in range(2, n+1):
        fibo.append(fibo[i-1] + fibo[i-2])
    return fibo[n]

fibo_array = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597, 2584, 4181, 6765]
fibo_tuples = list(enumerate(fibo_array))
print (fibo_tuples)
@pytest.mark.parametrize("n, fibo", fibo_tuples)
def test_fibonacci_1(n, fibo):
    assert fibo == fibonacci_1(n)

@pytest.mark.parametrize("n, fibo", fibo_tuples)
def test_fibonacci_2(n, fibo):
    assert fibo == fibonacci_2(n)