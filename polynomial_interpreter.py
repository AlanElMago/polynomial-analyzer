from parser.polynomial_parser import PolynomialParser
from sys import stderr
from typing import Any

class PolynomialInterpreter:
    def __init__(self, text: str) -> None:
        self.text = text
        self.parser = PolynomialParser.build()

    def get_text(self) -> str:
        return self.text

    def evaulate(self, **kwargs) -> Any | None:
        for key, value in kwargs.items():
            self.parser.ids[key] = value

        result = None

        try:
            result = self.parser.parse(self.text)
        except ZeroDivisionError:
            print('Error: division by zero', file=stderr)
        except ValueError:
            print('Error: undefined result', file=stderr)

        return result
