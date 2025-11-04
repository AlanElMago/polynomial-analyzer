from sys import stderr
from typing import Any

from parser.polynomial_parser import PolynomialParser

class PolynomialInterpreter:
    """
    Interpreter for polynomial expressions.

    Attributes
    ----------
    text : str
        The polynomial expression to be interpreted.
    parser : PolynomialParser
        The parser used to parse and evaluate the polynomial expression.

    Examples
    --------
    >>> p = PolynomialInterpreter('3.58*x**5 + 6.28*x**2*y*z + x*y*z**3 + 3')
    >>> p.evaulate(x=2, y=1, z=0.5)
    130.37
    """

    def __init__(self, text: str) -> None:
        """
        Initialize a PolynomialInterpreter instance.

        Parameters
        ----------
        text : str
            The polynomial expression to be interpreted.
        """

        self.text = text
        self.parser = PolynomialParser.build()

    def get_text(self) -> str:
        """
        Get the polynomial expression text.

        Returns
        -------
        str
            The polynomial expression text.
        """
        return self.text

    def evaulate(self, **kwargs) -> Any | None:
        """
        Evaluate the polynomial expression with the given variable values.

        Parameters
        ----------
        **kwargs
            Variable values to be used in the evaluation of the polynomial
            expression.

        Returns
        -------
        Any | None
            The result of the evaluation, or None if an error occurred.
        """
        for key, value in kwargs.items():
            self.parser.ids[key] = value

        result: Any | None = None

        try:
            result = self.parser.parse(self.text)
        except ZeroDivisionError:
            print('Error: division by zero', file=stderr)
        except ValueError:
            print('Error: undefined result', file=stderr)

        return result
