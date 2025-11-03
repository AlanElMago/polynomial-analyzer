from parser.polynomial_parser import PolynomialParser

import unittest
import math

class TestBasicArithmetic(unittest.TestCase):
    def setUp(self):
        self.parser = PolynomialParser.build()

    def test_addition(self):
        result = self.parser.parse('2 + 3')
        self.assertEqual(result, 5)

    def test_subtraction(self):
        result = self.parser.parse('10 - 4')
        self.assertEqual(result, 6)

    def test_multiplication(self):
        result = self.parser.parse('6 * 7')
        self.assertEqual(result, 42)

    def test_division(self):
        result = self.parser.parse('15 / 3')
        self.assertEqual(result, 5)

    def test_power(self):
        result = self.parser.parse('2 ** 3')
        self.assertEqual(result, 8)

    def test_unary_minus(self):
        result = self.parser.parse('-5')
        self.assertEqual(result, -5)

    def test_unary_minus_with_expression(self):
        result = self.parser.parse('-(3 + 2)')
        self.assertEqual(result, -5)

class TestOperatorPrecedence(unittest.TestCase):
    def setUp(self):
        self.parser = PolynomialParser.build()

    def test_multiplication_before_addition(self):
        result = self.parser.parse('2 + 3 * 4')
        self.assertEqual(result, 14)

    def test_division_before_subtraction(self):
        result = self.parser.parse('20 - 10 / 2')
        self.assertEqual(result, 15)

    def test_power_before_multiplication(self):
        result = self.parser.parse('2 * 3 ** 2')
        self.assertEqual(result, 18)

    def test_power_right_associative(self):
        result = self.parser.parse('2 ** 3 ** 2')
        self.assertEqual(result, 512)  # 2 ** (3 ** 2) = 2 ** 9

    def test_left_to_right_same_precedence(self):
        result = self.parser.parse('10 - 3 - 2')
        self.assertEqual(result, 5)  # (10 - 3) - 2

class TestGroupingSymbols(unittest.TestCase):
    def setUp(self):
        self.parser = PolynomialParser.build()

    def test_parentheses_override_precedence(self):
        result = self.parser.parse('(2 + 3) * 4')
        self.assertEqual(result, 20)

    def test_nested_parentheses(self):
        result = self.parser.parse('((2 + 3) * (4 + 1))')
        self.assertEqual(result, 25)

    def test_absolute_value_positive(self):
        result = self.parser.parse('|5|')
        self.assertEqual(result, 5)

    def test_absolute_value_negative(self):
        result = self.parser.parse('|-5|')
        self.assertEqual(result, 5)

    def test_absolute_value_expression(self):
        result = self.parser.parse('|3 - 7|')
        self.assertEqual(result, 4)

    def test_absolute_value_in_arithmetic(self):
        result = self.parser.parse('2 * |-3|')
        self.assertEqual(result, 6)

class TestVariableAssignment(unittest.TestCase):
    def setUp(self):
        self.parser = PolynomialParser.build()

    def test_simple_assignment(self):
        result = self.parser.parse('x = 5')
        self.assertEqual(result, 5)
        self.assertEqual(self.parser.ids['x'], 5)

    def test_assignment_with_expression(self):
        result = self.parser.parse('y = 2 + 3')
        self.assertEqual(result, 5)
        self.assertEqual(self.parser.ids['y'], 5)

    def test_variable_usage(self):
        self.parser.parse('a = 10')
        result = self.parser.parse('a + 5')
        self.assertEqual(result, 15)

    def test_multiple_variable_usage(self):
        self.parser.parse('x = 3')
        self.parser.parse('y = 4')
        result = self.parser.parse('x * y')
        self.assertEqual(result, 12)

    def test_variable_reassignment(self):
        self.parser.parse('z = 5')
        result = self.parser.parse('z = 10')
        self.assertEqual(result, 10)
        self.assertEqual(self.parser.ids['z'], 10)

    def test_assignment_with_existing_variable(self):
        self.parser.parse('a = 5')
        result = self.parser.parse('b = a * 2')
        self.assertEqual(result, 10)
        self.assertEqual(self.parser.ids['b'], 10)

class TestTrigonometricFunctions(unittest.TestCase):
    def setUp(self):
        self.parser = PolynomialParser.build()

    def test_sine(self):
        result = self.parser.parse('sin(0.5)')
        self.assertAlmostEqual(result, math.sin(0.5), places=10)

    def test_cosine(self):
        result = self.parser.parse('cos(0.5)')
        self.assertAlmostEqual(result, math.cos(0.5), places=10)

    def test_tangent(self):
        result = self.parser.parse('tan(0.5)')
        self.assertAlmostEqual(result, math.tan(0.5), places=10)

    def test_arcsine(self):
        result = self.parser.parse('asin(0.5)')
        self.assertAlmostEqual(result, math.asin(0.5), places=10)

    def test_arccosine(self):
        result = self.parser.parse('acos(0.5)')
        self.assertAlmostEqual(result, math.acos(0.5), places=10)

    def test_arctangent(self):
        result = self.parser.parse('atan(0.5)')
        self.assertAlmostEqual(result, math.atan(0.5), places=10)

    def test_sine_with_pi(self):
        self.parser.parse('pi = 3.14159265359')
        result = self.parser.parse('sin(pi / 2)')
        self.assertAlmostEqual(result, 1, places=5)

    def test_cosine_with_pi(self):
        self.parser.parse('pi = 3.14159265359')
        result = self.parser.parse('cos(pi)')
        self.assertAlmostEqual(result, -1, places=5)

    def test_tangent_with_pi(self):
        self.parser.parse('pi = 3.14159265359')
        result = self.parser.parse('tan(pi / 4)')
        self.assertAlmostEqual(result, 1, places=5)

    def test_nested_trig_functions(self):
        result = self.parser.parse('sin(cos(0))')
        self.assertAlmostEqual(result, math.sin(math.cos(0)), places=10)

    def test_trig_function_with_expression(self):
        result = self.parser.parse('sin(2 * 3)')
        self.assertAlmostEqual(result, math.sin(6), places=10)

class TestComplexExpressions(unittest.TestCase):
    def setUp(self):
        self.parser = PolynomialParser.build()

    def test_polynomial_evaluation(self):
        self.parser.parse('x = 2')
        result = self.parser.parse('3 * x ** 2 + 2 * x + 1')
        self.assertEqual(result, 17)  # 3*4 + 2*2 + 1

    def test_expression_with_all_operators(self):
        result = self.parser.parse('2 + 3 * 4 - 6 / 2 ** 2')
        self.assertEqual(result, 12.5)  # 2 + 12 - 1.5

    def test_mixed_trig_and_arithmetic(self):
        result = self.parser.parse('2 * sin(0) + 3 * cos(0)')
        self.assertAlmostEqual(result, 3, places=10)

    def test_complex_nested_expression(self):
        result = self.parser.parse('((2 + 3) * |sin(0) - 5|) / 2')
        self.assertAlmostEqual(result, 12.5, places=10)

    def test_variable_in_trig_function(self):
        self.parser.parse('angle = 0')
        result = self.parser.parse('sin(angle)')
        self.assertAlmostEqual(result, 0, places=10)

    def test_chained_assignments(self):
        result = self.parser.parse('a = b = c = 5')
        self.assertEqual(result, 5)
        self.assertEqual(self.parser.ids['a'], 5)
        self.assertEqual(self.parser.ids['b'], 5)
        self.assertEqual(self.parser.ids['c'], 5)

class TestFloatingPointNumbers(unittest.TestCase):
    def setUp(self):
        self.parser = PolynomialParser.build()

    def test_float_addition(self):
        result = self.parser.parse('2.5 + 3.7')
        self.assertAlmostEqual(result, 6.2, places=10)

    def test_float_division(self):
        result = self.parser.parse('7.5 / 2.5')
        self.assertAlmostEqual(result, 3.0, places=10)

    def test_mixed_int_float(self):
        result = self.parser.parse('5 * 2.5')
        self.assertAlmostEqual(result, 12.5, places=10)

    def test_float_power(self):
        result = self.parser.parse('2.0 ** 3.0')
        self.assertAlmostEqual(result, 8.0, places=10)

if __name__ == '__main__':
    unittest.main()
