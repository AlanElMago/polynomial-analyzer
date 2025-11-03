from lexer.polynomial_lexer import PolynomialLexer

import unittest

lexer = PolynomialLexer.build()

class TestArithmeticOperators(unittest.TestCase):
    def test_plus_operator(self):
        tokens = lexer.tokenize('+')

        self.assertEqual(tokens[0].type, 'PLUS')
        self.assertEqual(tokens[0].value, '+')

    def test_minus_operator(self):
        tokens = lexer.tokenize('-')

        self.assertEqual(tokens[0].type, 'MINUS')
        self.assertEqual(tokens[0].value, '-')

    def test_times_operator(self):
        tokens = lexer.tokenize('*')

        self.assertEqual(tokens[0].type, 'TIMES')
        self.assertEqual(tokens[0].value, '*')

    def test_divide_operator(self):
        tokens = lexer.tokenize('/')

        self.assertEqual(tokens[0].type, 'DIVIDE')
        self.assertEqual(tokens[0].value, '/')

    def test_power_operator(self):
        tokens = lexer.tokenize('**')

        self.assertEqual(tokens[0].type, 'POWER')
        self.assertEqual(tokens[0].value, '**')

class TestGroupingSymbols(unittest.TestCase):
    def test_left_parenthesis(self):
        tokens = lexer.tokenize('(')

        self.assertEqual(tokens[0].type, 'LPAREN')
        self.assertEqual(tokens[0].value, '(')

    def test_right_parenthesis(self):
        tokens = lexer.tokenize(')')

        self.assertEqual(tokens[0].type, 'RPAREN')
        self.assertEqual(tokens[0].value, ')')

    def test_vertical_bar(self):
        tokens = lexer.tokenize('|')

        self.assertEqual(tokens[0].type, 'VERT')
        self.assertEqual(tokens[0].value, '|')

class TestIdTokens(unittest.TestCase):
    def test_id_beginning_with_lowercase(self):
        tokens = lexer.tokenize('var1')

        self.assertEqual(tokens[0].type, 'ID')
        self.assertEqual(tokens[0].value, 'var1')

    def test_id_beginning_with_uppercase(self):
        tokens = lexer.tokenize('VarName')

        self.assertEqual(tokens[0].type, 'ID')
        self.assertEqual(tokens[0].value, 'VarName')

    def test_id_beginning_with_underscore(self):
        tokens = lexer.tokenize('_temp')

        self.assertEqual(tokens[0].type, 'ID')
        self.assertEqual(tokens[0].value, '_temp')

class TestNumberTokens(unittest.TestCase):
    def test_positive_integer(self):
        tokens = lexer.tokenize('123')

        self.assertEqual(tokens[0].type, 'NUMBER')
        self.assertEqual(tokens[0].value, 123)

    def test_negative_integer(self):
        tokens = lexer.tokenize('-456')

        self.assertEqual(tokens[0].type, 'MINUS')
        self.assertEqual(tokens[1].type, 'NUMBER')
        self.assertEqual(tokens[1].value, 456)

    def test_positive_real(self):
        tokens = lexer.tokenize('3.14')

        self.assertEqual(tokens[0].type, 'NUMBER')
        self.assertEqual(tokens[0].value, 3.14)

    def test_negative_real(self):
        tokens = lexer.tokenize('-0.001')

        self.assertEqual(tokens[0].type, 'MINUS')
        self.assertEqual(tokens[1].type, 'NUMBER')
        self.assertEqual(tokens[1].value, 0.001)

if __name__ == '__main__':
    unittest.main()
