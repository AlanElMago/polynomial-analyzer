from typing import Any

from parser.polynomial_parser import PolynomialParser

def main() -> None:
    parser = PolynomialParser.build()
    text: str = ''
    result: Any | None = None

    while True:
        try:
            text = input('poly_calc > ')
        except EOFError:
            print('EOFError')
            break
        except KeyboardInterrupt:
            print('KeyboardInterrupt')
            break

        try:
            result = parser.parse(text)
        except ValueError:
            print('Undefined')
            continue
        except ZeroDivisionError:
            print('Division by zero')
            continue

        print(result)

if __name__ == '__main__':
    main()
