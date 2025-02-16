import unittest
from app import refactor_code

class TestRefactor(unittest.TestCase):
    def test_refactor_code(self):
        # Тест на удаление неиспользуемых импортов
        code = """
import unused_module
import os
print(os.getcwd())
"""
        expected = """
import os
print(os.getcwd())
"""
        self.assertEqual(refactor_code(code).strip(), expected.strip())

if __name__ == '__main__':
    unittest.main()