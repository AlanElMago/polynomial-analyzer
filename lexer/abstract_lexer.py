from abc import ABC, abstractmethod
from sys import stderr
from typing import Tuple

import ply.lex as lex

class AbstractLexer(ABC):
    t_ignore = ' \t'

    def __init__(self) -> None:
        super().__init__()

        self.lexer: lex.Lexer | None = None

    def t_error(self, t: lex.LexToken) -> None:
        print(f"Illegal character '{t.value[0]}'", file=stderr)
        t.lexer.skip(1)

    def get_lexer(self) -> lex.Lexer:
        if self.lexer == None:
            raise RuntimeError("Lexer not built. Use the 'build' class \
                                method to create an instance.")

        return self.lexer

    @abstractmethod
    def tokenize(self, text: str) -> Tuple[lex.LexToken, ...]:
        ...

    @classmethod
    @abstractmethod
    def build(cls, **kwargs) -> 'AbstractLexer':
        ...
