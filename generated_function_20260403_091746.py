def factorial(n):
    """Calculate the factorial of a non-negative integer n.

    The factorial of a non-negative integer n is the product of all positive integers less than or equal to n.
    For example, factorial(5) = 5 * 4 * 3 * 2 * 1 = 120.

    Args:
        n (int): A non-negative integer whose factorial is to be computed.

    Returns:
        int: The factorial of n.

    Raises:
        ValueError: If n is a negative integer.

    Example:
        >>> factorial(5)
        120
        >>> factorial(0)
        1

    Edge Cases:
        - factorial(0) returns 1 as defined for factorial.
        - Attempts to calculate factorial for negative integers will raise a ValueError.
    """
    if n < 0:
        raise ValueError("Input must be a non-negative integer.")
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

import unittest

class TestFactorial(unittest.TestCase):

    def test_basic_functionality(self):
        self.assertEqual(factorial(5), 120)
        self.assertEqual(factorial(3), 6)

    def test_edge_cases(self):
        self.assertEqual(factorial(0), 1)  # Edge case for 0
        self.assertEqual(factorial(1), 1)  # Edge case for 1

    def test_error_cases(self):
        with self.assertRaises(ValueError):
            factorial(-1)  # Negative input should raise ValueError
        with self.assertRaises(ValueError):
            factorial(-10)  # Another negative input

    def test_large_input(self):
        self.assertEqual(factorial(10), 3628800)  # Standard large input
        self.assertEqual(factorial(20), 2432902008176640000)  # Very large input

    def test_non_integer_input(self):
        with self.assertRaises(TypeError):
            factorial(5.5)  # Non-integer input should raise TypeError
        with self.assertRaises(TypeError):
            factorial("5")  # String input should raise TypeError

if __name__ == "__main__":
    unittest.main()
