import unittest
from err_simplifier import simplify_message

class TestSimplifyMessage(unittest.TestCase):
    
    def test_already_satisfied(self):
        self.assertEqual(simplify_message("Requirement already satisfied: package"), "Already satisfied/installed: package")
    
    def test_defaulting_to_user_installation(self):
        self.assertEqual(simplify_message("Defaulting to user installation"), "Defaulting to user installation because system-wide site-packages are not writable.")
    
    # Add more tests here

if __name__ == '__main__':
    unittest.main()
