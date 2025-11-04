from abc import ABC, abstractmethod
from sys import stderr
from typing import Tuple

import ply.lex as lex

class AbstractLexer(ABC):
    """
    Abstract base class for lexers.

    Attributes
    ----------
    t_ignore : str
        A string containing characters to be ignored by the lexer.
    lexer : lex.Lexer | None
        The PLY lexer instance used by the AbstractLexer.
    """
    t_ignore = ' \t'

    def __init__(self) -> None:
        """
        Initialize a AbstractLexer instance.
        """
        super().__init__()

        self.lexer: lex.Lexer | None = None

    def t_error(self, t: lex.LexToken) -> None:
        """
        Error handling rule for illegal characters.

        Parameters
        ----------
        t : lex.LexToken
            The token that caused the error.
        """
        print(f"Illegal character '{t.value[0]}'", file=stderr)
        t.lexer.skip(1)

    def get_lexer(self) -> lex.Lexer:
        """
        Get the PLY lexer instance.

        Returns
        -------
        lex.Lexer
            The PLY lexer instance.

        Raises
        ------
        RuntimeError
            If the lexer has not been built yet.
        """
        if self.lexer == None:
            raise RuntimeError("Lexer not built. Use the 'build' class \
                                method to create an instance.")

        return self.lexer

    @abstractmethod
    def tokenize(self, text: str) -> Tuple[lex.LexToken, ...]:
        """
        Tokenize the input text.

        Parameters
        ----------
        text : str
            The input text to be tokenized.

        Returns
        -------
        Tuple[lex.LexToken, ...]
            A tuple of tokens generated from the input text.
        """
        ...

    @classmethod
    @abstractmethod
    def build(cls, **kwargs) -> 'AbstractLexer':
        """
        Build and return an instance of the AbstractLexer.

        Parameters
        ----------
        **kwargs
            Additional keyword arguments for the PLY lexer instance that will
            be used by the AbstractLexer.

        Returns
        -------
        AbstractLexer
            An instance of AbstractLexer.
        """
        ...
