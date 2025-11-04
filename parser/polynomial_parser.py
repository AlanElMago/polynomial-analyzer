import math
from typing import Any, List, Tuple

import ply.lex as lex
import ply.yacc as yacc
from parser.abstract_parser import AbstractParser
from lexer.polynomial_lexer import PolynomialLexer

class PolynomialParser(AbstractParser):
    """
    Parser for polynomial expressions.

    Attributes
    ----------
    precedence : Tuple[Tuple[str, ...], ...]
        A tuple defining the precedence and associativity of operators.
        Operators with the highest precedence are evaluated first.

    Notes
    -----
    Attributes and methods that begin with `p_` define production rules for the
    underlying PLY parser.

    Examples
    --------
    >>> parser = PolynomialParser.build()
    >>> parser.parse('x = 2 + 3')
    5
    >>> parser.parse('x * x')
    25
    """

    precedence: Tuple[Tuple[str, ...], ...] = (
        ('right', 'EQUALS'),         # associativity right, precedence = 0
        ('left', 'PLUS', 'MINUS'),   # associativity left,  precedence = 1
        ('left', 'TIMES', 'DIVIDE'), # associativity left,  precedence = 2
        ('right', 'POWER'),          # associativity right, precedence = 3
    )

    def __init__(self, lexer: lex.Lexer, tokens: List[str]) -> None:
        """
        Initialize a PolynomialParser instance.

        Parameters
        ----------
        lexer : lex.Lexer
            The PLY lexer instance used by the PolynomialParser.
        tokens : List[str]
            A list of names of all token types.       

        .. warning::
            Do not instantiate this class directly. Use the `build` class
            method instead to properly initialize a PolynomialParser.

        See Also
        --------
        PolynomialParser.build : Preferred method for creating a
            PolynomialParser instance.
        """
        super().__init__(lexer, tokens)

    def p_assignment_expression(self, p: yacc.YaccProduction) -> None:
        '''expression : ID EQUALS expression'''
        result = p[3]
        self.ids[p[1]] = result
        p[0] = result

    def p_function_expression(self, p: yacc.YaccProduction) -> None:
        '''expression : SINE LPAREN expression RPAREN
                      | COSINE LPAREN expression RPAREN
                      | TANGENT LPAREN expression RPAREN
                      | ARCSINE LPAREN expression RPAREN
                      | ARCCOSINE LPAREN expression RPAREN
                      | ARCTANGENT LPAREN expression RPAREN
                      | EXPONENTIAL LPAREN expression RPAREN
                      | NATURAL_LOG LPAREN expression RPAREN
                      | LOG_BASE_2 LPAREN expression RPAREN
                      | LOG_BASE_10 LPAREN expression RPAREN
                      | SQUARE_ROOT LPAREN expression RPAREN
        '''
        match p[1]:
            case 'sin':
                p[0] = math.sin(p[3])
            case 'cos':
                p[0] = math.cos(p[3])
            case 'tan':
                p[0] = math.tan(p[3])
            case 'asin':
                p[0] = math.asin(p[3])
            case 'acos':
                p[0] = math.acos(p[3])
            case 'atan':
                p[0] = math.atan(p[3])
            case 'exp':
                p[0] = math.exp(p[3])
            case 'ln':
                p[0] = math.log(p[3])
            case 'log2':
                p[0] = math.log2(p[3])
            case 'log10':
                p[0] = math.log10(p[3])
            case 'sqrt':
                p[0] = math.sqrt(p[3])

    def p_unary_expression(self, p: yacc.YaccProduction) -> None:
        '''expression : MINUS expression'''
        p[0] = -p[2]

    def p_binary_expression(self, p: yacc.YaccProduction) -> None:
        '''expression : expression PLUS expression
                      | expression MINUS expression
                      | expression TIMES expression
                      | expression DIVIDE expression
                      | expression POWER expression
        '''
        match p[2]:
            case '+':
                p[0] = p[1] + p[3]
            case '-':
                p[0] = p[1] - p[3]
            case '*':
                p[0] = p[1] * p[3]
            case '/':
                p[0] = p[1] / p[3]
            case '**':
                p[0] = p[1] ** p[3]

    def p_group_expression(self, p: yacc.YaccProduction) -> None:
        '''expression : LPAREN expression RPAREN
                      | VERT expression VERT
        '''
        match p[1]:
            case '(':
                p[0] = p[2]
            case '|':
                p[0] = abs(p[2])

    def p_id_expression(self, p: yacc.YaccProduction) -> None:
        '''expression : ID'''
        try:
            p[0] = self.ids[p[1]]
        except:
            text: str = input(f'{p[1]} = ')

            sub_parser = PolynomialParser.build()
            sub_parser.ids = self.ids
            p[0] = sub_parser.parse(text)

            self.ids[p[1]] = p[0]

    def p_number_expression(self, p: yacc.YaccProduction) -> None:
        '''expression : NUMBER'''
        p[0] = p[1]

    def parse(self, text: str) -> Any:
        """
        Parse the input text.

        Parameters
        ----------
        text : str
            The input text to be parsed.

        Returns
        -------
        Any
            The result of parsing the input text.

        Raises
        ------
        ValueError
            If the result of the parsed expression is undefined.
        DivisionByZeroError
            If a division by zero occurs in the parsed expression.
        """
        parser = self.get_parser()

        return parser.parse(input=text, lexer=self.lexer)

    @classmethod
    def build(cls, **kwargs) -> 'PolynomialParser':
        """
        Build and return an instance of the PolynomialParser.

        This is the preferred way to create a PolynomialParser instance, as it
        properly initializes the underlying PLY parser.

        Parameters
        ----------
        **kwargs
            Additional keyword arguments to pass to the PLY lexer used by the
            PolynomialParser

        Returns
        -------
        PolynomialParser
            An instance of PolynomialParser.
        """
        polynomial_lexer = PolynomialLexer.build(**kwargs)

        lexer: lex.Lexer = polynomial_lexer.get_lexer()
        tokens: List[str] = polynomial_lexer.tokens

        polynomial_parser = PolynomialParser(lexer, tokens)
        polynomial_parser.parser = yacc.yacc(module=polynomial_parser)

        return polynomial_parser
