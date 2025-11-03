import math
import ply.yacc as yacc

from parser.abstract_parser import AbstractParser
from lexer.polynomial_lexer import PolynomialLexer
from typing import Any, Tuple

class PolynomialParser(AbstractParser):
    precedence: Tuple[Tuple[str, ...], ...] = (
        ('right', 'EQUALS'),
        ('left', 'PLUS', 'MINUS'),
        ('left', 'TIMES', 'DIVIDE'),
        ('right', 'POWER'),
    )

    def __init__(self, lexer, tokens) -> None:
        super().__init__(lexer, tokens)

    def p_assignment_expression(self, p):
        '''expression : ID EQUALS expression'''
        self.ids[p[1]] = p[3]

    def p_function_expression(self, p):
        '''expression : SINE LPAREN expression RPAREN
                      | COSINE LPAREN expression RPAREN
                      | TANGENT LPAREN expression RPAREN
        '''
        match p[1]:
            case 'sin':
                p[0] = math.sin(p[3])
            case 'cos':
                p[0] = math.cos(p[3])
            case 'tan':
                p[0] = math.tan(p[3])

    def p_binary_expression(self, p):
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

    def p_group_expression(self, p):
        '''expression : LPAREN expression RPAREN
                      | VERT expression VERT
        '''
        match p[1]:
            case '(':
                p[0] = p[2]
            case '|':
                p[0] = abs(p[2])

    def p_id_expression(self, p):
        '''expression : ID'''
        try:
            p[0] = self.ids[p[1]]
        except:
            text = input(f'{p[1]} = ')

            sub_parser = PolynomialParser.build()
            sub_parser.ids = self.ids
            p[0] = sub_parser.parse(text)

            self.ids[p[1]] = p[0]

    def p_number_expression(self, p):
        '''expression : NUMBER'''
        p[0] = p[1]

    def parse(self, text: str) -> Any:
        parser = self.get_parser()

        return parser.parse(input=text, lexer=self.lexer)

    @classmethod
    def build(cls, **kwargs) -> 'PolynomialParser':
        polynomial_lexer = PolynomialLexer.build(**kwargs)

        lexer = polynomial_lexer.get_lexer()
        tokens = polynomial_lexer.tokens

        polynomial_parser = PolynomialParser(lexer, tokens)
        polynomial_parser.parser = yacc.yacc(module=polynomial_parser)

        return polynomial_parser
