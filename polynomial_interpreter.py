from parser.polynomial_parser import PolynomialParser
from typing import Any

class PolynomialInterpreter:
    def __init__(self, text: str) -> None:
        self.text = text
        self.parser = PolynomialParser.build()

    def get_text(self) -> str:
        return self.text

    def evaulate(self, **kwargs) -> Any:
        for key, value in kwargs.items():
            self.parser.ids[key] = value

        return self.parser.parse(self.text)
