import unittest

def add_numbers(a, b):
    """
    Adds two numbers together and returns the result.

    Summary:
    This function takes two numerical inputs, adds them, and provides the sum as the output.

    Args:
        a (int, float): The first number to be added.
        b (int, float): The second number to be added.

    Returns:
        int, float: The sum of the two input numbers. If both inputs are integers, the output will be an integer.
                    If either input is a float, the output will be a float.

    Example Usage:
        result = add_numbers(5, 3)
        print(result)  # Output: 8
        
        result = add_numbers(5.5, 4.5)
        print(result)  # Output: 10.0

    Edge Cases:
    - If both inputs are of different types (e.g., int and float), the output will be a float.
    - If either of the inputs is None or a non-numeric type (such as a string), the function will raise a TypeError.
    - The function does not handle complex numbers.

    Normalization:
    - The function does not normalize inputs; users must ensure that inputs are either numbers.
    """
    return a + b


class TestAddNumbers(unittest.TestCase):
    
    def test_basic_functionality(self):
        self.assertEqual(add_numbers(5, 3), 8)
        self.assertEqual(add_numbers(5.5, 4.5), 10.0)
        self.assertEqual(add_numbers(-1, 1), 0)
        self.assertEqual(add_numbers(-1.5, 1.5), 0.0)
        self.assertEqual(add_numbers(3, 7.5), 10.5)
        
    def test_edge_cases(self):
        self.assertEqual(add_numbers(1, 2.0), 3.0)  # int and float
        self.assertEqual(add_numbers(2.0, 3), 5.0)  # float and int
        
    def test_type_errors(self):
        with self.assertRaises(TypeError):
            add_numbers(None, 5)
        
        with self.assertRaises(TypeError):
            add_numbers(5, "three")
        
        with self.assertRaises(TypeError):
            add_numbers("five", "three")
        
        with self.assertRaises(TypeError):
            add_numbers(5, [])
        
        with self.assertRaises(TypeError):
            add_numbers({}, 4)

if __name__ == "__main__":
    unittest.main()
