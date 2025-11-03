from abc import ABC, abstractmethod
from sys import stderr
from typing import Any, Dict, List

import ply.yacc as yacc
import ply.lex as lex

class AbstractParser(ABC):
    def __init__(self, lexer: lex.Lexer, tokens: List[str]) -> None:
        super().__init__()

        self.lexer = lexer
        self.tokens = tokens

        self.parser: yacc.LRParser | None = None
        self.ids: Dict[str, Any] = {}

    def p_error(self, _) -> None:
        print(f"Syntax error", file=stderr)

    def get_parser(self) -> yacc.LRParser:
        if self.parser == None:
            raise RuntimeError("Parser not built. Use the 'build' class \
                                method to create an instance.")

        return self.parser

    @abstractmethod
    def parse(self, text: str) -> Any:
        ...

    @classmethod
    @abstractmethod
    def build(cls) -> 'AbstractParser':
        ...
