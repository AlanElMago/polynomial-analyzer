from sys import stderr
from typing import Dict, List, Tuple

import ply.lex as lex
from lexer.abstract_lexer import AbstractLexer

class PolynomialLexer(AbstractLexer):
    """
    Lexer for polynomial expressions.

    Attributes
    ----------
    reserved : Dict[str, str]
        A dictionary mapping reserved keywords to their token types.
    tokens : List[str]
        A list of names of all token types.

    Notes
    -----
    Attributes and methods that begin with `t_` define token rules for the
    underlying PLY lexer.

    Examples
    --------
    >>> lexer = PolynomialLexer.build()
    >>> lexer.tokenize('x + 2')
    (LexToken(ID,'x',1,0), LexToken(PLUS,'+',1,2), LexToken(NUMBER,2,1,4))
    """

    reserved: Dict[str, str] = {
        'sin'   : 'SINE',
        'cos'   : 'COSINE',
        'tan'   : 'TANGENT',
        'asin'  : 'ARCSINE',
        'acos'  : 'ARCCOSINE',
        'atan'  : 'ARCTANGENT',
        'exp'   : 'EXPONENTIAL',
        'ln'    : 'NATURAL_LOG',
        'log2'  : 'LOG_BASE_2',
        'log10' : 'LOG_BASE_10',
        'sqrt'  : 'SQUARE_ROOT',
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

    def __init__(self) -> None:
        """
        Initialize a PolynomialLexer instance.

        .. warning::
            Do not instantiate this class directly. Use the `build` class
            method instead to properly initialize a PolynomialLexer.

        See Also
        --------
        PolynomialLexer.build : Preferred method for creating a PolynomialLexer
            instance.
        """
        super().__init__()

    def t_ID(self, t: lex.LexToken) -> lex.LexToken:
        r'[a-zA-Z_][a-zA-Z0-9_]*'

        t.type = self.reserved.get(t.value, 'ID')

        return t

    def t_NUMBER(self, t: lex.LexToken) -> lex.LexToken:
        r'\d+(\.\d+)?'

        try:
            t.value = float(t.value) if '.' in t.value else int(t.value)
        except ValueError as e:
            print(e, file=stderr)

        return t

    def tokenize(self, text: str) -> Tuple[lex.LexToken, ...]:
        lexer: lex.Lexer = self.get_lexer()
        lexer.input(text)

        return tuple(token for token in lexer)

    @classmethod
    def build(cls, **kwargs) -> 'PolynomialLexer':
        """
        Build and return an instance of the PolynomialLexer.

        This is the preferred way to create a PolynomialLexer instance, as it
        properly initializes the underlying PLY lexer.

        Parameters
        ----------
        **kwargs
            Additional keyword arguments to pass to the PLY lexer used by the
            PolynomialLexer.
    
        Returns
        -------
        PolynomialLexer
            An instance of PolynomialLexer.
        """
        polynomial_lexer = PolynomialLexer()
        polynomial_lexer.lexer = lex.lex(module=polynomial_lexer, **kwargs)

        return polynomial_lexer
