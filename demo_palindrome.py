import unittest

def is_palindrome(s):
    """
    Check if a given string is a palindrome.

    A palindrome is a string that reads the same forwards and backwards,
    ignoring case and any non-alphanumeric characters (spaces, punctuation, etc.).

    Args:
        s (str): The input string to check for palindrome properties.

    Returns:
        bool: True if the string is a palindrome, False otherwise.

    Example usage:
        >>> is_palindrome("A man a plan a canal Panama")
        True
        >>> is_palindrome("Hello")
        False

    Edge cases:
        - An empty string is considered a palindrome.
        - Strings with only spaces are also treated as palindromes.
        - Single-character strings are palindromes by default.
    """
    cleaned = "".join(c.lower() for c in s if c.isalnum())
    return cleaned == cleaned[::-1]

class TestIsPalindrome(unittest.TestCase):
    
    def test_basic_functionality(self):
        self.assertTrue(is_palindrome("A man a plan a canal Panama"))
        self.assertTrue(is_palindrome("racecar"))
        self.assertFalse(is_palindrome("Hello"))
        self.assertFalse(is_palindrome("Python"))

    def test_edge_cases(self):
        self.assertTrue(is_palindrome(""))
        self.assertTrue(is_palindrome(" "))  # Only spaces
        self.assertTrue(is_palindrome("a"))  # Single character
        self.assertTrue(is_palindrome("  A  "))  # Leading and trailing spaces

    def test_numerical_palindromes(self):
        self.assertTrue(is_palindrome("12321"))
        self.assertFalse(is_palindrome("12345"))

    def test_special_characters(self):
        self.assertTrue(is_palindrome("A man, a plan, a canal: Panama!"))
        # Leading digit breaks symmetry once non-letters are normalized to alnum
        self.assertFalse(is_palindrome("1A man, a plan, a canal: Panama!"))

    def test_mixed_case(self):
        self.assertTrue(is_palindrome("No lemon, no melon"))
        self.assertTrue(is_palindrome("Able was I ere I saw Elba"))
        self.assertFalse(is_palindrome("This is not a palindrome"))

    def test_long_strings(self):
        long_palindrome = "A" * 1000 + " " + "A" * 1000
        self.assertTrue(is_palindrome(long_palindrome))
        long_non_palindrome = "A" * 500 + "B" + "A" * 499
        self.assertFalse(is_palindrome(long_non_palindrome))

if __name__ == "__main__":
    unittest.main()
