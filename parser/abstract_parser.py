from abc import ABC, abstractmethod
from sys import stderr
from typing import Any, Dict, List

import ply.yacc as yacc
import ply.lex as lex

class AbstractParser(ABC):
    """
    Abstract base class for parsers.

    Attributes
    ----------
    lexer : lex.Lexer
        The PLY lexer instance used by the AbstractParser.
    tokens : List[str]
        A list of names of all token types.
    parser : yacc.LRParser | None
        The PLY parser instance used by the AbstractParser.
    ids : Dict[str, Any]
        A dictionary for storing identifiers and their associated values.
    """

    def __init__(self, lexer: lex.Lexer, tokens: List[str]) -> None:
        """
        Initialize a AbstractParser instance.

        Parameters
        ----------
        lexer : lex.Lexer
            The PLY lexer instance used by the AbstractParser.
        tokens : List[str]
            A list of names of all token types.
        """
        super().__init__()

        self.lexer = lexer
        self.tokens = tokens

        self.parser: yacc.LRParser | None = None
        self.ids: Dict[str, Any] = {}

    def p_error(self, _) -> None:
        """
        Error handling rule for syntax errors.
        """
        print(f"Syntax error", file=stderr)

    def get_parser(self) -> yacc.LRParser:
        """
        Get the PLY parser instance.

        Returns
        -------
        yacc.LRParser
            The PLY parser instance.

        Raises
        ------
        RuntimeError
            If the parser has not been built yet.
        """
        if self.parser == None:
            raise RuntimeError("Parser not built. Use the 'build' class \
                                method to create an instance.")

        return self.parser

    @abstractmethod
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
        """
        ...

    @classmethod
    @abstractmethod
    def build(cls, **kwargs) -> 'AbstractParser':
        """
        Build and return an instance of the AbstractParser.

        Parameters
        ----------
        **kwargs
            Additional keyword arguments to pass to the PLY lexer instance that
            will be used by the AbstractParser.

        Returns
        -------
        AbstractParser
            An instance of AbstractParser.
        """
        ...
