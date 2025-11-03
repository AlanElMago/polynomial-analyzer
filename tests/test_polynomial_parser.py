import math
import unittest

from parser.polynomial_parser import PolynomialParser

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

class TestExponentialFunction(unittest.TestCase):
    def setUp(self):
        self.parser = PolynomialParser.build()

    def test_exponential(self):
        result = self.parser.parse('exp(0)')
        self.assertAlmostEqual(result, 1, places=10)

    def test_exponential_with_one(self):
        result = self.parser.parse('exp(1)')
        self.assertAlmostEqual(result, math.e, places=10)

    def test_exponential_with_positive_value(self):
        result = self.parser.parse('exp(2)')
        self.assertAlmostEqual(result, math.exp(2), places=10)

    def test_exponential_with_negative_value(self):
        result = self.parser.parse('exp(-1)')
        self.assertAlmostEqual(result, math.exp(-1), places=10)

    def test_exponential_with_expression(self):
        result = self.parser.parse('exp(2 * 3)')
        self.assertAlmostEqual(result, math.exp(6), places=10)

    def test_nested_exponential(self):
        result = self.parser.parse('exp(exp(0))')
        self.assertAlmostEqual(result, math.e, places=10)

class TestLogarithmicFunctions(unittest.TestCase):
    def setUp(self):
        self.parser = PolynomialParser.build()

    def test_natural_log(self):
        result = self.parser.parse('ln(1)')
        self.assertAlmostEqual(result, 0, places=10)

    def test_natural_log_of_e(self):
        self.parser.parse('e = 2.71828182846')
        result = self.parser.parse('ln(e)')
        self.assertAlmostEqual(result, 1, places=5)

    def test_natural_log_positive_value(self):
        result = self.parser.parse('ln(10)')
        self.assertAlmostEqual(result, math.log(10), places=10)

    def test_log_base_2(self):
        result = self.parser.parse('log2(8)')
        self.assertAlmostEqual(result, 3, places=10)

    def test_log_base_2_of_one(self):
        result = self.parser.parse('log2(1)')
        self.assertAlmostEqual(result, 0, places=10)

    def test_log_base_2_positive_value(self):
        result = self.parser.parse('log2(16)')
        self.assertAlmostEqual(result, 4, places=10)

    def test_log_base_10(self):
        result = self.parser.parse('log10(100)')
        self.assertAlmostEqual(result, 2, places=10)

    def test_log_base_10_of_one(self):
        result = self.parser.parse('log10(1)')
        self.assertAlmostEqual(result, 0, places=10)

    def test_log_base_10_positive_value(self):
        result = self.parser.parse('log10(1000)')
        self.assertAlmostEqual(result, 3, places=10)

    def test_natural_log_with_expression(self):
        result = self.parser.parse('ln(2 * 5)')
        self.assertAlmostEqual(result, math.log(10), places=10)

    def test_nested_logarithms(self):
        result = self.parser.parse('ln(exp(2))')
        self.assertAlmostEqual(result, 2, places=10)

    def test_log2_with_power(self):
        result = self.parser.parse('log2(2 ** 5)')
        self.assertAlmostEqual(result, 5, places=10)

class TestSquareRootFunction(unittest.TestCase):
    def setUp(self):
        self.parser = PolynomialParser.build()

    def test_square_root_perfect_square(self):
        result = self.parser.parse('sqrt(4)')
        self.assertAlmostEqual(result, 2, places=10)

    def test_square_root_of_zero(self):
        result = self.parser.parse('sqrt(0)')
        self.assertAlmostEqual(result, 0, places=10)

    def test_square_root_of_one(self):
        result = self.parser.parse('sqrt(1)')
        self.assertAlmostEqual(result, 1, places=10)

    def test_square_root_non_perfect_square(self):
        result = self.parser.parse('sqrt(2)')
        self.assertAlmostEqual(result, math.sqrt(2), places=10)

    def test_square_root_large_number(self):
        result = self.parser.parse('sqrt(100)')
        self.assertAlmostEqual(result, 10, places=10)

    def test_square_root_with_expression(self):
        result = self.parser.parse('sqrt(16 + 9)')
        self.assertAlmostEqual(result, 5, places=10)

    def test_nested_square_root(self):
        result = self.parser.parse('sqrt(sqrt(16))')
        self.assertAlmostEqual(result, 2, places=10)

    def test_square_root_with_variable(self):
        self.parser.parse('x = 9')
        result = self.parser.parse('sqrt(x)')
        self.assertAlmostEqual(result, 3, places=10)

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

    def test_exponential_in_arithmetic(self):
        result = self.parser.parse('2 * exp(1)')
        self.assertAlmostEqual(result, 2 * math.e, places=10)

    def test_exponential_with_variable(self):
        self.parser.parse('x = 2')
        result = self.parser.parse('exp(x)')
        self.assertAlmostEqual(result, math.exp(2), places=10)

    def test_mixed_exponential_and_trig(self):
        result = self.parser.parse('exp(sin(0)) + cos(0)')
        self.assertAlmostEqual(result, 2, places=10)  # exp(0) + 1 = 1 + 1

    def test_logarithm_in_arithmetic(self):
        result = self.parser.parse('2 * ln(10)')
        self.assertAlmostEqual(result, 2 * math.log(10), places=10)

    def test_mixed_log_and_exponential(self):
        result = self.parser.parse('ln(exp(5))')
        self.assertAlmostEqual(result, 5, places=10)

    def test_logarithm_with_variable(self):
        self.parser.parse('x = 100')
        result = self.parser.parse('log10(x)')
        self.assertAlmostEqual(result, 2, places=10)

    def test_complex_log_expression(self):
        result = self.parser.parse('log2(8) + log10(100) + ln(1)')
        self.assertAlmostEqual(result, 5, places=10)  # 3 + 2 + 0

    def test_square_root_in_arithmetic(self):
        result = self.parser.parse('2 * sqrt(9)')
        self.assertAlmostEqual(result, 6, places=10)

    def test_square_root_with_power(self):
        result = self.parser.parse('sqrt(4) ** 2')
        self.assertAlmostEqual(result, 4, places=10)

    def test_pythagorean_theorem(self):
        self.parser.parse('a = 3')
        self.parser.parse('b = 4')
        result = self.parser.parse('sqrt(a ** 2 + b ** 2)')
        self.assertAlmostEqual(result, 5, places=10)

    def test_mixed_functions_with_sqrt(self):
        result = self.parser.parse('sqrt(16) + ln(1) + exp(0)')
        self.assertAlmostEqual(result, 5, places=10)  # 4 + 0 + 1

if __name__ == '__main__':
    unittest.main()
