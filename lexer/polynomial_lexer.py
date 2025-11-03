import ply.lex as lex

from lexer.abstract_lexer import AbstractLexer
from sys import stderr
from typing import List, Tuple

class PolynomialLexer(AbstractLexer):
    reserved = {
        'sin': 'SINE',
        'cos': 'COSINE',
        'tan': 'TANGENT',
        'asin': 'ARCSINE',
        'acos': 'ARCCOSINE',
        'atan': 'ARCTANGENT',
        'exp': 'EXPONENTIAL',
        'ln': 'NATURAL_LOG',
        'log2': 'LOG_BASE_2',
        'log10': 'LOG_BASE_10',
    }

    tokens: List[str] = [
        'ID',
        'NUMBER',
        'POWER',
        'EQUALS',
        'PLUS',
        'MINUS',
        'TIMES',
        'DIVIDE',
        'LPAREN',
        'RPAREN',
        'VERT',
    ] + list(reserved.values())

    t_POWER  = r'\*\*'
    t_EQUALS = r'\='
    t_PLUS   = r'\+'
    t_MINUS  = r'\-'
    t_TIMES  = r'\*'
    t_DIVIDE = r'\/'
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_VERT   = r'\|'

    def t_ID(self, t) -> lex.LexToken:
        r'[a-zA-Z_][a-zA-Z0-9_]*'

        t.type = self.reserved.get(t.value, 'ID')

        return t

    def t_NUMBER(self, t) -> lex.LexToken:
        r'\d+(\.\d+)?'

        try:
            t.value = float(t.value) if '.' in t.value else int(t.value)
        except ValueError as e:
            print(e, file=stderr)

        return t

    def tokenize(self, text: str) -> Tuple[lex.LexToken, ...]:
        lexer = self.get_lexer()
        lexer.input(text)

        return tuple(token for token in lexer)

    @classmethod
    def build(cls, **kwargs) -> 'PolynomialLexer':
        polynomial_lexer = PolynomialLexer()
        polynomial_lexer.lexer = lex.lex(module=polynomial_lexer, **kwargs)

        return polynomial_lexer
