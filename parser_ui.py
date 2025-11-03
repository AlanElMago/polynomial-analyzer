from parser.polynomial_parser import PolynomialParser

def main() -> None:
    parser = PolynomialParser.build()
    text = ''
    result = None

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

        if result is not None:
            print(result)

if __name__ == '__main__':
    main()
